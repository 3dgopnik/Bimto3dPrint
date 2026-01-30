# Built-In категории Revit (BuiltInCategory)

> Версия списка: ориентир по Revit API 2024. При обновлении Revit пересмотрите enum `BuiltInCategory`.

## Как читать таблицу
- **Enum** — имя категории в Revit API (`BuiltInCategory.*`).
- **Описание** — кратко по назначению.
- **Рекомендация** — включать/исключать для оболочки здания.
- **Примеры** — типовые элементы.

## Архитектурные
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Walls | Стены | Включать | Наружные/внутренние стены |
| BuiltInCategory.OST_CurtainWallPanels | Панели витражных стен | Включать | Curtain wall panels |
| BuiltInCategory.OST_CurtainWallMullions | Импосты витражных стен | Включать | Mullions |
| BuiltInCategory.OST_Roofs | Кровли | Включать | Скатные/плоские кровли |
| BuiltInCategory.OST_Floors | Перекрытия/полы | Включать | Плиты перекрытий |
| BuiltInCategory.OST_Ceilings | Потолки | Исключать | Подвесные потолки |
| BuiltInCategory.OST_Stairs | Лестницы | По необходимости | Внутренние лестницы |
| BuiltInCategory.OST_Ramps | Пандусы | По необходимости | Входные пандусы |
| BuiltInCategory.OST_Doors | Двери | По необходимости | Входные/межкомнатные |
| BuiltInCategory.OST_Windows | Окна | По необходимости | Оконные блоки |
| BuiltInCategory.OST_CurtainWallPanels | Панели витражей | Включать | Витражные панели |
| BuiltInCategory.OST_CurtainWallMullions | Импосты | Включать | Профили витражей |
| BuiltInCategory.OST_Railings | Ограждения | По необходимости | Перила |
| BuiltInCategory.OST_StairsRailing | Перила лестниц | По необходимости | Перила |
| BuiltInCategory.OST_StairsRuns | Марши лестниц | По необходимости | Лестничные марши |
| BuiltInCategory.OST_StairsLandings | Площадки лестниц | По необходимости | Площадки |
| BuiltInCategory.OST_StairsSupport | Опоры лестниц | По необходимости | Косоуры |
| BuiltInCategory.OST_Fascias | Карнизы | По необходимости | Фасции |
| BuiltInCategory.OST_Gutters | Водосточные желоба | По необходимости | Желоба |
| BuiltInCategory.OST_Downspouts | Водосточные трубы | По необходимости | Трубы |
| BuiltInCategory.OST_Soffits | Софиты | По необходимости | Подшивы |
| BuiltInCategory.OST_CurtainGrids | Сетки витражей | Исключать | Curtain grids |
| BuiltInCategory.OST_ExteriorLighting | Наружное освещение | Исключать | Фонари |
| BuiltInCategory.OST_Site | Участок | По необходимости | Рельеф |
| BuiltInCategory.OST_Topography | Топография | По необходимости | Поверхность участка |
| BuiltInCategory.OST_Toposolid | Топосолид | По необходимости | Твердотельный рельеф |
| BuiltInCategory.OST_Parking | Парковка | По необходимости | Разметка |
| BuiltInCategory.OST_BuildingPads | Подложки зданий | По необходимости | Building pads |
| BuiltInCategory.OST_Entourage | Окружение | Исключать | Люди/машины |
| BuiltInCategory.OST_GenericModel | Обобщенные модели | По необходимости | Элементы оболочки |
| BuiltInCategory.OST_Mass | Массы | По необходимости | Концептуальные массы |
| BuiltInCategory.OST_AdaptiveComponents | Адаптивные компоненты | По необходимости | Фасадные элементы |
| BuiltInCategory.OST_Casework | Шкафы/встроенная мебель | Исключать | Кухни |
| BuiltInCategory.OST_Furniture | Мебель | Исключать | Столы/стулья |
| BuiltInCategory.OST_SpecialityEquipment | Спецоборудование | Исключать | Лифтовое оборудование |
| BuiltInCategory.OST_Plants | Растения | Исключать | Деревья |
| BuiltInCategory.OST_SiteProperty | Свойства участка | Исключать | Site property |
| BuiltInCategory.OST_Parts | Части | Исключать | Parts |
| BuiltInCategory.OST_Rooms | Помещения | Исключать | Room volumes |
| BuiltInCategory.OST_Areas | Зоны | Исключать | Area plan |
| BuiltInCategory.OST_Spaces | Пространства | Исключать | MEP spaces |

