using Autodesk.Revit.UI;

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
            // TODO: Load configuration and run export services.
            return Result.Succeeded;
        }
    }
}
