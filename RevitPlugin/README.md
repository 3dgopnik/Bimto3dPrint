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
3. В `bin/Release` будет сгенерирован `Bimto3dPrint.addin` с абсолютным путём к DLL.
4. Скопируйте в папку Revit Addins:
   - `Bimto3dPrint.dll`
   - `Bimto3dPrint.addin`
   - папку `Config/Presets/Revit`
5. Создайте `bimto3dprint.settings.json` рядом с `.addin` (шаблон: `bimto3dprint.settings.json.template`).

### Настройка Python пайплайна

Файл `bimto3dprint.settings.json` задаёт путь к Python/venv или к `bimto3dprint.exe`.

Пример:

```json
{
  "pythonExecutable": "C:\\Path\\To\\Python\\python.exe",
  "bimto3dprintExecutable": "",
  "bimto3dprintModule": "bimto3dprint.main",
  "useTudelftExtractor": true,
  "tudelftExtractorPath": "C:\\Path\\To\\Ifc_Envelope_Extractor_ifc4.exe"
}
```

Если `bimto3dprintExecutable` указан, он имеет приоритет над `pythonExecutable`.
При использовании ревит‑пресетов в пайплайне включайте `useTudelftExtractor`.

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
3. `bin/Release` will contain a generated `Bimto3dPrint.addin` with the absolute DLL path.
4. Copy into the Revit Addins folder:
   - `Bimto3dPrint.dll`
   - `Bimto3dPrint.addin`
   - the `Config/Presets/Revit` folder
5. Create `bimto3dprint.settings.json` next to the `.addin` (template: `bimto3dprint.settings.json.template`).

### Python pipeline configuration

`bimto3dprint.settings.json` defines the Python/venv path or a `bimto3dprint.exe` path.

Example:

```json
{
  "pythonExecutable": "C:\\Path\\To\\Python\\python.exe",
  "bimto3dprintExecutable": "",
  "bimto3dprintModule": "bimto3dprint.main",
  "useTudelftExtractor": true,
  "tudelftExtractorPath": "C:\\Path\\To\\Ifc_Envelope_Extractor_ifc4.exe"
}
```

If `bimto3dprintExecutable` is set, it takes precedence over `pythonExecutable`.
When running revit presets through the pipeline, enable `useTudelftExtractor`.

### Coding conventions
- Code and comments are in English.
- TODOs are explicit and short.