## Конструктивные
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_StructuralColumns | Конструктивные колонны | Включать | Ж/б/стальные колонны |
| BuiltInCategory.OST_StructuralFraming | Балки/фермы | Включать | Балки |
| BuiltInCategory.OST_StructuralFoundation | Фундаменты | По необходимости | Плиты/ленты |
| BuiltInCategory.OST_StructuralStiffener | Жесткости | Исключать | Stiffeners |
| BuiltInCategory.OST_StructuralRebar | Арматура | Исключать | Rebar |
| BuiltInCategory.OST_StructuralPathReinforcement | Армирование пути | Исключать | Reinforcement |
| BuiltInCategory.OST_StructuralFabricReinforcement | Арматурная сетка | Исключать | Fabric |
| BuiltInCategory.OST_StructuralTrusses | Фермы | По необходимости | Trusses |
| BuiltInCategory.OST_StructuralConnections | Узлы соединений | Исключать | Connections |
| BuiltInCategory.OST_StructuralBrace | Раскосы | По необходимости | Braces |
| BuiltInCategory.OST_StructuralPile | Сваи | По необходимости | Piles |
| BuiltInCategory.OST_StructuralWall | Несущие стены | Включать | Shear walls |
| BuiltInCategory.OST_StructuralFloor | Несущие перекрытия | Включать | Structural floors |
| BuiltInCategory.OST_StructuralFoundationSlab | Фундаментные плиты | По необходимости | Slab |

## MEP — инженерные системы
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_PipeCurves | Трубы | Исключать | Plumbing pipes |
| BuiltInCategory.OST_PipeFitting | Фитинги труб | Исключать | Elbows |
| BuiltInCategory.OST_PipeAccessory | Арматура труб | Исключать | Valves |
| BuiltInCategory.OST_PipeInsulations | Изоляция труб | Исключать | Insulation |
| BuiltInCategory.OST_DuctCurves | Воздуховоды | Исключать | Ducts |
| BuiltInCategory.OST_DuctFitting | Фитинги воздуховодов | Исключать | Duct fittings |
| BuiltInCategory.OST_DuctAccessory | Арматура воздуховодов | Исключать | Dampers |
| BuiltInCategory.OST_DuctInsulations | Изоляция воздуховодов | Исключать | Duct insulation |
| BuiltInCategory.OST_CableTray | Кабельные лотки | Исключать | Cable trays |
| BuiltInCategory.OST_CableTrayFitting | Фитинги лотков | Исключать | Tray fittings |
| BuiltInCategory.OST_Conduit | Кабельные каналы | Исключать | Conduits |
| BuiltInCategory.OST_ConduitFitting | Фитинги каналов | Исключать | Conduit fittings |
| BuiltInCategory.OST_ElectricalEquipment | Электрооборудование | Исключать | Panels |
| BuiltInCategory.OST_ElectricalFixtures | Электроарматура | Исключать | Switches |
| BuiltInCategory.OST_LightingFixtures | Светильники | Исключать | Lighting |
| BuiltInCategory.OST_LightingDevices | Осветительные приборы | Исключать | Devices |
| BuiltInCategory.OST_MechanicalEquipment | Мехоборудование | Исключать | AHU |
| BuiltInCategory.OST_PlumbingFixtures | Сантехника | Исключать | Sinks |
| BuiltInCategory.OST_Sprinklers | Спринклеры | Исключать | Sprinklers |
| BuiltInCategory.OST_FireAlarmDevices | Пожарные датчики | Исключать | Fire alarm |
| BuiltInCategory.OST_SecurityDevices | Охранные устройства | Исключать | Security |
| BuiltInCategory.OST_DataDevices | Слаботочные устройства | Исключать | Data devices |
| BuiltInCategory.OST_TelephoneDevices | Телефонные устройства | Исключать | Telephone |
| BuiltInCategory.OST_CommunicationDevices | Коммуникации | Исключать | Communication |
| BuiltInCategory.OST_NurseCallDevices | Вызов персонала | Исключать | Nurse call |
| BuiltInCategory.OST_VacuumEquipment | Вакуумное оборудование | Исключать | Vacuum |
| BuiltInCategory.OST_DuctTerminal | Воздухораспределители | Исключать | Diffusers |
| BuiltInCategory.OST_PipeMechanicalEquipment | Трубное мехоборудование | Исключать | Pumps |
| BuiltInCategory.OST_ElectricalCircuit | Электрические цепи | Исключать | Circuits |
| BuiltInCategory.OST_PipingSystem | Системы трубопроводов | Исключать | Piping system |
| BuiltInCategory.OST_DuctSystem | Системы воздуховодов | Исключать | Duct system |
| BuiltInCategory.OST_HVAC_Zones | HVAC зоны | Исключать | Zones |
| BuiltInCategory.OST_EnergyAnalysisSurfaces | Поверхности энергоанализа | Исключать | Energy surfaces |

## Мебель и оборудование
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Furniture | Мебель | Исключать | Столы |
| BuiltInCategory.OST_FurnitureSystems | Мебельные системы | Исключать | Workstations |
| BuiltInCategory.OST_Casework | Встроенная мебель | Исключать | Шкафы |
| BuiltInCategory.OST_SpecialityEquipment | Спецоборудование | Исключать | Лифтовое |
| BuiltInCategory.OST_PlumbingFixtures | Сантехника | Исключать | Унитазы |
| BuiltInCategory.OST_LightingFixtures | Светильники | Исключать | Люстры |
| BuiltInCategory.OST_LightingDevices | Осветительные приборы | Исключать | Devices |
| BuiltInCategory.OST_ElectricalFixtures | Электроарматура | Исключать | Розетки |
| BuiltInCategory.OST_MechanicalEquipment | Мехоборудование | Исключать | Чиллеры |
| BuiltInCategory.OST_FoodServiceEquipment | Пищевое оборудование | Исключать | Кухни |
| BuiltInCategory.OST_MedicalEquipment | Медоборудование | Исключать | Hospital |
| BuiltInCategory.OST_SecurityDevices | Охранные устройства | Исключать | Sensors |
| BuiltInCategory.OST_TelephoneDevices | Телефония | Исключать | Phones |

