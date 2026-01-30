# User Guide

## Revit plugin installation
1. Build the `RevitPlugin` project in Release.
2. `bin/Release` will contain a generated `Bimto3dPrint.addin` with the absolute DLL path.
3. Copy into your Revit Addins folder:
   - `Bimto3dPrint.dll`
   - `Bimto3dPrint.addin`
   - the `Config/Presets/Revit` folder
4. Create `bimto3dprint.settings.json` next to the `.addin` (template: `RevitPlugin/bimto3dprint.settings.json.template`).

## Usage
1. Open a Revit model.
2. Run **Bimto3dPrint Export**.
3. Choose a preset, IFC version, output folder, and output format.
4. Enable **Run Python pipeline after export** if needed.
5. Run IFC export and post-processing.

> Screenshots will be added later (placeholders without binaries).

## Python processor
Helper classes are available in the pipeline:
- `IFCLoader` — load IFC files and filter elements by category.
- `MeshOptimizer` — prepare meshes for 3D printing (shell, thickening, smoothing, validation).

## Settings
- Categories: included/excluded shell categories.
- Simplification: target triangle count and tolerances.
- Printing: scale, wall thickness, minimum feature size.

## Troubleshooting
- Empty export: verify active 3D view and category list.
- Large file size: increase simplification or exclude small details.

## FAQ
**Q:** How do I exclude furniture?
**A:** Add `BuiltInCategory.OST_Furniture` to `exclude`.
