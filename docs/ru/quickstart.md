# Быстрый старт

## Шаги

1. Установите зависимости Python Processor (см. `PythonProcessor/README.md`).
2. Подготовьте IFC файл из Revit.
3. Подготовьте exe TU Delft (один файл или папку с версиями под IFC2x3/IFC4/IFC4x3).
4. Запустите обработку:

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/to/tudelft_exe_dir
```

5. При необходимости настройте утолщение (`--min-wall-mm` или `--no-thicken`).
6. Проверьте отчёт валидации в логах (включая автоопределение единиц) и откройте результат в ПО для печати.
