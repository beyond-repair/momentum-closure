"""P0-B.2 geometry generator — pure classical baseline.

Emits:
  - machine-readable JSON manifest (vertex coordinates, scale ladder,
    Rodrigues matrices, boundary tags)
  - OpenSCAD source for CD-N3-P / CD-N3-M / CD-N3-N
  - optional STL via external mesh tools (not required here)

Category locks are enforced at construction time: s is never promoted
to an angle; θ0 is never invented; Ware parameters cannot enter.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .params import BASELINE, GeometryParams, MANIFEST_SCHEMA_VERSION
from .rodrigues import apply_rotation, threefold_rotations, rodriques_matrix


# ---------------------------------------------------------------------------
# Primitive: equilateral triangle in the plane ⊥ â, scaled by L
# ---------------------------------------------------------------------------

def _equilateral_triangle(L_mm: float, axis: Sequence[float]) -> np.ndarray:
    """
    Three vertices of an equilateral triangle centred at origin,
    lying in the plane perpendicular to â, with side length ~ L_mm.

    Circumradius R = L / √3  (so that the projected span is order-L).
    """
    # Build an orthonormal frame with e3 = â
    a = np.asarray(axis, dtype=float)
    a = a / np.linalg.norm(a)
    # choose a helper vector not parallel to a
    helper = np.array([1.0, 0.0, 0.0]) if abs(a[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(a, helper)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(a, e1)
    R_circ = L_mm / math.sqrt(3.0)
    verts = []
    for k in range(3):
        phi = 2.0 * math.pi * k / 3.0
        v = R_circ * (math.cos(phi) * e1 + math.sin(phi) * e2)
        verts.append(v)
    return np.array(verts, dtype=float)


@dataclass
class GeometryInstance:
    """One concrete CAD model (P / M / N variant)."""

    model_id: str
    params: GeometryParams
    vertices_mm: Dict[str, List[List[float]]] = field(default_factory=dict)
    transforms: Dict[str, List[List[float]]] = field(default_factory=dict)
    boundary_tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "params": self.params.to_dict(),
            "vertices_mm": self.vertices_mm,
            "transforms": self.transforms,
            "boundary_tags": self.boundary_tags,
            "metadata": self.metadata,
        }


def _polarity_sign(model_id: str) -> float:
    """P → +1, M → −1 (mirror), N → 0 (null / control)."""
    if model_id.endswith("-P"):
        return 1.0
    if model_id.endswith("-M"):
        return -1.0
    return 0.0


def generate_baseline(
    params: Optional[GeometryParams] = None,
    model_ids: Optional[Sequence[str]] = None,
) -> List[GeometryInstance]:
    """
    Build the three baseline geometries CD-N3-P, CD-N3-M, CD-N3-N.

    Construction
    ------------
    1. Scale ladder: L_k = L0 * s^k   (s is scale only)
    2. At each level, place an equilateral triangle of size L_k
    3. Replicate by {I, R(120°), R(240°)} about â   (Rodrigues only)
    4. Polarity: P keeps orientation, M applies a reflection through
       a plane containing â, N is the pure geometric control (no
       handedness bias beyond the classical shape itself)

    No Ware term, no invented θ0, no use of s as an angle.
    """
    params = params or BASELINE
    model_ids = list(model_ids or params.models)
    rotations = threefold_rotations(params.axis)
    rot_mats = {
        f"R_{k * 120}": rotations[k].tolist() for k in range(3)
    }

    instances: List[GeometryInstance] = []
    for mid in model_ids:
        sign = _polarity_sign(mid)
        verts: Dict[str, List[List[float]]] = {}
        tags: Dict[str, str] = {}

        for level, L in enumerate(params.scale_ladder_mm):
            base_tri = _equilateral_triangle(L, params.axis)
            # optional reflection for M variant (mirror through xz-plane
            # when â = ž — classical geometric mirror, not a Ware op)
            if sign < 0:
                reflect = np.diag([1.0, -1.0, 1.0])
                base_tri = (reflect @ base_tri.T).T

            for k, R in enumerate(rotations):
                cloud = apply_rotation(R, base_tri)
                key = f"level{level}_sector{k}"
                verts[key] = cloud.tolist()
                tags[key] = (
                    f"boundary:conductor;level={level};sector={k};"
                    f"scale={params.s**level:.6f};model={mid}"
                )

        inst = GeometryInstance(
            model_id=mid,
            params=params,
            vertices_mm=verts,
            transforms=rot_mats,
            boundary_tags=tags,
            metadata={
                "polarity_sign": sign,
                "category_locks": params.to_dict()["category_locks"],
                "schema_version": MANIFEST_SCHEMA_VERSION,
            },
        )
        instances.append(inst)
    return instances


def emit_manifest(
    instances: Sequence[GeometryInstance],
    path: Path | str,
) -> str:
    """Write machine-readable JSON manifest; return SHA-256 of payload."""
    path = Path(path)
    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "phase": "P0-B.2",
        "description": (
            "Pure-geometry CAD baseline for CD-N3. "
            "s is a scale factor only; symmetry from Rodrigues R(120°) about â. "
            "Ware layer forbidden from modifying this baseline."
        ),
        "models": [inst.to_dict() for inst in instances],
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    payload["manifest_sha256"] = digest
    text = json.dumps(payload, indent=2, sort_keys=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return digest


def emit_openscad(
    instance: GeometryInstance,
    path: Path | str,
    wall_mm: float = 1.0,
) -> None:
    """
    Emit a simple OpenSCAD module that extrudes the level-0 triangle
    sectors and recursively places scaled copies.  Useful for visual
    inspection; the authoritative geometry remains the JSON manifest.
    """
    path = Path(path)
    p = instance.params
    lines: List[str] = [
        f"// Auto-generated P0-B.2 — {instance.model_id}",
        f"// L0 = {p.L0_mm} mm, n = {p.n}, s = {p.s} (SCALE ONLY)",
        f"// fold angle = 120 deg via Rodrigues; θ0 NOT invented",
        f"// category_locks: s_is_not_angle, ware_modifies_geometry=false",
        "",
        f"L0 = {p.L0_mm};",
        f"s  = {p.s};  // non-dimensional scale — never an angle",
        f"wall = {wall_mm};",
        "",
        "module sector_triangle(L) {",
        "  R = L / sqrt(3);",
        "  points = [",
        "    [R, 0],",
        "    [R*cos(120), R*sin(120)],",
        "    [R*cos(240), R*sin(240)]",
        "  ];",
        "  linear_extrude(height = wall)",
        "    polygon(points);",
        "}",
        "",
        "module threefold(L) {",
        "  for (k = [0:2])",
        "    rotate([0, 0, k*120])",
        "      sector_triangle(L);",
        "}",
        "",
        f"// {instance.model_id}",
    ]
    if instance.metadata.get("polarity_sign", 1.0) < 0:
        lines += ["mirror([0, 1, 0]) {"]
        indent = "  "
    else:
        indent = ""

    for level in range(p.depth):
        L = p.L0_mm * (p.s ** level)
        lines.append(f"{indent}threefold({L:.6f});  // level {level}")

    if instance.metadata.get("polarity_sign", 1.0) < 0:
        lines.append("}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def run_p0_b2(
    out_dir: Path | str = "geometry_out",
) -> Dict[str, Any]:
    """Convenience entry point for P0-B.2."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    instances = generate_baseline()
    manifest_path = out / "CD-N3_geometry_manifest.json"
    digest = emit_manifest(instances, manifest_path)
    scad_paths = []
    for inst in instances:
        scad = out / f"{inst.model_id}.scad"
        emit_openscad(inst, scad)
        scad_paths.append(str(scad))
    return {
        "manifest": str(manifest_path),
        "manifest_sha256": digest,
        "openscad": scad_paths,
        "scale_ladder_mm": instances[0].params.scale_ladder_mm,
        "category_locks": instances[0].params.to_dict()["category_locks"],
    }
