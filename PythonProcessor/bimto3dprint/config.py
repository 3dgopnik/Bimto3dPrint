"""Configuration loader and preset manager for the pipeline.

Example:
    from bimto3dprint.config import ConfigManager

    manager = ConfigManager()
    config = manager.load_preset("python:shell_only")
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Sequence

from loguru import logger


def load_config(path: Path) -> Dict[str, Any]:
    """Load a JSON configuration file.

    Args:
        path: Path to the JSON config.

    Returns:
        Parsed configuration dictionary.
    """
    # TODO: Add schema validation.
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


class ConfigManager:
    """Manage preset discovery and validation."""

    def __init__(self, config_dir: Path | str = "../Config/Presets") -> None:
        base_dir = Path(__file__).resolve().parents[1]
        resolved_dir = Path(config_dir)
        if not resolved_dir.is_absolute():
            resolved_dir = (base_dir / resolved_dir).resolve()
        self.config_dir = resolved_dir
        self.python_dir = self.config_dir / "Python"
        self.revit_dir = self.config_dir / "Revit"

    def load_preset(self, preset: str) -> Dict[str, Any]:
        """Load a preset by name, prefix, or path."""
        preset_path = Path(preset)
        if preset_path.exists():
            logger.info("Loading preset from path: {}", preset_path)
            config = load_config(preset_path)
            self.validate_config(config)
            return config

        preset_type, preset_name = self._split_preset_name(preset)
        directory = self.python_dir if preset_type == "python" else self.revit_dir
        preset_path = directory / f"{preset_name}.json"
        if not preset_path.exists():
            raise FileNotFoundError(f"Preset not found: {preset}")

        logger.info("Loading {} preset: {}", preset_type, preset_path)
        config = load_config(preset_path)
        self.validate_config(config)
        return config

    def get_available_presets(self) -> list[str]:
        """Return available preset names with prefixes."""
        presets: list[str] = []
        presets.extend(self._collect_presets(self.python_dir, "python"))
        presets.extend(self._collect_presets(self.revit_dir, "revit"))
        return presets

    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate core configuration structure."""
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a JSON object.")

        if "version" not in config:
            raise ValueError("Configuration missing required key: version")

        categories = config.get("categories")
        if not isinstance(categories, dict):
            raise ValueError("Configuration missing required key: categories")

        include = categories.get("include")
        if not isinstance(include, Sequence) or isinstance(include, str) or not list(include):
            raise ValueError("Configuration missing required key: categories.include")

        if "tudelft_extractor" in config:
            logger.info("TU Delft extractor enabled; skipping category content validation.")

    @staticmethod
    def _split_preset_name(preset: str) -> tuple[str, str]:
        if ":" in preset:
            prefix, name = preset.split(":", 1)
            if prefix in {"python", "revit"}:
                return prefix, name
        return "python", preset

    @staticmethod
    def _collect_presets(directory: Path, prefix: str) -> list[str]:
        if not directory.exists():
            return []
        return [
            f"{prefix}:{path.stem}"
            for path in sorted(directory.glob("*.json"))
        ]
