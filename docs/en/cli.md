# CLI

## Bimto3dPrint

### Process IFC

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe \
  --lod 2.2 \
  --voxel 1.0 \
  --threads 8
```

### Validate mesh

```bash
bimto3dprint validate out/model.stl
```

### List presets

```bash
bimto3dprint list-presets
```

## Core options

- `process IFC_FILE` — path to the IFC file.
- `--preset` — preset name from `Config/Presets` or a JSON path.
- `--output` — output file path.
- `--format` — export format: `stl`, `obj`, `fbx`.
- `--scale` — scale factor before export.
- `--simplify` — simplification level (`low`, `medium`, `high`) or ratio (0–1).
- `--no-thicken` — disable wall thickening entirely.
- `--min-wall-mm` — minimum wall thickness during thickening (mm).

The envelope from TU Delft is automatically normalized to millimeters; the unit decision is logged.

## TU Delft IfcEnvelopeExtractor options

- `--use-tudelft-extractor` — enable the external extractor.
- `--extractor-path` — path to the schema-specific exe (IFC2x3/IFC4/IFC4x3).
- `--lod` — target LoD.
- `--voxel` — voxel size.
- `--threads` — number of threads.
