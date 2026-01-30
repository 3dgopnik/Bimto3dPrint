# Быстрый старт

## Сценарий A — Manual IFC

1. Установите зависимости Python Processor (см. `PythonProcessor/README.md`).
2. Экспортируйте IFC из Revit.
3. Запустите внутренний пайплайн с python‑пресетом:

```bash
bimto3dprint process input.ifc \
  --preset python:shell_only \
  --output out/model.stl \
  --format stl
```

4. При необходимости настройте утолщение (`--min-wall-mm` или `--no-thicken`).
5. Проверьте отчёт валидации в логах и откройте результат в ПО для печати.

## Сценарий B — One‑click из Revit

1. Соберите и установите Revit plugin (см. `RevitPlugin/README.md`).
2. Убедитесь, что рядом с `.addin` лежит `bimto3dprint.settings.json` с путём к Python.
3. В Revit нажмите **Bimto3dPrint**, выберите пресет, папку вывода и формат.
4. Отметьте **Run Python pipeline after export** для авто‑запуска пайплайна.
5. Дождитесь сообщения с путём к результату и логом.
