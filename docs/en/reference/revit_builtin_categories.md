# Revit Built-In Categories (BuiltInCategory)

> List version: aligned with Revit API 2024. Re-check `BuiltInCategory` when upgrading Revit.

## How to read the table
- **Enum** — Revit API category name (`BuiltInCategory.*`).
- **Description** — short purpose.
- **Recommendation** — include/exclude for building shell.
- **Examples** — typical elements.

## Architectural
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Walls | Walls | Include | Exterior/interior walls |
| BuiltInCategory.OST_CurtainWallPanels | Curtain wall panels | Include | Curtain wall panels |
| BuiltInCategory.OST_CurtainWallMullions | Curtain wall mullions | Include | Mullions |
| BuiltInCategory.OST_Roofs | Roofs | Include | Pitched/flat roofs |
| BuiltInCategory.OST_Floors | Floors | Include | Floor slabs |
| BuiltInCategory.OST_Ceilings | Ceilings | Exclude | Suspended ceilings |
| BuiltInCategory.OST_Stairs | Stairs | Optional | Interior stairs |
| BuiltInCategory.OST_Ramps | Ramps | Optional | Access ramps |
| BuiltInCategory.OST_Doors | Doors | Optional | Entry/interior |
| BuiltInCategory.OST_Windows | Windows | Optional | Window assemblies |
| BuiltInCategory.OST_Railings | Railings | Optional | Handrails |
| BuiltInCategory.OST_StairsRailing | Stair railings | Optional | Railings |
| BuiltInCategory.OST_StairsRuns | Stair runs | Optional | Runs |
| BuiltInCategory.OST_StairsLandings | Stair landings | Optional | Landings |
| BuiltInCategory.OST_StairsSupport | Stair supports | Optional | Stringers |
| BuiltInCategory.OST_Fascias | Fascias | Optional | Fascia |
| BuiltInCategory.OST_Gutters | Gutters | Optional | Gutters |
| BuiltInCategory.OST_Downspouts | Downspouts | Optional | Downspouts |
| BuiltInCategory.OST_Soffits | Soffits | Optional | Soffits |
| BuiltInCategory.OST_CurtainGrids | Curtain grids | Exclude | Grids |
| BuiltInCategory.OST_ExteriorLighting | Exterior lighting | Exclude | Site lighting |
| BuiltInCategory.OST_Site | Site | Optional | Site context |
| BuiltInCategory.OST_Topography | Topography | Optional | Toposurface |
| BuiltInCategory.OST_Toposolid | Toposolid | Optional | Toposolid |
| BuiltInCategory.OST_Parking | Parking | Optional | Parking areas |
| BuiltInCategory.OST_BuildingPads | Building pads | Optional | Pads |
| BuiltInCategory.OST_Entourage | Entourage | Exclude | People/vehicles |
| BuiltInCategory.OST_GenericModel | Generic models | Optional | Shell elements |
| BuiltInCategory.OST_Mass | Mass | Optional | Conceptual mass |
| BuiltInCategory.OST_AdaptiveComponents | Adaptive components | Optional | Facade elements |
| BuiltInCategory.OST_Casework | Casework | Exclude | Cabinets |
| BuiltInCategory.OST_Furniture | Furniture | Exclude | Chairs |
| BuiltInCategory.OST_SpecialityEquipment | Specialty equipment | Exclude | Elevators |
| BuiltInCategory.OST_Plants | Plants | Exclude | Trees |
| BuiltInCategory.OST_SiteProperty | Site property | Exclude | Site property |
| BuiltInCategory.OST_Parts | Parts | Exclude | Parts |
| BuiltInCategory.OST_Rooms | Rooms | Exclude | Room volumes |
| BuiltInCategory.OST_Areas | Areas | Exclude | Areas |
| BuiltInCategory.OST_Spaces | Spaces | Exclude | MEP spaces |

