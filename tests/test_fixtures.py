"""Classical fixture checks. Tolerances are not fitted to a claimed thrust."""

import math

import pytest

pytest.importorskip("numpy")

from momentum_closure.convergence.tensor import ConvergenceTensor
from momentum_closure.fixtures import (
    C_LIGHT_M_S,
    InvalidPattern,
    analytic_force_N,
    eta_p,
    eta_p_status,
    even_odd,
    gauss_force_N,
    midpoint_force_N,
    mirror_45_xz,
    rel_err,
)
from momentum_closure.cli import (
    MESH_TOLERANCE,
    build_report,
    format_report,
)


def test_dipole_analytic_target_from_review():
    fz = analytic_force_N(1.0, (0.0, 0.0, 0.9))[2]
    # Review quotes ≈ 1.00069e-9 N. The exact value is 0.9/(3c).
    assert fz == pytest.approx(0.9 / (3.0 * C_LIGHT_M_S))
    assert abs(fz - 1.00069e-9) / 1.00069e-9 < 5e-5


def test_gauss_matches_analytic_not_by_refit():
    a = (0.2, -0.3, 0.4)
    analytic = analytic_force_N(1.0, a)
    gauss, power = gauss_force_N(1.0, a)
    for g, an in zip(gauss, analytic):
        assert rel_err(g, an) < 1e-12
    assert power == pytest.approx(1.0, abs=1e-12)


def test_midpoint_mesh_misses_declared_tolerance():
    analytic_z = analytic_force_N(1.0, (0.0, 0.0, 0.9))[2]
    coarse, _ = midpoint_force_N(1.0, (0.0, 0.0, 0.9), 24, 48)
    fine, _ = midpoint_force_N(1.0, (0.0, 0.0, 0.9), 96, 192)
    tensor = ConvergenceTensor()
    tensor.declare("mesh", MESH_TOLERANCE)
    eps = tensor.measure("mesh", coarse[2], fine[2])
    assert eps > MESH_TOLERANCE
    assert tensor.status("mesh").value == "FAILED"
    # Fine grid is closer than coarse, but neither is forced onto the target.
    assert rel_err(fine[2], analytic_z) < rel_err(coarse[2], analytic_z)
    assert rel_err(fine[2], analytic_z) > 1e-6


def test_isotropic_force_is_numerical_noise():
    force, power = gauss_force_N(1.0, (0.0, 0.0, 0.0))
    norm = math.sqrt(sum(x * x for x in force))
    assert norm < 1e-18
    assert power == pytest.approx(1.0, abs=1e-12)


def test_positivity_rejects_before_evaluation():
    with pytest.raises(InvalidPattern, match="INVALID_INPUT"):
        analytic_force_N(1.0, (0.0, 0.0, 1.1))
    with pytest.raises(InvalidPattern, match="INVALID_INPUT"):
        gauss_force_N(1.0, (0.9, 0.9, 0.0))


def test_eta_p_is_ordinary_not_above_one():
    force = analytic_force_N(1.0, (0.0, 0.0, 0.9))
    eta = eta_p(force, 1.0)
    assert eta == pytest.approx(0.3)
    assert eta_p_status(eta) == "ORDINARY_DIRECTIONAL"
    assert eta_p_status(1.5) == "INVALID_INVESTIGATE"


def test_mirror_45_is_involutive():
    import numpy as np

    mirror = mirror_45_xz()
    assert np.linalg.norm(mirror @ mirror - np.eye(3)) < 1e-12
    even, odd = even_odd((0.2, -0.4, 0.7), mirror)
    assert np.linalg.norm(mirror @ even - even) < 1e-12
    assert np.linalg.norm(mirror @ odd + odd) < 1e-12


def test_report_does_not_certify_thrust():
    report = build_report()
    text = format_report(report)
    assert report["mesh_status"] == "FAILED"
    assert report["radiation_status"] == "PASSED"
    assert report["surface_status"] == "DECLARED"
    assert report["certificate"].startswith("NOT_CERTIFIED")
    assert report["certifies_physical_residual"] is False
    assert "physical_thrust=UNSUPPORTED" in text
    assert "ware_momentum_flux=UNSUPPORTED" in text
    assert "not_thrust=true" in text
    assert report["pair_cancel_residual"] < 1e-12
    assert report["unbalanced_residual"] == pytest.approx(1.0, abs=1e-9)
    assert report["port_inside_enclosure"] is False
    assert report["fold_angle_rad"] == pytest.approx(2.0 * math.pi / 3.0)
    assert report["scale_ladder_mm"] == pytest.approx([100.0, 45.0, 20.25, 9.1125])
