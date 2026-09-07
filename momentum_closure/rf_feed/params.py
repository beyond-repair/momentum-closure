"""Locked RF-feed and Faraday-enclosure parameters (P0-C.1).

CATEGORY LOCKS
--------------
- Geometry scale factor s never appears as an angle here.
- Feed is a classical single-port SMA/coax topology.
- Faraday enclosure is an explicit perfect-electric-conductor (PEC)
  boundary for the classical boundary-value problem.
- Ware / non-classical parameters are not admitted.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Tuple

FEED_SCHEMA_VERSION = "P0-C.1"


@dataclass(frozen=True)
class FeedParams:
    """Single-port SMA / coax excitation parameters.

    All lengths in millimetres unless noted.  Impedance in ohms.
    Frequency band is declarative only at this stage (solver uses it later).
    """

    # Coax geometry (typical SMA-compatible proportions, scaled to L0 context)
    outer_diameter_mm: float = 4.6      # SMA outer conductor ~ OD
    inner_diameter_mm: float = 1.27     # centre pin
    dielectric_od_mm: float = 4.1       # PTFE / dielectric outer
    pin_length_mm: float = 8.0          # protrusion into cavity
    flange_thickness_mm: float = 2.0

    # Electrical
    Z0_ohm: float = 50.0
    f_min_Hz: float = 1.0e9
    f_max_Hz: float = 6.0e9
    f_nominal_Hz: float = 2.45e9

    # Placement relative to geometry origin (mm)
    # Default: feed enters along -ž through the bottom of the enclosure
    port_position_mm: Tuple[float, float, float] = (0.0, 0.0, -60.0)
    port_axis: Tuple[float, float, float] = (0.0, 0.0, 1.0)  # wave vector / pin axis

    def __post_init__(self) -> None:
        if self.Z0_ohm <= 0:
            raise ValueError("Z0 must be positive")
        if self.inner_diameter_mm >= self.outer_diameter_mm:
            raise ValueError("inner diameter must be < outer diameter")
        if self.f_min_Hz >= self.f_max_Hz:
            raise ValueError("f_min must be < f_max")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["schema_version"] = FEED_SCHEMA_VERSION
        d["category_locks"] = {
            "feed_is_classical_sma_coax": True,
            "ware_modifies_feed": False,
            "single_port_only": True,
            "s_used_as_angle": False,
        }
        return d


@dataclass(frozen=True)
class FaradayEnclosure:
    """Explicit Faraday (PEC) boundary surrounding the CD-N3 geometry.

    The enclosure is the outer classical boundary for the BVP.
    Interior holds the pure-geometry structure + feed.
    """

    # Cylindrical / box outer boundary (mm)
    radius_mm: float = 80.0
    height_mm: float = 120.0
    wall_thickness_mm: float = 2.0
    shape: str = "cylinder"  # "cylinder" | "box"

    # Origin at geometric centre; axis aligned with geometry â = ž
    centre_mm: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Boundary condition tag for solvers
    bc_type: str = "PEC"

    def __post_init__(self) -> None:
        if self.shape not in ("cylinder", "box"):
            raise ValueError("shape must be 'cylinder' or 'box'")
        if self.radius_mm <= 0 or self.height_mm <= 0:
            raise ValueError("enclosure dimensions must be positive")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["schema_version"] = FEED_SCHEMA_VERSION
        d["category_locks"] = {
            "enclosure_is_explicit_faraday": True,
            "bc_type": self.bc_type,
            "ware_modifies_enclosure": False,
        }
        return d


# Canonical locked instances
DEFAULT_FEED = FeedParams()
DEFAULT_ENCLOSURE = FaradayEnclosure()
