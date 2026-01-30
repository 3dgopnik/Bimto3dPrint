# Quickstart

## Steps

1. Install Python Processor dependencies (see `PythonProcessor/README.md`).
2. Export an IFC file from Revit.
3. Ensure you have the correct TU Delft extractor exe for your IFC schema.
4. Run the pipeline:

```bash
bimto3dprint process input.ifc \
  --preset shell_only \
  --output out/model.stl \
  --format stl \
  --use-tudelft-extractor \
  --extractor-path /path/Ifc_Envelope_Extractor_ifc4.exe
```

5. Review the validation report in logs and open the output in your printing tool.
