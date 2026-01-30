# IFC_BuildingEnvExtractor — quick analysis

> Note: the `tudelft3d/IFC_BuildingEnvExtractor` repository is not reachable from this environment (HTTP 403). The analysis is based on common IFC processing practices and should be verified once access is restored.

## Expected architecture

1. Load IFC (`ifcopenshell.open`).
2. Filter envelope categories (walls, roofs, slabs, etc.).
3. Tessellate geometry (`ifcopenshell.geom`).
4. Merge meshes into one.
5. Extract envelope (voxel/alpha/convex hull).
6. Post-process (repair, simplify, scale).
7. Export (STL/OBJ/FBX).

## Adaptation for 3D printing

- Scale to printer volume.
- Simplify while preserving shape.
- Ensure watertightness and normals.
- Validate and log before export.

## Full analysis

See `Documentation/Reference/ifc_building_env_extractor_analysis.md`.
