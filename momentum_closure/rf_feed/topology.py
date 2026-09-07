"""SMA/coax feed topology builder (P0-C.1).

Produces a machine-readable description of:
  - coax pin / dielectric / outer conductor
  - port face (lumped / wave port candidate)
  - Faraday enclosure surface tags
  - attachment relative to CD-N3 geometry origin

No eigenmode solve here — that is P0-C.2/C.3.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .params import DEFAULT_ENCLOSURE, DEFAULT_FEED, FaradayEnclosure, FeedParams


@dataclass
class FeedTopology:
    """Concrete single-port feed + enclosure layout."""

    feed: FeedParams
    enclosure: FaradayEnclosure
    # Geometric primitives (mm)
    pin_cylinder: Dict[str, Any] = field(default_factory=dict)
    dielectric_cylinder: Dict[str, Any] = field(default_factory=dict)
    outer_conductor: Dict[str, Any] = field(default_factory=dict)
    port_face: Dict[str, Any] = field(default_factory=dict)
    enclosure_surface: Dict[str, Any] = field(default_factory=dict)
    boundary_tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feed": self.feed.to_dict(),
            "enclosure": self.enclosure.to_dict(),
            "pin_cylinder": self.pin_cylinder,
            "dielectric_cylinder": self.dielectric_cylinder,
            "outer_conductor": self.outer_conductor,
            "port_face": self.port_face,
            "enclosure_surface": self.enclosure_surface,
            "boundary_tags": self.boundary_tags,
            "metadata": self.metadata,
        }


def _unit(v: Sequence[float]) -> np.ndarray:
    a = np.asarray(v, dtype=float)
    n = np.linalg.norm(a)
    if n < 1e-15:
        raise ValueError("zero-length axis")
    return a / n


def build_sma_coax_feed(
    feed: Optional[FeedParams] = None,
    enclosure: Optional[FaradayEnclosure] = None,
    geometry_L0_mm: float = 100.0,
) -> FeedTopology:
    """
    Place a single SMA/coax port on the Faraday enclosure so that the
    centre pin points toward the CD-N3 geometric origin.

    The feed does **not** alter pure-geometry parameters (L0, n, s).
    It only adds classical excitation and PEC boundary definitions.
    """
    feed = feed or DEFAULT_FEED
    enclosure = enclosure or DEFAULT_ENCLOSURE

    axis = _unit(feed.port_axis)
    pos = np.asarray(feed.port_position_mm, dtype=float)

    # Pin: solid cylinder along axis, length pin_length, radius inner/2
    pin = {
        "type": "cylinder",
        "axis": axis.tolist(),
        "origin_mm": pos.tolist(),
        "length_mm": feed.pin_length_mm,
        "radius_mm": feed.inner_diameter_mm / 2.0,
        "material": "PEC_conductor",
        "role": "centre_pin",
    }

    # Dielectric annulus between inner and dielectric OD
    dielectric = {
        "type": "annular_cylinder",
        "axis": axis.tolist(),
        "origin_mm": pos.tolist(),
        "length_mm": feed.pin_length_mm + feed.flange_thickness_mm,
        "inner_radius_mm": feed.inner_diameter_mm / 2.0,
        "outer_radius_mm": feed.dielectric_od_mm / 2.0,
        "material": "PTFE_or_vacuum_equivalent",
        "epsilon_r": 2.1,
        "role": "coax_dielectric",
    }

    # Outer conductor
    outer = {
        "type": "annular_cylinder",
        "axis": axis.tolist(),
        "origin_mm": pos.tolist(),
        "length_mm": feed.flange_thickness_mm,
        "inner_radius_mm": feed.dielectric_od_mm / 2.0,
        "outer_radius_mm": feed.outer_diameter_mm / 2.0,
        "material": "PEC_conductor",
        "role": "outer_conductor",
    }

    # Port face: disk at the exterior end of the coax (wave/lumped port)
    port_origin = pos - axis * feed.flange_thickness_mm
    port_face = {
        "type": "disk",
        "centre_mm": port_origin.tolist(),
        "normal": (-axis).tolist(),
        "radius_mm": feed.outer_diameter_mm / 2.0,
        "Z0_ohm": feed.Z0_ohm,
        "role": "wave_port_or_lumped_port",
        "port_index": 1,
        "single_port": True,
    }

    # Faraday enclosure surface
    if enclosure.shape == "cylinder":
        enc = {
            "type": "cylinder_shell",
            "centre_mm": list(enclosure.centre_mm),
            "axis": [0.0, 0.0, 1.0],
            "radius_mm": enclosure.radius_mm,
            "height_mm": enclosure.height_mm,
            "wall_thickness_mm": enclosure.wall_thickness_mm,
            "bc": enclosure.bc_type,
        }
    else:
        enc = {
            "type": "box_shell",
            "centre_mm": list(enclosure.centre_mm),
            "half_extents_mm": [
                enclosure.radius_mm,
                enclosure.radius_mm,
                enclosure.height_mm / 2.0,
            ],
            "wall_thickness_mm": enclosure.wall_thickness_mm,
            "bc": enclosure.bc_type,
        }

    tags = {
        "centre_pin": "boundary:PEC;role=feed_pin;port=1",
        "outer_conductor": "boundary:PEC;role=feed_outer;port=1",
        "port_face": f"boundary:port;Z0={feed.Z0_ohm};port=1;single_port=true",
        "enclosure": f"boundary:{enclosure.bc_type};role=faraday_enclosure",
        "dielectric": "region:dielectric;epsilon_r=2.1;role=coax_fill",
    }

    # Sanity: port should sit on or outside the enclosure wall
    # (soft check — recorded in metadata, not hard-fail for parametric sweeps)
    radial = math.sqrt(pos[0] ** 2 + pos[1] ** 2)
    inside_radial = radial < enclosure.radius_mm - 1.0
    z_extent = enclosure.height_mm / 2.0
    inside_z = abs(pos[2]) < z_extent - 1.0

    topo = FeedTopology(
        feed=feed,
        enclosure=enclosure,
        pin_cylinder=pin,
        dielectric_cylinder=dielectric,
        outer_conductor=outer,
        port_face=port_face,
        enclosure_surface=enc,
        boundary_tags=tags,
        metadata={
            "schema_version": "P0-C.1",
            "geometry_L0_mm_reference": geometry_L0_mm,
            "port_appears_inside_enclosure_volume": bool(inside_radial and inside_z),
            "category_locks": {
                "feed_is_classical_sma_coax": True,
                "ware_modifies_feed": False,
                "single_port_only": True,
                "enclosure_is_explicit_faraday": True,
                "s_used_as_angle": False,
                "theta_0_invented": False,
            },
        },
    )
    return topo
