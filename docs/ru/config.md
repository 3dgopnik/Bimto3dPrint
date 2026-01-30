# Конфигурация

## category_filters.json (проектный шаблон)

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

## Примечания
- Категории должны соответствовать `BuiltInCategory`.
- `conditional_include` требует доп. фильтров по параметрам/геометрии.
- Извлечённая оболочка автоматически приводится к миллиметрам; решение по единицам фиксируется в логах.

## Схемы и пресеты
- Схемы: `Config/Schemas/category_filter_schema.json`, `Config/Schemas/export_settings_schema.json`.
- Пресеты: `Config/Presets/` (shell_only, shell_with_structure, full_exterior, simple_box).

## Настройка TU Delft IfcEnvelopeExtractor

При использовании CLI можно добавить блок `tudelft_extractor` в конфигурацию:

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

Опция `extractor_path` должна указывать на exe, соответствующий схеме IFC (IFC2x3 / IFC4 / IFC4x3).

## Управление утолщением стен

Параметры утолщения управляются через CLI:

- `--min-wall-mm` — минимальная толщина стен (мм).
- `--no-thicken` — полностью отключить утолщение.
