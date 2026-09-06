"""Locked pure-geometry parameters for CD-N3 baseline.

CATEGORY LOCK
-------------
s = 0.45 is a dimensionless recursive *scaling* factor.
It is NOT an angle.  Treating s as θ0 (radians) is a category error
and is forbidden in this module.

3-fold rotational symmetry is supplied exclusively by the Rodrigues
matrix R(2π/3) about the canonical axis â.  No free angular parameter
θ0 is introduced.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Tuple

MANIFEST_SCHEMA_VERSION = "P0-B.2"


@dataclass(frozen=True)
class GeometryParams:
    """Pure geometry (G) — classical baseline only.

    Fields
    ------
    L0_mm : float
        Root characteristic length (mm).
    n : int
        Discrete rotational symmetry order.  Must be 3 for CD-N3.
    s : float
        Non-dimensional recursive scale factor (0 < s < 1).
        **Not an angle.**  Sub-element lengths are L0 * s^k.
    depth : int
        Number of recursive scale levels (including root level 0).
    axis : Tuple[float, float, float]
        Unit symmetry axis â (canonical +z for the control geometry).
    models : Tuple[str, ...]
        Designators for the three polarity / mirror / null variants.
    """

    L0_mm: float = 100.0
    n: int = 3
    s: float = 0.45          # SCALE ONLY — never interpret as radians
    depth: int = 4           # levels 0..3 → L0, L0*s, L0*s², L0*s³
    axis: Tuple[float, float, float] = (0.0, 0.0, 1.0)
    models: Tuple[str, ...] = ("CD-N3-P", "CD-N3-M", "CD-N3-N")

    def __post_init__(self) -> None:
        if self.n != 3:
            raise ValueError("CD-N3 baseline requires n = 3")
        if not (0.0 < self.s < 1.0):
            raise ValueError("s must be a scale factor in (0, 1)")
        if self.depth < 1:
            raise ValueError("depth must be ≥ 1")
        # Explicit category guard: s is not an angle
        object.__setattr__(self, "_s_is_scale_not_angle", True)

    @property
    def fold_angle_rad(self) -> float:
        """Canonical 3-fold rotation angle.  Independent of s."""
        import math
        return 2.0 * math.pi / self.n   # 120° = 2π/3 — NOT s

    @property
    def scale_ladder_mm(self) -> List[float]:
        """L_k = L0 * s^k for k = 0 .. depth-1."""
        return [self.L0_mm * (self.s ** k) for k in range(self.depth)]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["schema_version"] = MANIFEST_SCHEMA_VERSION
        d["fold_angle_rad"] = self.fold_angle_rad
        d["fold_angle_deg"] = 120.0
        d["scale_ladder_mm"] = self.scale_ladder_mm
        d["category_locks"] = {
            "s_is_scale_factor": True,
            "s_is_not_angle": True,
            "theta_0_invented": False,
            "symmetry_source": "Rodrigues R(2π/n) about â",
            "ware_modifies_geometry": False,
        }
        return d


# Canonical locked instance for the clean-room baseline
BASELINE = GeometryParams()
