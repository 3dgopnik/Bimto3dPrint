# Quickstart

## Steps

1. Install Python Processor dependencies (see `PythonProcessor/README.md`).
2. Export an IFC file from Revit.
3. Prepare the TU Delft extractor exe (single file or a directory with IFC2x3/IFC4/IFC4x3 builds).
4. Run the pipeline:

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/to/tudelft_exe_dir
```

5. Adjust wall thickening if needed (`--min-wall-mm` or `--no-thicken`).
6. Review the validation report in logs (including unit detection) and open the output in your printing tool.
