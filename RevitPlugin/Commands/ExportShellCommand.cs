using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Interop;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.IFC;
using Autodesk.Revit.UI;
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

                var dialogResult = dialog.ShowDialog();
                if (dialogResult != true)
                {
                    Logger.Info("Export cancelled by user.");
                    return Result.Cancelled;
                }

                var preset = string.IsNullOrWhiteSpace(dialog.SelectedPreset) ? "shell_only" : dialog.SelectedPreset;
                var outputFormat = string.IsNullOrWhiteSpace(dialog.SelectedOutputFormat) ? "stl" : dialog.SelectedOutputFormat;

                var view3D = ResolveExportView(document);
                if (view3D == null)
                {
                    message = "No suitable 3D view found for export.";
                    Logger.Error(message);
                    TaskDialog.Show("Bimto3dPrint", message);
                    return Result.Failed;
                }

                var exportFolder = PrepareOutputFolder();
                var exportFileName = BuildSafeFileName(document.Title);
                var ifcPath = Path.Combine(exportFolder, $"{exportFileName}.ifc");

                Logger.Info($"Exporting IFC to {ifcPath}");

                using (var progress = new ProgressDialog("Exporting IFC..."))
                {
                    progress.Show();

                    var exportSucceeded = ExportIfc(document, view3D, exportFolder, exportFileName);
                    if (!exportSucceeded)
                    {
                        message = "IFC export failed. Please check Revit export settings.";
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

                var pythonBridge = new PythonBridgeService();
                var result = pythonBridge.CallPythonProcessor(ifcPath, preset, outputFormat);

                if (result.Cancelled)
                {
                    Logger.Warn("Python processing cancelled.");
                    TaskDialog.Show("Bimto3dPrint", "Python processing was cancelled.");
                    return Result.Cancelled;
                }

                if (!result.Success)
                {
                    var errorMessage = $"Python processing failed: {result.Message}";
                    Logger.Error(errorMessage);
                    TaskDialog.Show("Bimto3dPrint", errorMessage);
                    return Result.Failed;
                }

                var successMessage = $"Export completed. Output: {result.OutputPath}";
                Logger.Info(successMessage);
                TaskDialog.Show("Bimto3dPrint", successMessage);
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
                var presetDirectory = Path.Combine(baseDirectory, "Config", "Presets");
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

        private static string PrepareOutputFolder()
        {
            var exportFolder = Path.Combine(Path.GetTempPath(), "Bimto3dPrint");
            Directory.CreateDirectory(exportFolder);
            return exportFolder;
        }

        private static string BuildSafeFileName(string name)
        {
            var invalid = Path.GetInvalidFileNameChars();
            var safe = new string(name.Where(ch => !invalid.Contains(ch)).ToArray());
            return string.IsNullOrWhiteSpace(safe) ? "bimto3dprint_export" : safe;
        }

        private static bool ExportIfc(Document document, View3D view, string exportFolder, string fileName)
        {
            var options = new IFCExportOptions
            {
                FileVersion = IFCVersion.IFC4,
                FilterViewId = view.Id,
                ExportBaseQuantities = false
            };

            options.AddOption("SpaceBoundaries", "0");
            options.AddOption("ExportInternalRevitPropertySets", "false");

            return document.Export(exportFolder, fileName, options);
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
