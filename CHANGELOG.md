# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Split preset packs into Revit and Python groups with prefixed CLI listing and new python shell preset.
- ConfigManager with preset discovery and validation for the Python pipeline.
- Revit IFC export flow with selectable presets, IFC version, output folder, and optional Python pipeline runner.
- IFC export service, Python runner settings template, and addin template generation during build.
- Python pipeline settings template for configurable Python/TU Delft paths.
- Version-pinned Python requirements and dev pytest optional dependency.
- Updated documentation for manual IFC and one-click Revit workflows plus preset type guidance.
- Expanded user-facing README with installation, usage, and troubleshooting details.
- Roadmap with versioned planning and status markers.
- New backlog ideas for preview mode and batch CLI processing.
- Initial project governance and documentation scaffolding.
- Revit built-in categories reference and user guide drafts.
- Configuration schemas and presets for export pipeline.
- C# Revit plugin and Python processor scaffolding.
- Revit export command now launches IFC export and Python processing via the new bridge service.
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
