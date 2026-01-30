# PythonProcessor

## RU

Python‑пайплайн для загрузки IFC, извлечения оболочки и подготовки сетки к 3D печати.

### Установка

```bash
python -m pip install -e .
```

### Внутренний режим (python‑пресеты)

```bash
bimto3dprint process input.ifc \
  --preset python:shell_only \
  --output out/model.stl \
  --format stl
```

### Внешний IfcEnvelopeExtractor (TU Delft)

1. Скачайте exe для нужной схемы IFC (IFC2x3 / IFC4 / IFC4x3).
2. Передайте путь к exe через CLI флаг `--extractor-path`.
3. Можно использовать `revit:` пресеты.

### Пример TU Delft

```bash
bimto3dprint process input.ifc \
  --preset revit:shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe \
  --lod 2.2 \
  --voxel 1.0
```

## EN

Python pipeline for loading IFC files, extracting the building envelope, and preparing meshes for 3D printing.

### Installation

```bash
python -m pip install -e .
```

### Internal mode (python presets)

```bash
bimto3dprint process input.ifc \
  --preset python:shell_only \
  --output out/model.stl \
  --format stl
```

### External IfcEnvelopeExtractor (TU Delft)

1. Download the exe that matches your IFC schema (IFC2x3 / IFC4 / IFC4x3).
2. Provide the executable path via the `--extractor-path` CLI flag.
3. `revit:` presets are allowed in this mode.

### TU Delft example

```bash
bimto3dprint process input.ifc \
  --preset revit:shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe \
  --lod 2.2 \
  --voxel 1.0
```
