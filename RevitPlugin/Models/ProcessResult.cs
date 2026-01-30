namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Represents the result of a Python processing call.
    /// </summary>
    public class ProcessResult
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="ProcessResult"/> class.
        /// </summary>
        public ProcessResult(bool success, bool cancelled, int exitCode, string outputPath, string standardOutput, string standardError, string message)
        {
            Success = success;
            Cancelled = cancelled;
            ExitCode = exitCode;
            OutputPath = outputPath ?? string.Empty;
            StandardOutput = standardOutput ?? string.Empty;
            StandardError = standardError ?? string.Empty;
            Message = message ?? string.Empty;
        }

        /// <summary>
        /// Gets a value indicating whether processing succeeded.
        /// </summary>
        public bool Success { get; }

        /// <summary>
        /// Gets a value indicating whether processing was cancelled by the user.
        /// </summary>
        public bool Cancelled { get; }

        /// <summary>
        /// Gets the process exit code.
        /// </summary>
        public int ExitCode { get; }

        /// <summary>
        /// Gets the output file path.
        /// </summary>
        public string OutputPath { get; }

        /// <summary>
        /// Gets the captured standard output.
        /// </summary>
        public string StandardOutput { get; }

        /// <summary>
        /// Gets the captured standard error.
        /// </summary>
        public string StandardError { get; }

        /// <summary>
        /// Gets the user-facing message.
        /// </summary>
        public string Message { get; }
    }
}
