"""Integration for TU Delft IFC Building Envelope Extractor."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from loguru import logger

from bimto3dprint.utils.ifc_schema import detect_ifc_schema


@dataclass
class IfcEnvExtractorRunner:
    """Run the TU Delft IFC envelope extractor executable."""

    extractor_path: Path
    resolved_extractor_path: Path | None = None

    def __post_init__(self) -> None:
        self.extractor_path = Path(self.extractor_path)
        if not self.extractor_path.exists():
            raise FileNotFoundError(f"Extractor executable not found: {self.extractor_path}")
        if not (self.extractor_path.is_file() or self.extractor_path.is_dir()):
            raise ValueError(f"Extractor path must be a file or directory: {self.extractor_path}")

    def _resolve_extractor_path(self, ifc_path: Path) -> Path:
        if self.extractor_path.is_file():
            self.resolved_extractor_path = self.extractor_path
            return self.extractor_path

        schema = detect_ifc_schema(ifc_path)
        logger.info("Detected IFC schema: {}", schema)

        schema_patterns = {
            "IFC2X3": "ifc2x3",
            "IFC4": "ifc4",
            "IFC4X3": "ifc4x3",
        }
        token = schema_patterns[schema]
        candidates = [
            path
            for path in self.extractor_path.glob("*.exe")
            if token in path.name.lower()
        ]
        if schema == "IFC4":
            candidates = [path for path in candidates if "ifc4x3" not in path.name.lower()]

        if not candidates:
            raise RuntimeError(
                "Could not find extractor exe for "
                f"{schema} in {self.extractor_path}. "
                f"Expected name like '*{token}*.exe'."
            )

        chosen = sorted(candidates, key=lambda path: path.name.lower())[0]
        logger.info(
            "Auto-selected TU Delft extractor for IFC schema: {} \u2192 {}",
            schema,
            chosen.name,
        )
        logger.info("Selected extractor exe path: {}", chosen)
        self.resolved_extractor_path = chosen
        return chosen

    def build_config(
        self,
        ifc_path: Path,
        output_dir: Path,
        lods: list[float] | None = None,
        voxel_size: float = 1.0,
        threads: int = 8,
        generate_exterior: bool = True,
        generate_interior: bool = False,
        output_obj: bool = True,
        output_step: bool = False,
    ) -> dict[str, Any]:
        """Build configuration dictionary for the extractor.

        Args:
            ifc_path: Path to the IFC file.
            output_dir: Output directory for extractor artifacts.
            lods: List of target LoD values.
            voxel_size: Voxel size for envelope generation.
            threads: Number of threads.
            generate_exterior: Whether to output exterior JSON geometry.
            generate_interior: Whether to output interior JSON geometry.
            output_obj: Whether to output OBJ mesh.
            output_step: Whether to output STEP file.

        Returns:
            Configuration dictionary aligned with TU Delft extractor schema.
        """
        ifc_path = Path(ifc_path)
        output_dir = Path(output_dir)
        lods = lods or [2.2]

        resolved_extractor = self._resolve_extractor_path(ifc_path)
        logger.info(
            "TU Delft extractor settings: lods={}, voxel_size={}, exe_path={}, output_dir={}",
            lods,
            voxel_size,
            resolved_extractor,
            output_dir,
        )
        config: dict[str, Any] = {
            "Filepaths": {
                "Input": [str(ifc_path)],
                "Output": str(output_dir / "envelope.city.json"),
                "Report": str(output_dir / "envelope_report.json"),
            },
            "LoD output": lods,
            "Voxel": {
                "Size": float(voxel_size),
                "Store values": 0,
                "Logic": 3,
                "Coarse filter": True,
            },
            "IFC": {
                "Ignore proxy": True,
                "Simplify geometry": True,
                "Correct placement": True,
            },
            "JSON": {
                "Generate exterior": int(generate_exterior),
                "Generate interior": int(generate_interior),
                "Generate footprint": 0,
                "Generate roof outline": 0,
            },
            "Output format": {
                "OBJ file": int(output_obj),
                "STEP file": int(output_step),
            },
            "Tolerances": {
                "Spatial": 1e-6,
                "Angular": 1e-4,
                "Area": 1e-4,
            },
            "Generate report": 1,
            "Threads": int(threads),
        }
        logger.info("Built TU Delft extractor config for {}", ifc_path)
        return config

    def write_config(self, config: dict[str, Any], config_path: Path) -> None:
        """Write configuration dictionary to disk as JSON.

        Args:
            config: Configuration dictionary.
            config_path: Path to write JSON file.
        """
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        logger.info("Saved extractor config: {}", config_path)

    def run(
        self,
        config_path: Path,
        ifc_path: Path,
        timeout_sec: int = 3600,
    ) -> CompletedProcess[str]:
        """Run the extractor executable with a configuration file.

        Args:
            config_path: Path to the JSON configuration.
            ifc_path: Path to the IFC file (used for schema detection when needed).
            timeout_sec: Timeout in seconds.

        Returns:
            CompletedProcess instance.

        Raises:
            RuntimeError: If extractor returns a non-zero exit code.
            TimeoutError: If the process times out.
        """
        config_path = Path(config_path)
        resolved_extractor = self._resolve_extractor_path(ifc_path)
        logger.info("Running extractor: {} {}", resolved_extractor, config_path)
        try:
            completed = subprocess.run(
                [str(resolved_extractor), str(config_path)],
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            logger.error("Extractor timed out after {}s", timeout_sec)
            raise TimeoutError("Extractor execution timed out") from exc

        if completed.stdout:
            logger.info("Extractor stdout:\n{}", completed.stdout)
        if completed.stderr:
            logger.warning("Extractor stderr:\n{}", completed.stderr)

        if completed.returncode != 0:
            raise RuntimeError(
                f"Extractor failed with code {completed.returncode}: {completed.stderr.strip()}"
            )

        logger.info("Extractor finished successfully")
        return completed

    def find_output_obj(self, output_dir: Path) -> Path:
        """Find the most recent OBJ file produced by the extractor.

        Args:
            output_dir: Directory where outputs are expected.

        Returns:
            Path to the OBJ file.

        Raises:
            FileNotFoundError: If no OBJ files were found.
        """
        output_dir = Path(output_dir)
        objs = list(output_dir.rglob("*.obj"))
        if not objs:
            raise FileNotFoundError(
                "OBJ output not found: check Output format, output path, and permissions."
            )

        chosen = max(objs, key=lambda path: path.stat().st_mtime)
        mtime = chosen.stat().st_mtime
        logger.info("Found {} OBJ files under {}", len(objs), output_dir)
        logger.info("Selected OBJ output: {} (mtime={})", chosen, mtime)
        return chosen
