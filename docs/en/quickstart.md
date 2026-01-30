# Quickstart

## Scenario A — Manual IFC

1. Install Python Processor dependencies (see `PythonProcessor/README.md`).
2. Export an IFC from Revit.
3. Run the internal pipeline with a python preset:

```bash
bimto3dprint process input.ifc \
  --preset python:shell_only \
  --output out/model.stl \
  --format stl
```

4. Adjust wall thickening if needed (`--min-wall-mm` or `--no-thicken`).
5. Review the validation report in logs and open the output in your printing tool.

## Scenario B — One-click from Revit

1. Build and install the Revit plugin (see `RevitPlugin/README.md`).
2. Ensure `bimto3dprint.settings.json` sits next to the `.addin` with the Python path set.
3. In Revit click **Bimto3dPrint**, pick a preset, output folder, and format.
4. Enable **Run Python pipeline after export** to run the pipeline automatically.
5. Wait for the completion dialog with the output and log paths.
