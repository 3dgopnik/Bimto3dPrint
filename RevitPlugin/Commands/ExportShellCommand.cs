using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Interop;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Bimto3dPrint.Models;
using Bimto3dPrint.Services;
using Bimto3dPrint.UI;
using Bimto3dPrint.Utils;

namespace Bimto3dPrint.Commands
{
    /// <summary>
    /// Entry point command for exporting building shell.
    /// </summary>
    public class ExportShellCommand : IExternalCommand
    {
        /// <summary>
        /// Executes the export flow.
        /// </summary>
        /// <param name="commandData">Revit command data.</param>
        /// <param name="message">Failure message.</param>
        /// <param name="elements">Failure elements.</param>
        /// <returns>Execution result.</returns>
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            try
            {
                var uiApp = commandData.Application;
                var document = uiApp.ActiveUIDocument?.Document;
                if (document == null)
                {
                    message = "No active document found.";
                    Logger.Error(message);
                    return Result.Failed;
                }

                Logger.Info("Starting Bimto3dPrint export command.");

                var dialog = new ExportDialog();
                new WindowInteropHelper(dialog).Owner = uiApp.MainWindowHandle;

                var presets = LoadPresets();
                dialog.LoadPresets(presets);
                dialog.LoadOutputFormats(new[] { "stl", "obj", "fbx" });
                dialog.LoadIfcVersions(new[] { "IFC4", "IFC2x3" });

                var dialogResult = dialog.ShowDialog();
                if (dialogResult != true)
                {
                    Logger.Info("Export cancelled by user.");
                    return Result.Cancelled;
                }

                var preset = string.IsNullOrWhiteSpace(dialog.SelectedPreset) ? "shell_only" : dialog.SelectedPreset;
                var outputFormat = string.IsNullOrWhiteSpace(dialog.SelectedOutputFormat) ? "stl" : dialog.SelectedOutputFormat;
                var outputFolder = dialog.OutputFolder;

                if (string.IsNullOrWhiteSpace(outputFolder))
                {
                    message = "Output folder is required.";
                    Logger.Error(message);
                    TaskDialog.Show("Bimto3dPrint", message);
                    return Result.Failed;
                }

                if (dialog.MinWallThicknessMm <= 0)
                {
                    message = "Minimum wall thickness must be positive.";
                    Logger.Error(message);
                    TaskDialog.Show("Bimto3dPrint", message);
                    return Result.Failed;
                }

                var view3D = ResolveExportView(document);
                if (view3D == null)
                {
                    message = "No suitable 3D view found for export.";
                    Logger.Error(message);
                    TaskDialog.Show("Bimto3dPrint", message);
                    return Result.Failed;
                }

                var exportFolder = outputFolder;
                var exportFileName = BuildSafeFileName(document.Title);
                var ifcPath = Path.Combine(exportFolder, $"{exportFileName}.ifc");

                Logger.Info($"Exporting IFC to {ifcPath}");

                using (var progress = new ProgressDialog("Exporting IFC..."))
                {
                    progress.Show();

                    var exportSettings = new IfcExportSettings
                    {
                        IfcVersion = dialog.SelectedIfcVersion,
                        FilterViewId = view3D.Id,
                        ExportBaseQuantities = false,
                        UseActiveViewGeometry = true,
                        ExportLinkedFiles = false
                    };

                    try
                    {
                        var ifcService = new IfcExportService();
                        ifcPath = ifcService.ExportIfc(document, exportFolder, exportFileName, exportSettings);
                    }
                    catch (Exception ex)
                    {
                        message = $"IFC export failed: {ex.Message}";
                        Logger.Error(message);
                        TaskDialog.Show("Bimto3dPrint", message);
                        return Result.Failed;
                    }
                }

                if (!File.Exists(ifcPath))
                {
                    message = "IFC file was not created.";
                    Logger.Error(message);
                    TaskDialog.Show("Bimto3dPrint", message);
                    return Result.Failed;
                }

                if (dialog.RunPipelineAfterExport)
                {
                    var outputPath = Path.Combine(exportFolder, $"{exportFileName}.{outputFormat}");
                    var runner = new PythonRunner();
                    var presetReference = $"revit:{preset}";

                    if (!runner.Settings.UseTudelftExtractor && PresetUsesRevitCategories(preset))
                    {
                        message = "Selected preset uses BuiltInCategory.* and requires the TU Delft extractor.";
                        Logger.Error(message);
                        TaskDialog.Show("Bimto3dPrint", message);
                        return Result.Failed;
                    }

                    var options = new PythonRunOptions
                    {
                        MinWallMm = dialog.MinWallThicknessMm,
                        NoThicken = dialog.NoThicken
                    };

                    int exitCode;
                    try
                    {
                        exitCode = runner.RunBimto3dPrint(ifcPath, presetReference, outputPath, outputFormat, options);
                    }
                    catch (Exception ex)
                    {
                        message = $"Python pipeline failed: {ex.Message}";
                        Logger.Error(message);
                        TaskDialog.Show("Bimto3dPrint", message);
                        return Result.Failed;
                    }

                    if (exitCode != 0)
                    {
                        var errorMessage = $"Python pipeline failed (exit code {exitCode}). Log: {runner.LastLogPath}";
                        Logger.Error(errorMessage);
                        TaskDialog.Show("Bimto3dPrint", errorMessage);
                        return Result.Failed;
                    }

                    var successMessage = $"Export completed. Output: {outputPath}\nLog: {runner.LastLogPath}";
                    Logger.Info(successMessage);
                    TaskDialog.Show("Bimto3dPrint", successMessage);
                    return Result.Succeeded;
                }

                var exportMessage = $"IFC export completed: {ifcPath}";
                Logger.Info(exportMessage);
                TaskDialog.Show("Bimto3dPrint", exportMessage);
                return Result.Succeeded;
            }
            catch (Exception ex)
            {
                Logger.Error($"Unexpected error: {ex.Message}");
                message = ex.Message;
                TaskDialog.Show("Bimto3dPrint", $"Unexpected error: {ex.Message}");
                return Result.Failed;
            }
        }

