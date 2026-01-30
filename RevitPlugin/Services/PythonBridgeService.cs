using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using Bimto3dPrint.Models;
using Bimto3dPrint.Utils;

namespace Bimto3dPrint.Services
{
    /// <summary>
    /// Bridges Revit plugin with the Python processor.
    /// </summary>
    public class PythonBridgeService
    {
        private const string DefaultModule = "bimto3dprint.main";

        /// <summary>
        /// Calls the Python processor to handle IFC data.
        /// </summary>
        public ProcessResult CallPythonProcessor(string ifcPath, string preset, string outputFormat)
        {
            if (string.IsNullOrWhiteSpace(ifcPath) || !File.Exists(ifcPath))
            {
                return new ProcessResult(false, false, -1, string.Empty, string.Empty, string.Empty, "IFC file does not exist.");
            }

            var sanitizedPreset = string.IsNullOrWhiteSpace(preset) ? "default" : preset;
            var sanitizedFormat = string.IsNullOrWhiteSpace(outputFormat) ? "stl" : outputFormat.ToLowerInvariant();
            var outputPath = BuildOutputPath(ifcPath, sanitizedFormat);
            var pythonExecutable = ResolvePythonExecutable();

            Logger.Info($"Python bridge using executable: {pythonExecutable}");
            Logger.Info($"Python output path: {outputPath}");

            var arguments = BuildArguments(ifcPath, sanitizedPreset, outputPath, sanitizedFormat);

            var startInfo = new ProcessStartInfo
            {
                FileName = pythonExecutable,
                Arguments = arguments,
                WorkingDirectory = Path.GetDirectoryName(ifcPath) ?? Environment.CurrentDirectory,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            var outputBuilder = new StringBuilder();
            var errorBuilder = new StringBuilder();

            using (var process = new Process { StartInfo = startInfo })
            using (var progressDialog = new ProgressDialog("Processing IFC with Python..."))
            {
                process.OutputDataReceived += (_, args) =>
                {
                    if (!string.IsNullOrWhiteSpace(args.Data))
                    {
                        outputBuilder.AppendLine(args.Data);
                    }
                };
                process.ErrorDataReceived += (_, args) =>
                {
                    if (!string.IsNullOrWhiteSpace(args.Data))
                    {
                        errorBuilder.AppendLine(args.Data);
                    }
                };

                try
                {
                    progressDialog.Show();

                    if (!process.Start())
                    {
                        Logger.Error("Failed to start Python process.");
                        return new ProcessResult(false, false, -1, outputPath, outputBuilder.ToString(), errorBuilder.ToString(), "Failed to start Python process.");
                    }

                    process.BeginOutputReadLine();
                    process.BeginErrorReadLine();

                    while (!process.HasExited)
                    {
                        if (progressDialog.IsCancellationRequested)
                        {
                            TryTerminate(process);
                            Logger.Warn("Python process cancelled by user.");
                            return new ProcessResult(false, true, -1, outputPath, outputBuilder.ToString(), errorBuilder.ToString(), "Processing was cancelled.");
                        }

                        progressDialog.Dispatcher.Invoke(DispatcherPriority.Background, new Action(() => { }));
                        Thread.Sleep(200);
                    }

                    var exitCode = process.ExitCode;
                    var succeeded = exitCode == 0;
                    var message = succeeded ? "Python processing completed successfully." : "Python processing failed.";

                    if (succeeded)
                    {
                        Logger.Info(message);
                    }
                    else
                    {
                        Logger.Error($"{message} Exit code: {exitCode}. Error: {errorBuilder}");
                    }

                    return new ProcessResult(succeeded, false, exitCode, outputPath, outputBuilder.ToString(), errorBuilder.ToString(), message);
                }
                catch (Exception ex)
                {
                    Logger.Error($"Python processing failed: {ex.Message}");
                    return new ProcessResult(false, false, -1, outputPath, outputBuilder.ToString(), errorBuilder.ToString(), ex.Message);
                }
                finally
                {
                    progressDialog.Close();
                }
            }
        }

        private static string ResolvePythonExecutable()
        {
            var configured = Environment.GetEnvironmentVariable("BIMTO3DPRINT_PYTHON");
            if (!string.IsNullOrWhiteSpace(configured) && File.Exists(configured))
            {
                return configured;
            }

            return "python";
        }

        private static string BuildArguments(string ifcPath, string preset, string outputPath, string outputFormat)
        {
            return $"-m {DefaultModule} process \"{ifcPath}\" --preset {preset} --output \"{outputPath}\" --format {outputFormat}";
        }

        private static string BuildOutputPath(string ifcPath, string outputFormat)
        {
            var extension = outputFormat.StartsWith(".", StringComparison.Ordinal) ? outputFormat : $".{outputFormat}";
            return Path.ChangeExtension(ifcPath, extension);
        }

        private static void TryTerminate(Process process)
        {
            try
            {
                if (!process.HasExited)
                {
                    process.Kill();
                }
            }
            catch (Exception ex)
            {
                Logger.Warn($"Failed to terminate Python process: {ex.Message}");
            }
        }

        private sealed class ProgressDialog : Window, IDisposable
        {
            public ProgressDialog(string title)
            {
                Title = title;
                Width = 420;
                Height = 160;
                WindowStartupLocation = WindowStartupLocation.CenterScreen;
                ResizeMode = ResizeMode.NoResize;
                Content = BuildContent();
            }

            public bool IsCancellationRequested { get; private set; }

            public void Dispose()
            {
                Close();
            }

            private UIElement BuildContent()
            {
                var panel = new StackPanel { Margin = new Thickness(16), Orientation = Orientation.Vertical };
                panel.Children.Add(new TextBlock
                {
                    Text = "Please wait while the Python processor completes.",
                    Margin = new Thickness(0, 0, 0, 8)
                });
                panel.Children.Add(new ProgressBar
                {
                    IsIndeterminate = true,
                    Height = 18,
                    Margin = new Thickness(0, 0, 0, 12)
                });

                var cancelButton = new Button { Content = "Cancel", Width = 90, HorizontalAlignment = HorizontalAlignment.Right };
                cancelButton.Click += (_, __) =>
                {
                    IsCancellationRequested = true;
                    cancelButton.IsEnabled = false;
                    cancelButton.Content = "Cancelling...";
                };

                panel.Children.Add(cancelButton);
                return panel;
            }
        }
    }
}
