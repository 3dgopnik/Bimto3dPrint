# Bimto3dPrint

Цель проекта — автоматизированное извлечение **только внешней архитектурной оболочки** из Revit, подготовка её для 3D печати (Bambu Lab H2S) и экспорт в 3ds Max.

## Текущий пайплайн
- Поддерживается внешний движок TU Delft IfcEnvelopeExtractor (через CLI `bimto3dprint process`).
- После получения оболочки выполняется watertight‑ремонт, утолщение, сглаживание и валидация перед экспортом.
- Экспорт доступен в STL/OBJ/FBX.

## Этап 0: анализ структуры Revit и перечень категорий

### Типичная структура Revit-проекта
- **Дисциплины**: Architecture, Structure, MEP (HVAC/Plumbing/Electrical), Site.
- **Основные виды**: планы этажей, фасады, разрезы, 3D виды.
- **Группы элементов**: ограждающие конструкции (стены/кровли/перекрытия), инженерные системы, мебель/оборудование, аннотации и вспомогательные элементы.

### Категории для фильтрации (Built-in Categories)
Ниже — базовый список категорий для фильтрации. Он служит отправной точкой и должен уточняться под конкретный проект.

#### Всегда включать (архитектурная оболочка)
- **Стены**: `OST_Walls` (только наружные).
- **Крыши**: `OST_Roofs`.
- **Перекрытия**: `OST_Floors` (только верхнее и нижнее).
- **Витражные системы**: `OST_CurtainWallPanels`, `OST_CurtainWallMullions`.
- **Колонны**: `OST_StructuralColumns` (только внешние).
- **Основание**: `OST_BuildingPad`.
- **Пандусы**: `OST_Ramps` (если внешние).
- **Лестницы**: `OST_Stairs`, `OST_StairsRuns`, `OST_StairsLandings` (если внешние).

#### Условно включать (по параметрам/геометрии)
- **Ограждения**: `OST_Railings` (только внешние).
- **Двери**: `OST_Doors` (опционально, можно закрывать проёмы).
- **Окна**: `OST_Windows` (опционально, можно закрывать проёмы).
- **Ген. модели**: `OST_GenericModel` (только по параметрам, если используется для фасада).
- **Плиты/фундаменты**: `OST_StructuralFoundation` (если участвуют во внешнем контуре).

#### Всегда исключать (интерьеры, инженерия, аннотации)
**Интерьеры и оборудование**
- `OST_Furniture`, `OST_FurnitureSystems`, `OST_Casework`, `OST_SpecialityEquipment`.

**MEP / инженерные системы**
- `OST_MechanicalEquipment`, `OST_DuctCurves`, `OST_DuctFitting`, `OST_DuctAccessories`, `OST_DuctTerminal`.
- `OST_PipeCurves`, `OST_PipeFitting`, `OST_PipeAccessories`.
- `OST_CableTray`, `OST_CableTrayFitting`, `OST_Conduit`, `OST_ConduitFitting`.
- `OST_ElectricalEquipment`, `OST_ElectricalFixtures`, `OST_LightingFixtures`.
- `OST_PlumbingFixtures`, `OST_Sprinklers`.

**Аннотации и служебные элементы**
- `OST_Levels`, `OST_Grids`, `OST_Rooms`, `OST_Areas`, `OST_Spaces`.
- `OST_Dimensions`, `OST_TextNotes`, `OST_GenericAnnotation`, `OST_Tags`.

**Прочее**
- `OST_Topography` (если не требуется рельеф).
- `OST_Entourage`, `OST_Planting`.

### Рекомендации по определению внешних элементов
- **Параметры**: `Wall.Function == Exterior`, параметры несущей/наружной стены.
- **Геометрия**: проверка близости к внешнему bounding box здания.
- **Связь со средой**: элементы, контактирующие с внешним пространством.

## Документация
- [Быстрый старт](quickstart.md)
- [CLI](cli.md)
- [Конфигурация](config.md)
- [Troubleshooting](troubleshooting.md)
- [Справочник Built-In категорий](reference/revit_builtin_categories.md)
- [Руководство пользователя](user_guide.md)
