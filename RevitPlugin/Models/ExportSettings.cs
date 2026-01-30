namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Export settings model.
    /// </summary>
    public class ExportSettings
    {
        /// <summary>
        /// IFC file name.
        /// </summary>
        public string FileName { get; set; } = string.Empty;

        /// <summary>
        /// IFC version.
        /// </summary>
        public string IfcVersion { get; set; } = "IFC4";

        /// <summary>
        /// Output format (stl/obj/fbx).
        /// </summary>
        public string OutputFormat { get; set; } = "stl";
    }
}
