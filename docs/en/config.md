# Configuration

## category_filters.json (project template)

```json
{
  "export_categories": {
    "always_include": [
      "OST_Walls",
      "OST_Roofs",
      "OST_Floors"
    ],
    "conditional_include": [
      "OST_CurtainWallPanels",
      "OST_CurtainWallMullions",
      "OST_StructuralColumns",
      "OST_BuildingPad",
      "OST_Ramps",
      "OST_Stairs"
    ],
    "always_exclude": [
      "OST_Furniture",
      "OST_FurnitureSystems",
      "OST_Casework",
      "OST_MechanicalEquipment",
      "OST_ElectricalFixtures",
      "OST_PlumbingFixtures",
      "OST_LightingFixtures",
      "OST_GenericModel"
    ]
  },
  "wall_filters": {
    "only_exterior": true,
    "only_structural": false,
    "min_thickness_mm": 100
  },
  "opening_handling": {
    "close_windows": true,
    "close_doors": true,
    "fill_method": "solid"
  },
  "geometry_simplification": {
    "enabled": true,
    "detail_level": "medium",
    "merge_coplanar": true,
    "remove_details_smaller_than_mm": 50
  }
}
```

## Notes
- Categories must match `BuiltInCategory`.
- `conditional_include` requires additional parameter/geometry filters.
- Extracted envelopes are automatically normalized to millimeters; unit decisions are logged.

## Schemas and presets
- Schemas: `Config/Schemas/category_filter_schema.json`, `Config/Schemas/export_settings_schema.json`.
- Presets: `Config/Presets/` (shell_only, shell_with_structure, full_exterior, simple_box).

## TU Delft IfcEnvelopeExtractor settings

When using the CLI you can add a `tudelft_extractor` block to the configuration:

```json
{
  "tudelft_extractor": {
    "extractor_path": "/path/Ifc_Envelope_Extractor_ifc4.exe",
    "lod": 2.2,
    "voxel_size": 1.0,
    "threads": 8
  }
}
```

The `extractor_path` must point to the exe that matches the IFC schema (IFC2x3 / IFC4 / IFC4x3).

## Wall thickening control

Wall thickening is configured via CLI:

- `--min-wall-mm` — minimum wall thickness (mm).
- `--no-thicken` — disable thickening entirely.
