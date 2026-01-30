using System;
using System.IO;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.IFC;
using Bimto3dPrint.Models;
using Bimto3dPrint.Utils;

namespace Bimto3dPrint.Services
{
    /// <summary>
    /// Service for exporting IFC files from Revit.
    /// </summary>
    public class IfcExportService
    {
        /// <summary>
        /// Export an IFC file using the provided settings.
        /// </summary>
        public string ExportIfc(Document document, string outputDir, string fileName, IfcExportSettings settings)
        {
            if (document == null)
            {
                throw new ArgumentNullException(nameof(document));
            }

            if (string.IsNullOrWhiteSpace(outputDir))
            {
                throw new ArgumentException("Output directory is required.", nameof(outputDir));
            }

            Directory.CreateDirectory(outputDir);

            var options = new IFCExportOptions
            {
                FileVersion = ResolveIfcVersion(settings.IfcVersion),
                ExportBaseQuantities = settings.ExportBaseQuantities,
                FilterViewId = settings.FilterViewId
            };

            options.AddOption("UseActiveViewGeometry", settings.UseActiveViewGeometry ? "true" : "false");
            options.AddOption("ExportLinkedFiles", settings.ExportLinkedFiles ? "true" : "false");
            options.AddOption("SpaceBoundaries", "0");
            options.AddOption("ExportInternalRevitPropertySets", "false");

            Logger.Info($"Exporting IFC to {outputDir} with file name {fileName}");
            Logger.Info($"IFC version: {settings.IfcVersion}");

            var success = document.Export(outputDir, fileName, options);
            if (!success)
            {
                Logger.Error("Revit IFC export returned failure.");
                throw new InvalidOperationException("Revit IFC export failed.");
            }

            var ifcPath = Path.Combine(outputDir, $"{fileName}.ifc");
            Logger.Info($"IFC export completed: {ifcPath}");
            return ifcPath;
        }

        private static IFCVersion ResolveIfcVersion(string version)
        {
            if (string.IsNullOrWhiteSpace(version))
            {
                return IFCVersion.IFC4;
            }

            var normalized = version.Trim().ToUpperInvariant();
            if (normalized == "IFC2X3" || normalized == "IFC2X3CV2")
            {
                return IFCVersion.IFC2x3CV2;
            }

            return IFCVersion.IFC4;
        }
    }
}
