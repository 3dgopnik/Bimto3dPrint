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
- Category names must match `BuiltInCategory`.
- `conditional_include` requires parameter/geometry filters.

## Schemas and presets
- Schemas: `Config/Schemas/category_filter_schema.json`, `Config/Schemas/export_settings_schema.json`.
- Presets: `Config/Presets/` (shell_only, shell_with_structure, full_exterior, simple_box).
