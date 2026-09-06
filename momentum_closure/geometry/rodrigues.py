"""Rodrigues rotation matrices for discrete n-fold symmetry.

The only angular degree of freedom admitted in the pure-geometry layer
is the canonical fold angle 2π/n.  The recursive scale factor s is never
passed into these routines.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np


def rodriques_matrix(
    axis: Sequence[float],
    angle_rad: float,
) -> np.ndarray:
    """
    Rodrigues' rotation formula.

        R = I cos θ + (a a^T)(1 - cos θ) + [a]_× sin θ

    Parameters
    ----------
    axis : length-3 unit (or will be normalised) vector â
    angle_rad : rotation angle in *radians* (must be the fold angle, not s)
    """
    a = np.asarray(axis, dtype=float)
    nrm = np.linalg.norm(a)
    if nrm < 1e-15:
        raise ValueError("symmetry axis has vanishing norm")
    a = a / nrm
    K = np.array(
        [
            [0.0, -a[2], a[1]],
            [a[2], 0.0, -a[0]],
            [-a[1], a[0], 0.0],
        ],
        dtype=float,
    )
    I = np.eye(3)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    R = I * c + np.outer(a, a) * (1.0 - c) + K * s
    return R


def threefold_rotations(axis: Sequence[float] = (0.0, 0.0, 1.0)) -> List[np.ndarray]:
    """
    Return {I, R(120°), R(240°)} about â.

    These are the *only* discrete rotational images used for the
    CD-N3 baseline.  The scale factor s does not appear.
    """
    import math
    theta = 2.0 * math.pi / 3.0
    R1 = rodriques_matrix(axis, theta)
    R2 = rodriques_matrix(axis, 2.0 * theta)
    I = np.eye(3)
    return [I, R1, R2]


def apply_rotation(R: np.ndarray, points: np.ndarray) -> np.ndarray:
    """Apply 3×3 rotation to an (N, 3) point cloud."""
    return (R @ points.T).T
