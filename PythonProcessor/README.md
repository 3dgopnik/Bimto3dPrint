# PythonProcessor

## RU

Python‑пайплайн для загрузки IFC, извлечения оболочки и подготовки сетки к 3D печати.

### Установка

```bash
python -m pip install -e .
```

### Внешний IfcEnvelopeExtractor (TU Delft)

1. Скачайте exe для нужной схемы IFC (IFC2x3 / IFC4 / IFC4x3).
2. Передайте путь к exe через CLI флаг `--extractor-path`.

### Пример

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
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

### External IfcEnvelopeExtractor (TU Delft)

1. Download the exe that matches your IFC schema (IFC2x3 / IFC4 / IFC4x3).
2. Provide the executable path via the `--extractor-path` CLI flag.

### Example

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe \
  --lod 2.2 \
  --voxel 1.0
```