        private static IEnumerable<string> LoadPresets()
        {
            try
            {
                var baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
                var presetDirectory = Path.Combine(baseDirectory, "Config", "Presets", "Revit");
                if (!Directory.Exists(presetDirectory))
                {
                    return new[] { "shell_only" };
                }

                return Directory.GetFiles(presetDirectory, "*.json")
                    .Select(path => Path.GetFileNameWithoutExtension(path))
                    .OrderBy(name => name)
                    .ToList();
            }
            catch (Exception ex)
            {
                Logger.Warn($"Failed to load presets: {ex.Message}");
                return new[] { "shell_only" };
            }
        }

        private static View3D ResolveExportView(Document document)
        {
            if (document.ActiveView is View3D activeView && !activeView.IsTemplate)
            {
                return activeView;
            }

            return new FilteredElementCollector(document)
                .OfClass(typeof(View3D))
                .Cast<View3D>()
                .FirstOrDefault(view => !view.IsTemplate);
        }

        private static string BuildSafeFileName(string name)
        {
            var invalid = Path.GetInvalidFileNameChars();
            var safe = new string(name.Where(ch => !invalid.Contains(ch)).ToArray());
            return string.IsNullOrWhiteSpace(safe) ? "bimto3dprint_export" : safe;
        }

        private static bool PresetUsesRevitCategories(string presetName)
        {
            try
            {
                var baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
                var presetDirectory = Path.Combine(baseDirectory, "Config", "Presets", "Revit");
                var presetPath = Path.Combine(presetDirectory, $"{presetName}.json");
                if (!File.Exists(presetPath))
                {
                    return false;
                }

                var content = File.ReadAllText(presetPath);
                return content.Contains("BuiltInCategory.", StringComparison.Ordinal);
            }
            catch (Exception ex)
            {
                Logger.Warn($"Failed to inspect preset categories: {ex.Message}");
                return false;
            }
        }

        private sealed class ProgressDialog : Window, IDisposable
        {
            public ProgressDialog(string title)
            {
                Title = title;
                Width = 360;
                Height = 140;
                WindowStartupLocation = WindowStartupLocation.CenterScreen;
                ResizeMode = ResizeMode.NoResize;
                Content = BuildContent();
            }

            public void Dispose()
            {
                Close();
            }

            private static UIElement BuildContent()
            {
                var panel = new StackPanel { Margin = new Thickness(16), Orientation = Orientation.Vertical };
                panel.Children.Add(new TextBlock
                {
                    Text = "Exporting IFC file from Revit...",
                    Margin = new Thickness(0, 0, 0, 8)
                });
                panel.Children.Add(new ProgressBar
                {
                    IsIndeterminate = true,
                    Height = 18
                });
                return panel;
            }
        }
    }
}