## Structural
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_StructuralColumns | Structural columns | Include | Concrete/steel columns |
| BuiltInCategory.OST_StructuralFraming | Framing | Include | Beams |
| BuiltInCategory.OST_StructuralFoundation | Foundations | Optional | Slab/strip |
| BuiltInCategory.OST_StructuralStiffener | Stiffeners | Exclude | Stiffeners |
| BuiltInCategory.OST_StructuralRebar | Rebar | Exclude | Rebar |
| BuiltInCategory.OST_StructuralPathReinforcement | Path reinforcement | Exclude | Reinforcement |
| BuiltInCategory.OST_StructuralFabricReinforcement | Fabric reinforcement | Exclude | Fabric |
| BuiltInCategory.OST_StructuralTrusses | Trusses | Optional | Trusses |
| BuiltInCategory.OST_StructuralConnections | Connections | Exclude | Connections |
| BuiltInCategory.OST_StructuralBrace | Braces | Optional | Braces |
| BuiltInCategory.OST_StructuralPile | Piles | Optional | Piles |
| BuiltInCategory.OST_StructuralWall | Structural walls | Include | Shear walls |
| BuiltInCategory.OST_StructuralFloor | Structural floors | Include | Structural floors |
| BuiltInCategory.OST_StructuralFoundationSlab | Foundation slabs | Optional | Slab |

## MEP
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_PipeCurves | Pipes | Exclude | Plumbing pipes |
| BuiltInCategory.OST_PipeFitting | Pipe fittings | Exclude | Elbows |
| BuiltInCategory.OST_PipeAccessory | Pipe accessories | Exclude | Valves |
| BuiltInCategory.OST_PipeInsulations | Pipe insulation | Exclude | Insulation |
| BuiltInCategory.OST_DuctCurves | Ducts | Exclude | Ducts |
| BuiltInCategory.OST_DuctFitting | Duct fittings | Exclude | Fittings |
| BuiltInCategory.OST_DuctAccessory | Duct accessories | Exclude | Dampers |
| BuiltInCategory.OST_DuctInsulations | Duct insulation | Exclude | Insulation |
| BuiltInCategory.OST_CableTray | Cable trays | Exclude | Cable trays |
| BuiltInCategory.OST_CableTrayFitting | Cable tray fittings | Exclude | Tray fittings |
| BuiltInCategory.OST_Conduit | Conduits | Exclude | Conduits |
| BuiltInCategory.OST_ConduitFitting | Conduit fittings | Exclude | Conduit fittings |
| BuiltInCategory.OST_ElectricalEquipment | Electrical equipment | Exclude | Panels |
| BuiltInCategory.OST_ElectricalFixtures | Electrical fixtures | Exclude | Switches |
| BuiltInCategory.OST_LightingFixtures | Lighting fixtures | Exclude | Lighting |
| BuiltInCategory.OST_LightingDevices | Lighting devices | Exclude | Devices |
| BuiltInCategory.OST_MechanicalEquipment | Mechanical equipment | Exclude | AHU |
| BuiltInCategory.OST_PlumbingFixtures | Plumbing fixtures | Exclude | Sinks |
| BuiltInCategory.OST_Sprinklers | Sprinklers | Exclude | Sprinklers |
| BuiltInCategory.OST_FireAlarmDevices | Fire alarm devices | Exclude | Fire alarm |
| BuiltInCategory.OST_SecurityDevices | Security devices | Exclude | Security |
| BuiltInCategory.OST_DataDevices | Data devices | Exclude | Data |
| BuiltInCategory.OST_TelephoneDevices | Telephone devices | Exclude | Telephone |
| BuiltInCategory.OST_CommunicationDevices | Communication devices | Exclude | Communication |
| BuiltInCategory.OST_NurseCallDevices | Nurse call devices | Exclude | Nurse call |
| BuiltInCategory.OST_VacuumEquipment | Vacuum equipment | Exclude | Vacuum |
| BuiltInCategory.OST_DuctTerminal | Duct terminals | Exclude | Diffusers |
| BuiltInCategory.OST_PipeMechanicalEquipment | Pipe mechanical equipment | Exclude | Pumps |
| BuiltInCategory.OST_ElectricalCircuit | Electrical circuits | Exclude | Circuits |
| BuiltInCategory.OST_PipingSystem | Piping systems | Exclude | Systems |
| BuiltInCategory.OST_DuctSystem | Duct systems | Exclude | Systems |
| BuiltInCategory.OST_HVAC_Zones | HVAC zones | Exclude | Zones |
| BuiltInCategory.OST_EnergyAnalysisSurfaces | Energy analysis surfaces | Exclude | Energy surfaces |

