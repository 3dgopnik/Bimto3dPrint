using Autodesk.Revit.DB;

namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Settings for IFC export.
    /// </summary>
    public class IfcExportSettings
    {
        /// <summary>
        /// IFC schema version (IFC2x3/IFC4).
        /// </summary>
        public string IfcVersion { get; set; } = "IFC4";

        /// <summary>
        /// Gets or sets a value indicating whether to export base quantities.
        /// </summary>
        public bool ExportBaseQuantities { get; set; }

        /// <summary>
        /// Gets or sets a value indicating whether to use active view geometry.
        /// </summary>
        public bool UseActiveViewGeometry { get; set; } = true;

        /// <summary>
        /// Gets or sets a value indicating whether to export linked files.
        /// </summary>
        public bool ExportLinkedFiles { get; set; }

        /// <summary>
        /// Gets or sets the view id used for IFC export.
        /// </summary>
        public ElementId FilterViewId { get; set; } = ElementId.InvalidElementId;
    }
}
