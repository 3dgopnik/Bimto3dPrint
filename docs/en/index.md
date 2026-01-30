# Bimto3dPrint

The project goal is to automatically extract **only the external architectural shell** from Revit, prepare it for 3D printing (Bambu Lab H2S), and export it to 3ds Max.

## Current pipeline
- Supports the TU Delft IfcEnvelopeExtractor as an external engine (via `bimto3dprint process`).
- After envelope extraction, units are normalized to millimeters, then the mesh is repaired (watertight), thickened, smoothed, and validated before export.
- STL/OBJ/FBX exports are available.

## Stage 0: Revit structure analysis and category list

### Typical Revit project structure
- **Disciplines**: Architecture, Structure, MEP (HVAC/Plumbing/Electrical), Site.
- **Views**: floor plans, elevations, sections, 3D views.
- **Element groups**: envelope elements (walls/roofs/floors), engineering systems, furniture/equipment, annotations and helpers.

### Filtering categories (Built-in Categories)
Below is the baseline category list for filtering. It should be refined per project.

#### Always include (architectural shell)
- **Walls**: `OST_Walls` (exterior only).
- **Roofs**: `OST_Roofs`.
- **Floors**: `OST_Floors` (top and bottom only).
- **Curtain systems**: `OST_CurtainWallPanels`, `OST_CurtainWallMullions`.
- **Columns**: `OST_StructuralColumns` (external only).
- **Building pad**: `OST_BuildingPad`.
- **Ramps**: `OST_Ramps` (external only).
- **Stairs**: `OST_Stairs`, `OST_StairsRuns`, `OST_StairsLandings` (external only).

#### Conditionally include (by parameters/geometry)
- **Railings**: `OST_Railings` (external only).
- **Doors**: `OST_Doors` (optional, can close openings).
- **Windows**: `OST_Windows` (optional, can close openings).
- **Generic models**: `OST_GenericModel` (by parameters if used on facades).
- **Foundations**: `OST_StructuralFoundation` (if part of the outer contour).

#### Always exclude (interiors, MEP, annotations)
**Interiors and equipment**
- `OST_Furniture`, `OST_FurnitureSystems`, `OST_Casework`, `OST_SpecialityEquipment`.

**MEP systems**
- `OST_MechanicalEquipment`, `OST_DuctCurves`, `OST_DuctFitting`, `OST_DuctAccessories`, `OST_DuctTerminal`.
- `OST_PipeCurves`, `OST_PipeFitting`, `OST_PipeAccessories`.
- `OST_CableTray`, `OST_CableTrayFitting`, `OST_Conduit`, `OST_ConduitFitting`.
- `OST_ElectricalEquipment`, `OST_ElectricalFixtures`, `OST_LightingFixtures`.
- `OST_PlumbingFixtures`, `OST_Sprinklers`.

**Annotations and helpers**
- `OST_Levels`, `OST_Grids`, `OST_Rooms`, `OST_Areas`, `OST_Spaces`.
- `OST_Dimensions`, `OST_TextNotes`, `OST_GenericAnnotation`, `OST_Tags`.

**Other**
- `OST_Topography` (if terrain is not required).
- `OST_Entourage`, `OST_Planting`.

### External element detection hints
- **Parameters**: `Wall.Function == Exterior`, structural/exterior parameters.
- **Geometry**: proximity to building bounding box.
- **Environment**: elements that interface with external spaces.

## Documentation
- [Quickstart](quickstart.md)
- [CLI](cli.md)
- [Configuration](config.md)
- [Troubleshooting](troubleshooting.md)
- [Built-In categories reference](reference/revit_builtin_categories.md)
- [User guide](user_guide.md)