## Furniture & Fixtures
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Furniture | Furniture | Exclude | Tables |
| BuiltInCategory.OST_FurnitureSystems | Furniture systems | Exclude | Workstations |
| BuiltInCategory.OST_Casework | Casework | Exclude | Cabinets |
| BuiltInCategory.OST_SpecialityEquipment | Specialty equipment | Exclude | Elevator equipment |
| BuiltInCategory.OST_PlumbingFixtures | Plumbing fixtures | Exclude | Toilets |
| BuiltInCategory.OST_LightingFixtures | Lighting fixtures | Exclude | Fixtures |
| BuiltInCategory.OST_LightingDevices | Lighting devices | Exclude | Devices |
| BuiltInCategory.OST_ElectricalFixtures | Electrical fixtures | Exclude | Receptacles |
| BuiltInCategory.OST_MechanicalEquipment | Mechanical equipment | Exclude | Chillers |
| BuiltInCategory.OST_FoodServiceEquipment | Food service equipment | Exclude | Kitchen equipment |
| BuiltInCategory.OST_MedicalEquipment | Medical equipment | Exclude | Medical |
| BuiltInCategory.OST_SecurityDevices | Security devices | Exclude | Sensors |
| BuiltInCategory.OST_TelephoneDevices | Telephone devices | Exclude | Phones |

## Annotations & Service
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Levels | Levels | Exclude | Levels |
| BuiltInCategory.OST_Grids | Grids | Exclude | Grids |
| BuiltInCategory.OST_ReferencePlanes | Reference planes | Exclude | Reference planes |
| BuiltInCategory.OST_ReferenceLines | Reference lines | Exclude | Reference lines |
| BuiltInCategory.OST_Dimensions | Dimensions | Exclude | Dimensions |
| BuiltInCategory.OST_TextNotes | Text notes | Exclude | Notes |
| BuiltInCategory.OST_Tags | Tags | Exclude | Tags |
| BuiltInCategory.OST_GenericAnnotation | Generic annotation | Exclude | Annotation |
| BuiltInCategory.OST_RevisionClouds | Revision clouds | Exclude | Revision clouds |
| BuiltInCategory.OST_TitleBlocks | Title blocks | Exclude | Title blocks |
| BuiltInCategory.OST_Viewports | Viewports | Exclude | Viewports |
| BuiltInCategory.OST_Views | Views | Exclude | Views |
| BuiltInCategory.OST_Sheets | Sheets | Exclude | Sheets |
| BuiltInCategory.OST_DetailComponents | Detail components | Exclude | Detail components |
| BuiltInCategory.OST_Lines | Lines | Exclude | Lines |
| BuiltInCategory.OST_Cameras | Cameras | Exclude | Cameras |
| BuiltInCategory.OST_RenderRegions | Render regions | Exclude | Render region |
| BuiltInCategory.OST_Schedules | Schedules | Exclude | Schedules |
| BuiltInCategory.OST_ViewportLabel | Viewport labels | Exclude | Viewport labels |
| BuiltInCategory.OST_ImportedCategories | Imported categories | Exclude | DWG imports |
| BuiltInCategory.OST_RvtLinks | Revit links | Exclude | Revit links |
| BuiltInCategory.OST_LinkAnalytical | Analytical links | Exclude | Analytical links |
| BuiltInCategory.OST_RoomTags | Room tags | Exclude | Room tags |
| BuiltInCategory.OST_AreaTags | Area tags | Exclude | Area tags |
| BuiltInCategory.OST_SpaceTags | Space tags | Exclude | Space tags |
| BuiltInCategory.OST_SpotElevations | Spot elevations | Exclude | Spot elevations |
| BuiltInCategory.OST_SpotCoordinates | Spot coordinates | Exclude | Spot coordinates |
| BuiltInCategory.OST_SpotSlopes | Spot slopes | Exclude | Spot slopes |

## Other shell-related categories (optional)
| Enum | Description | Recommendation | Examples |
| --- | --- | --- | --- |
| BuiltInCategory.OST_CurtainSystems | Curtain systems | Include | Curtain systems |
| BuiltInCategory.OST_CurtainSystemPanels | Curtain system panels | Include | System panels |
| BuiltInCategory.OST_CurtainSystemMullions | Curtain system mullions | Include | System mullions |
| BuiltInCategory.OST_Partitions | Partitions | Optional | Partitions |
| BuiltInCategory.OST_Assemblies | Assemblies | Exclude | Assemblies |

## Sources
- Revit API Docs: BuiltInCategory enum
- Autodesk Revit API Developer Guide
- Communities: The Building Coder, Revit API Forum

## Shell filtering guidance
1. **Minimal shell**: walls, roofs, floors, curtain systems, structural elements.
2. **Optional**: stairs, ramps, railings, site.
3. **Exclude**: MEP, furniture, annotations, service categories.
