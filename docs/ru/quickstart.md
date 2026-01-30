# Быстрый старт

## Шаги

1. Установите зависимости Python Processor (см. `PythonProcessor/README.md`).
2. Подготовьте IFC файл из Revit.
3. Убедитесь, что у вас есть подходящий exe TU Delft для нужной схемы IFC.
4. Запустите обработку:

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe
```

5. Проверьте отчёт валидации в логах и откройте результат в ПО для печати.
