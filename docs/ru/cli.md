# CLI

## Bimto3dPrint

### Обработка IFC

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/to/tudelft_exe_dir \
  --lod 2.2 \
  --voxel 1.0 \
  --threads 8
```

### Валидация сетки

```bash
bimto3dprint validate out/model.stl
```

### Список пресетов

```bash
bimto3dprint list-presets
```

## Основные параметры

- `process IFС_FILE` — путь к IFC файлу.
- `--preset` — имя пресета из `Config/Presets` или путь к JSON.
- `--output` — путь к файлу результата.
- `--format` — формат экспорта: `stl`, `obj`, `fbx`.
- `--scale` — коэффициент масштабирования перед экспортом.
- `--simplify` — уровень упрощения (`low`, `medium`, `high`) или число (0–1).
- `--no-thicken` — полностью отключить утолщение стен.
- `--min-wall-mm` — минимальная толщина стен при утолщении (в мм).

Оболочка, полученная из TU Delft, автоматически приводится к миллиметрам; решение по единицам логируется.

## Параметры TU Delft IfcEnvelopeExtractor

- `--use-tudelft-extractor` — включить внешний извлекатель оболочки.
- `--extractor-path` — путь к exe или к директории с несколькими exe (IFC2x3/IFC4/IFC4x3).

Если указан каталог, CLI автоматически выберет exe по схеме IFC и залогирует выбранный файл.
- `--lod` — требуемый уровень детализации (LoD).
- `--voxel` — размер вокселя.
- `--threads` — число потоков.
