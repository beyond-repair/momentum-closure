"""Pure geometry layer for Coherence Drive N=3 baseline (P0-B.2).

Category rules (locked):
  - s = 0.45 is a non-dimensional *scale factor only*.
  - s is never an angle. θ0 is not invented.
  - 3-fold symmetry is realized solely by Rodrigues R(120°) about â.
  - Classical Maxwell baseline must not be polluted by Ware parameters.
"""

from .params import GeometryParams, MANIFEST_SCHEMA_VERSION
from .rodrigues import rodriques_matrix, threefold_rotations
from .generator import (
    GeometryInstance,
    generate_baseline,
    emit_manifest,
    emit_openscad,
)

__all__ = [
    "GeometryParams",
    "MANIFEST_SCHEMA_VERSION",
    "rodriques_matrix",
    "threefold_rotations",
    "GeometryInstance",
    "generate_baseline",
    "emit_manifest",
    "emit_openscad",
]
