using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.Serialization.Json;
using System.Text;
using Bimto3dPrint.Models;
using Bimto3dPrint.Utils;

namespace Bimto3dPrint.Services
{
    /// <summary>
    /// Runs the Python processing pipeline.
    /// </summary>
    public class PythonRunner
    {
        private const string SettingsFileName = "bimto3dprint.settings.json";
        private readonly PythonRunnerSettings settings;

        /// <summary>
        /// Gets the last run log file path.
        /// </summary>
        public string LastLogPath { get; private set; } = string.Empty;

        /// <summary>
        /// Gets the loaded runner settings.
        /// </summary>
        public PythonRunnerSettings Settings => settings;

        /// <summary>
        /// Initializes a new instance of the <see cref="PythonRunner"/> class.
        /// </summary>
        public PythonRunner()
        {
            settings = LoadSettings();
        }

        /// <summary>
        /// Run the Python pipeline and return the process exit code.
        /// </summary>
        public int RunBimto3dPrint(string ifcPath, string presetName, string outputPath, string format, PythonRunOptions options)
        {
            if (string.IsNullOrWhiteSpace(ifcPath) || !File.Exists(ifcPath))
            {
                throw new FileNotFoundException("IFC file not found.", ifcPath);
            }

            if (string.IsNullOrWhiteSpace(outputPath))
            {
                throw new ArgumentException("Output path is required.", nameof(outputPath));
            }

            var executable = ResolveExecutable(settings);
            var arguments = BuildArguments(settings, ifcPath, presetName, outputPath, format, options, executable.isModule);

            Logger.Info($"Starting Python pipeline: {executable.path} {arguments}");

            var startInfo = new ProcessStartInfo
            {
                FileName = executable.path,
                Arguments = arguments,
                WorkingDirectory = Path.GetDirectoryName(ifcPath) ?? Environment.CurrentDirectory,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            if (!executable.isModule && !File.Exists(executable.path))
            {
                Logger.Error($"Configured bimto3dprint executable not found: {executable.path}");
                throw new FileNotFoundException("Configured bimto3dprint executable not found.", executable.path);
            }

            using (var process = new Process { StartInfo = startInfo })
            {
                var outputBuilder = new StringBuilder();
                var errorBuilder = new StringBuilder();

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

                if (!process.Start())
                {
                    Logger.Error("Failed to start Python pipeline process.");
                    return -1;
                }

                process.BeginOutputReadLine();
                process.BeginErrorReadLine();
                process.WaitForExit();

                var exitCode = process.ExitCode;
                SaveProcessLog(outputBuilder.ToString(), errorBuilder.ToString(), exitCode);

                Logger.Info($"Python pipeline completed with exit code {exitCode}.");
                return exitCode;
            }
        }

        private static PythonRunnerSettings LoadSettings()
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            var settingsPath = Path.Combine(baseDir, SettingsFileName);
            if (!File.Exists(settingsPath))
            {
                Logger.Warn($"Python settings file not found: {settingsPath}. Using defaults.");
                return new PythonRunnerSettings();
            }

            try
            {
                using (var stream = File.OpenRead(settingsPath))
                {
                    var serializer = new DataContractJsonSerializer(typeof(PythonRunnerSettings));
                    var data = serializer.ReadObject(stream) as PythonRunnerSettings;
                    return data ?? new PythonRunnerSettings();
                }
            }
            catch (Exception ex)
            {
                Logger.Warn($"Failed to load Python settings: {ex.Message}");
                return new PythonRunnerSettings();
            }
        }

        private static (string path, bool isModule) ResolveExecutable(PythonRunnerSettings settings)
        {
            if (!string.IsNullOrWhiteSpace(settings.Bimto3dprintExecutable))
            {
                return (settings.Bimto3dprintExecutable, false);
            }

            var configuredPython = settings.PythonExecutable;
            if (string.IsNullOrWhiteSpace(configuredPython))
            {
                configuredPython = Environment.GetEnvironmentVariable("BIMTO3DPRINT_PYTHON") ?? "python";
            }

            return (configuredPython, true);
        }

        private static string BuildArguments(
            PythonRunnerSettings settings,
            string ifcPath,
            string presetName,
            string outputPath,
            string format,
            PythonRunOptions options,
            bool useModule)
        {
            var builder = new StringBuilder();
            if (useModule)
            {
                builder.Append("-m ");
                builder.Append(string.IsNullOrWhiteSpace(settings.Bimto3dprintModule) ? "bimto3dprint.main" : settings.Bimto3dprintModule);
                builder.Append(' ');
            }

            builder.Append("process ");
            builder.Append(Escape(ifcPath));
            builder.Append(" --preset ");
            builder.Append(presetName);
            builder.Append(" --output ");
            builder.Append(Escape(outputPath));
            builder.Append(" --format ");
            builder.Append(format);

            if (options != null)
            {
                if (options.NoThicken)
                {
                    builder.Append(" --no-thicken");
                }
                else
                {
                    builder.Append(" --min-wall-mm ");
                    builder.Append(options.MinWallMm.ToString("F2", System.Globalization.CultureInfo.InvariantCulture));
                }
            }

            if (settings.UseTudelftExtractor)
            {
                builder.Append(" --use-tudelft-extractor");
                if (!string.IsNullOrWhiteSpace(settings.TudelftExtractorPath))
                {
                    builder.Append(" --extractor-path ");
                    builder.Append(Escape(settings.TudelftExtractorPath));
                }
            }

            return builder.ToString();
        }

        private static string Escape(string value)
        {
            return $"\"{value}\"";
        }

        private void SaveProcessLog(string standardOutput, string standardError, int exitCode)
        {
            var logDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs");
            Directory.CreateDirectory(logDirectory);

            var fileName = $"python_run_{DateTime.UtcNow:yyyyMMdd_HHmmss}.log";
            var logPath = Path.Combine(logDirectory, fileName);

            var builder = new StringBuilder();
            builder.AppendLine($"Exit code: {exitCode}");
            builder.AppendLine("--- STDOUT ---");
            builder.AppendLine(standardOutput);
            builder.AppendLine("--- STDERR ---");
            builder.AppendLine(standardError);

            File.WriteAllText(logPath, builder.ToString());
            LastLogPath = logPath;
            Logger.Info($"Python pipeline log saved: {logPath}");
        }
    }
}
