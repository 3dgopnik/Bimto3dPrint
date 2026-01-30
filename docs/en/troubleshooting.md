# Troubleshooting

## TU Delft extractor does not create OBJ

- Ensure you are using the exe that matches the IFC schema (IFC2x3 / IFC4 / IFC4x3).
- Confirm `--extractor-path` points to a valid executable.
- Verify the output directory is writable.
- Make sure OBJ output is enabled (it is on by default with `--use-tudelft-extractor`).

## "Extractor execution timed out"

- Increase the timeout or reduce model size.
- Lower `--lod` and increase `--voxel`.

## OBJ loading fails

- Verify that the OBJ file exists in the output directory.
- Ensure the model produced non-empty geometry.
