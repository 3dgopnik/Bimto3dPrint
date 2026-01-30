using System.Runtime.Serialization;

namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Settings for locating the Python pipeline executable.
    /// </summary>
    [DataContract]
    public class PythonRunnerSettings
    {
        /// <summary>
        /// Gets or sets the Python executable path.
        /// </summary>
        [DataMember(Name = "pythonExecutable")]
        public string PythonExecutable { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the standalone bimto3dprint executable path.
        /// </summary>
        [DataMember(Name = "bimto3dprintExecutable")]
        public string Bimto3dprintExecutable { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the module entry point for the pipeline.
        /// </summary>
        [DataMember(Name = "bimto3dprintModule")]
        public string Bimto3dprintModule { get; set; } = "bimto3dprint.main";

        /// <summary>
        /// Gets or sets a value indicating whether to use the TU Delft extractor.
        /// </summary>
        [DataMember(Name = "useTudelftExtractor")]
        public bool UseTudelftExtractor { get; set; }

        /// <summary>
        /// Gets or sets the TU Delft extractor path.
        /// </summary>
        [DataMember(Name = "tudelftExtractorPath")]
        public string TudelftExtractorPath { get; set; } = string.Empty;
    }
}
