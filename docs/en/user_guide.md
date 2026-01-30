# User Guide

## Revit plugin installation
1. Build the `RevitPlugin` project in Release.
2. Copy `Bimto3dPrint.addin` into your Revit Addins folder.
3. Ensure `Bimto3dPrint.dll` sits next to the `.addin` file.

## Usage
1. Open a Revit model.
2. Run **Bimto3dPrint Export**.
3. Choose a preset and output format.
4. Run IFC export and post-processing.

> Screenshots will be added later (placeholders without binaries).

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
