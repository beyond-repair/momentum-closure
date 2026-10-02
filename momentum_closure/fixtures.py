"""Classical far-field radiation fixtures.

These are the analytic identities in docs/MOMENTUM_CLOSURE_FRAMEWORK_REVIEW.md
(section 2.2). They check quadrature against

    F = P a / (3 c)

for dP/dΩ = (P/4π) (1 + a · r̂), |a| ≤ 1.

They are not a device, not a Ware term, and not a thrust measurement.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

import numpy as np

# Exact SI speed of light (m/s). Not a fitted constant.
C_LIGHT_M_S = 299_792_458.0

Vector = Tuple[float, float, float]


class InvalidPattern(ValueError):
    """Pattern can go negative. Spec token: INVALID_INPUT."""


def _as_vec(a: Sequence[float]) -> Vector:
    if len(a) != 3:
        raise ValueError("a must have length 3")
    return (float(a[0]), float(a[1]), float(a[2]))


def pattern_amplitude(a: Sequence[float]) -> float:
    x, y, z = _as_vec(a)
    return math.sqrt(x * x + y * y + z * z)


def require_nonnegative_pattern(a: Sequence[float]) -> Vector:
    """|a| ≤ 1 is sufficient for 1 + a·r̂ ≥ 0 on the sphere."""
    vec = _as_vec(a)
    if pattern_amplitude(vec) > 1.0 + 1e-12:
        raise InvalidPattern("INVALID_INPUT")
    return vec


def analytic_force_N(power_W: float, a: Sequence[float]) -> Vector:
    """Closed form F = P a / (3 c). Rejects |a| > 1 before evaluation."""
    if power_W < 0.0:
        raise ValueError("power must be non-negative")
    x, y, z = require_nonnegative_pattern(a)
    scale = power_W / (3.0 * C_LIGHT_M_S)
    return (scale * x, scale * y, scale * z)


def eta_p(force_N: Sequence[float], power_W: float) -> float:
    """η_p = c |F| / P. Greater than 1 is a diagnostic, not an anomaly claim."""
    if power_W <= 0.0:
        raise ValueError("power must be positive")
    x, y, z = _as_vec(force_N)
    mag = math.sqrt(x * x + y * y + z * z)
    return C_LIGHT_M_S * mag / power_W


def eta_p_status(eta: float) -> str:
    if eta > 1.0 + 1e-9:
        return "INVALID_INVESTIGATE"
    if eta >= 0.99:
        return "HIGHLY_COLLIMATED"
    return "ORDINARY_DIRECTIONAL"


def gauss_force_N(
    power_W: float,
    a: Sequence[float],
    n_u: int = 4,
    n_phi: int = 16,
) -> tuple[Vector, float]:
    """Momentum flux (1/c) ∫ (dP/dΩ) r̂ dΩ by Gauss–Legendre in u=cos θ.

    The integrand is a trigonometric polynomial of low degree, so a small
    rule is spectrally accurate. This does not refine a device mesh.
    """
    vec = require_nonnegative_pattern(a)
    if n_u < 2 or n_phi < 4:
        raise ValueError("quadrature rule is too small")
    nodes, weights = np.polynomial.legendre.leggauss(n_u)
    dphi = 2.0 * math.pi / n_phi
    acc = np.zeros(3)
    power = 0.0
    ax, ay, az = vec
    for u, w in zip(nodes, weights):
        st = math.sqrt(max(0.0, 1.0 - float(u) * float(u)))
        for j in range(n_phi):
            phi = (j + 0.5) * dphi
            nx = st * math.cos(phi)
            ny = st * math.sin(phi)
            nz = float(u)
            dPdO = (power_W / (4.0 * math.pi)) * (1.0 + ax * nx + ay * ny + az * nz)
            dP = dPdO * float(w) * dphi
            power += dP
            acc[0] += dP * nx
            acc[1] += dP * ny
            acc[2] += dP * nz
    acc /= C_LIGHT_M_S
    return (float(acc[0]), float(acc[1]), float(acc[2])), float(power)


def midpoint_force_N(
    power_W: float,
    a: Sequence[float],
    n_theta: int,
    n_phi: int,
) -> tuple[Vector, float]:
    """Same integral with a midpoint Riemann sum. Converges slowly."""
    vec = require_nonnegative_pattern(a)
    if n_theta < 2 or n_phi < 4:
        raise ValueError("quadrature rule is too small")
    dtheta = math.pi / n_theta
    dphi = 2.0 * math.pi / n_phi
    acc = np.zeros(3)
    power = 0.0
    ax, ay, az = vec
    for i in range(n_theta):
        theta = (i + 0.5) * dtheta
        st = math.sin(theta)
        ct = math.cos(theta)
        for j in range(n_phi):
            phi = (j + 0.5) * dphi
            nx = st * math.cos(phi)
            ny = st * math.sin(phi)
            nz = ct
            dPdO = (power_W / (4.0 * math.pi)) * (1.0 + ax * nx + ay * ny + az * nz)
            dP = dPdO * st * dtheta * dphi
            power += dP
            acc[0] += dP * nx
            acc[1] += dP * ny
            acc[2] += dP * nz
    acc /= C_LIGHT_M_S
    return (float(acc[0]), float(acc[1]), float(acc[2])), float(power)


def rel_err(measured: float, reference: float) -> float:
    return abs(measured - reference) / max(abs(reference), 1e-30)


def mirror_matrix(normal: Sequence[float]) -> np.ndarray:
    """Householder reflection. M² = I. Normal need not be a unit vector."""
    n = np.asarray(normal, dtype=float)
    nrm = np.linalg.norm(n)
    if nrm < 1e-15:
        raise ValueError("mirror normal has vanishing norm")
    n = n / nrm
    return np.eye(3) - 2.0 * np.outer(n, n)


def mirror_45_xz() -> np.ndarray:
    """Reflection through the plane whose normal is 45° in the xz plane."""
    s = math.sqrt(0.5)
    return mirror_matrix((s, 0.0, s))


def even_odd(vector: Sequence[float], mirror: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    v = np.asarray(vector, dtype=float)
    mv = mirror @ v
    return 0.5 * (v + mv), 0.5 * (v - mv)
