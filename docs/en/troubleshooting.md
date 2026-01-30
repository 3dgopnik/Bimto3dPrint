# Troubleshooting

## TU Delft extractor does not create OBJ

- Ensure you are using the exe that matches the IFC schema (IFC2x3 / IFC4 / IFC4x3).
- If you pass a directory, ensure it contains the exe for your IFC schema (IFC2x3 / IFC4 / IFC4x3).
- If you pass a file, confirm `--extractor-path` points to a valid executable.
- Verify the output directory is writable.
- Make sure OBJ output is enabled (it is on by default with `--use-tudelft-extractor`).

## "Extractor execution timed out"

- Increase the timeout or reduce model size.
- Lower `--lod` and increase `--voxel`.

## OBJ loading fails

- Verify that the OBJ file exists in the output directory.
- Ensure the model produced non-empty geometry.

## "TU Delft extractor returned invalid mesh"

- Confirm the extractor exe matches the IFC schema (or that auto-selection picked the correct one).
- Review LoD and `--voxel`: overly coarse voxel sizes can yield empty envelopes.
- Ensure the source IFC contains the building envelope geometry.

## Revit preset error in CLI

Message: `Revit preset contains BuiltInCategory.* and cannot be used with internal IFC extractor`.

- Use a `python:` preset (for example, `python:shell_only`) for the internal extractor.
- Or enable `--use-tudelft-extractor` and provide `--extractor-path`.

## Model scale looks incorrect

- Check the unit detection log (meters vs millimeters).
- Make sure `--scale` is not applied twice.
