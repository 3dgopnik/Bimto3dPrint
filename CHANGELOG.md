# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial project governance and documentation scaffolding.
- Revit built-in categories reference and user guide drafts.
- Configuration schemas and presets for export pipeline.
- C# Revit plugin and Python processor scaffolding.
- Pipeline runner script and test scenario descriptions.
- IFC_BuildingEnvExtractor analysis reference and shell extraction implementation.
- IFC loader utilities and mesh optimizer workflow for the Python processor.
- IFC loader now supports include/exclude categories and improved mesh thickness estimation.
- TU Delft IfcEnvelopeExtractor integration with CLI support and real mesh exporters.
- TU Delft extraction now validates mesh quality and auto-normalizes units to millimeters.
- CLI controls for wall thickening and minimum wall thickness in millimeters.
- IFC schema auto-detection for TU Delft extractor directory selection.
- Unit detection smoke tests for mesh normalization.

### Changed
- TU Delft extractor config now uses safe voxel/IFC/JSON defaults and stricter tolerances.
- Mesh unit detection heuristic now avoids false millimeter scaling.
- TU Delft OBJ selection now uses the newest generated file.
