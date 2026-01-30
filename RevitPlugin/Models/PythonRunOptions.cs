namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Options for running the Python pipeline.
    /// </summary>
    public class PythonRunOptions
    {
        /// <summary>
        /// Gets or sets the minimum wall thickness in millimeters.
        /// </summary>
        public double MinWallMm { get; set; } = 2.0;

        /// <summary>
        /// Gets or sets a value indicating whether to skip wall thickening.
        /// </summary>
        public bool NoThicken { get; set; }
    }
}