## Аннотации и служебные
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Levels | Уровни | Исключать | Levels |
| BuiltInCategory.OST_Grids | Оси | Исключать | Grids |
| BuiltInCategory.OST_ReferencePlanes | Опорные плоскости | Исключать | Reference planes |
| BuiltInCategory.OST_ReferenceLines | Опорные линии | Исключать | Reference lines |
| BuiltInCategory.OST_Dimensions | Размеры | Исключать | Dimensions |
| BuiltInCategory.OST_TextNotes | Текстовые примечания | Исключать | Text notes |
| BuiltInCategory.OST_Tags | Марки | Исключать | Tags |
| BuiltInCategory.OST_GenericAnnotation | Аннотации | Исключать | Generic annotation |
| BuiltInCategory.OST_RevisionClouds | Облака изменений | Исключать | Revision clouds |
| BuiltInCategory.OST_TitleBlocks | Штампы | Исключать | Title blocks |
| BuiltInCategory.OST_Viewports | Видовые экраны | Исключать | Viewports |
| BuiltInCategory.OST_Views | Виды | Исключать | Views |
| BuiltInCategory.OST_Sheets | Листы | Исключать | Sheets |
| BuiltInCategory.OST_DetailComponents | Узлы/детали | Исключать | Detail components |
| BuiltInCategory.OST_Lines | Линии | Исключать | Lines |
| BuiltInCategory.OST_Cameras | Камеры | Исключать | Cameras |
| BuiltInCategory.OST_RenderRegions | Области рендера | Исключать | Render region |
| BuiltInCategory.OST_Schedules | Спецификации | Исключать | Schedules |
| BuiltInCategory.OST_ViewportLabel | Подписи видов | Исключать | Viewport label |
| BuiltInCategory.OST_ImportedCategories | Импортированные категории | Исключать | DWG imports |
| BuiltInCategory.OST_RvtLinks | Связи Revit | Исключать | Revit links |
| BuiltInCategory.OST_LinkAnalytical | Связи аналитики | Исключать | Analytical links |
| BuiltInCategory.OST_RoomTags | Марки помещений | Исключать | Room tags |
| BuiltInCategory.OST_AreaTags | Марки зон | Исключать | Area tags |
| BuiltInCategory.OST_SpaceTags | Марки пространств | Исключать | Space tags |
| BuiltInCategory.OST_SpotElevations | Отметки высот | Исключать | Spot elevations |
| BuiltInCategory.OST_SpotCoordinates | Координаты | Исключать | Spot coordinates |
| BuiltInCategory.OST_SpotSlopes | Уклоны | Исключать | Spot slopes |

## Прочие категории оболочки (по необходимости)
| Enum | Описание | Рекомендация | Примеры |
| --- | --- | --- | --- |
| BuiltInCategory.OST_Site | Участок | По необходимости | Site |
| BuiltInCategory.OST_Topography | Топография | По необходимости | Toposurface |
| BuiltInCategory.OST_Toposolid | Топосолид | По необходимости | Toposolid |
| BuiltInCategory.OST_Parking | Парковка | По необходимости | Parking |
| BuiltInCategory.OST_GenericModel | Обобщенные модели | По необходимости | Generic models |
| BuiltInCategory.OST_Mass | Массы | По необходимости | Massing |
| BuiltInCategory.OST_AdaptiveComponents | Адаптивные компоненты | По необходимости | Adaptive |
| BuiltInCategory.OST_CurtainSystems | Витражные системы | Включать | Curtain systems |
| BuiltInCategory.OST_CurtainSystemPanels | Панели витражных систем | Включать | System panels |
| BuiltInCategory.OST_CurtainSystemMullions | Импосты витражных систем | Включать | System mullions |
| BuiltInCategory.OST_Stairs | Лестницы | По необходимости | Stairs |
| BuiltInCategory.OST_Railings | Ограждения | По необходимости | Railings |
| BuiltInCategory.OST_Assemblies | Сборки | Исключать | Assemblies |
| BuiltInCategory.OST_Partitions | Перегородки | По необходимости | Partitions |

## Источники
- Revit API Docs: BuiltInCategory enum
- Autodesk Revit API Developer Guide
- Сообщества: The Building Coder, Revit API Forum

## Рекомендации по фильтрации оболочки
1. **Минимальный набор**: стены, крыши, перекрытия, витражи, несущие элементы.
2. **По ситуации**: лестницы, пандусы, ограждения, наружные площадки.
3. **Исключать**: MEP, мебель, аннотации и служебные категории.
