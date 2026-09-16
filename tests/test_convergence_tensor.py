import math
import pytest

from momentum_closure.convergence.tensor import (
    AxisStatus,
    ConvergenceCertificate,
    ConvergenceTensor,
)


def test_declare_before_measure():
    C = ConvergenceTensor()
    with pytest.raises(RuntimeError):
        C.measure("mesh", 1.0, 1.1)


def test_mesh_and_surface_pass():
    C = ConvergenceTensor()
    C.declare("mesh", 0.05)
    C.declare("surface", 0.05)
    assert C.measure("mesh", 1.00, 1.01, floor=1e-12) < 0.05
    assert C.measure("surface", 1.00, 1.02, floor=1e-12) < 0.05
    cert = ConvergenceCertificate(C)
    assert cert.certified()
    assert C.status("timestep") == AxisStatus.MISSING


def test_closure_residual_definition():
    C = ConvergenceTensor()
    eps = C.residual_closure(
        F_near=(1.0, 0.0, 0.0),
        F_far=(-1.0, 0.0, 0.0),
        Pdot_matter=(0.0, 0.0, 0.0),
        P_scale=1.0,
    )
    assert eps < 1e-15
    eps_bad = C.residual_closure((1.0, 0, 0), (0, 0, 0), (0, 0, 0), 1.0)
    assert math.isclose(eps_bad, 1.0)


def test_radiation_fixture_scale():
    c = 299792458.0
    F = 0.9 / (3.0 * c)
    assert abs(F - 1.00069e-9) / 1.00069e-9 < 5e-5
