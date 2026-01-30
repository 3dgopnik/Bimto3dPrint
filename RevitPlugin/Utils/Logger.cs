using System;
using System.IO;

namespace Bimto3dPrint.Utils
{
    /// <summary>
    /// Simple file logger for the plugin.
    /// </summary>
    public static class Logger
    {
        private static readonly string LogDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs");
        private static readonly string LogFilePath = Path.Combine(LogDirectory, "bimto3dprint.log");

        /// <summary>
        /// Writes a log message.
        /// </summary>
        public static void Info(string message)
        {
            Write("INFO", message);
        }

        /// <summary>
        /// Writes a warning message.
        /// </summary>
        public static void Warn(string message)
        {
            Write("WARN", message);
        }

        /// <summary>
        /// Writes an error message.
        /// </summary>
        public static void Error(string message)
        {
            Write("ERROR", message);
        }

        private static void Write(string level, string message)
        {
            Directory.CreateDirectory(LogDirectory);
            var line = $"{DateTime.UtcNow:O} [{level}] {message}";
            File.AppendAllLines(LogFilePath, new[] { line });
        }
    }
}
