# RevitPlugin

## RU

### Требования
- Visual Studio 2022
- .NET Framework 4.8 Developer Pack
- Revit SDK (для `RevitAPI.dll`, `RevitAPIUI.dll`)

### Структура
- `Commands/` — точки входа Revit (`IExternalCommand`).
- `UI/` — WPF диалог экспорта.
- `Filters/` — фильтры по категориям/параметрам/геометрии.
- `Services/` — подготовка вида и экспорт IFC.
- `Models/` — модели настроек.
- `Utils/` — логирование и анализ элементов.

### Сборка и тестирование
1. Установите переменную `RevitApiPath` на папку с `RevitAPI.dll`.
2. Соберите проект в конфигурации Release.
3. Скопируйте `Bimto3dPrint.addin` в папку Revit Addins.

### Coding conventions
- Код и комментарии — на английском.
- TODO — явные и короткие.

## EN

### Requirements
- Visual Studio 2022
- .NET Framework 4.8 Developer Pack
- Revit SDK (for `RevitAPI.dll`, `RevitAPIUI.dll`)

### Structure
- `Commands/` — Revit entry points (`IExternalCommand`).
- `UI/` — WPF export dialog.
- `Filters/` — category/parameter/geometry filters.
- `Services/` — view preparation and IFC export.
- `Models/` — settings models.
- `Utils/` — logging and element analysis.

### Build and test
1. Set the `RevitApiPath` variable to the folder with `RevitAPI.dll`.
2. Build the project in Release configuration.
3. Copy `Bimto3dPrint.addin` into the Revit Addins folder.

### Coding conventions
- Code and comments are in English.
- TODOs are explicit and short.
