"""Command-line audit for the momentum-closure sketch.

Prints geometry, feed, and classical far-field fixture numbers.
Does not certify thrust, a Ware momentum flux, or a mesh residual.
"""

from __future__ import annotations

import argparse
import math
import tempfile
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from momentum_closure import __version__
from momentum_closure.convergence.tensor import (
    AxisStatus,
    ConvergenceCertificate,
    ConvergenceTensor,
)
from momentum_closure.fixtures import (
    C_LIGHT_M_S,
    analytic_force_N,
    eta_p,
    eta_p_status,
    even_odd,
    gauss_force_N,
    midpoint_force_N,
    mirror_45_xz,
    rel_err,
    require_nonnegative_pattern,
    InvalidPattern,
)
from momentum_closure.geometry.generator import run_p0_b2
from momentum_closure.geometry.params import BASELINE
from momentum_closure.geometry.rodrigues import threefold_rotations
from momentum_closure.rf_feed.manifest import run_p0_c1

# Declared before any measurement. Not adjusted to force a pass.
MESH_TOLERANCE = 1e-3
RADIATION_TOLERANCE = 1e-9
SURFACE_TOLERANCE = 1e-3

# Fixed fixture from the framework review: P = 1 W, a = 0.9 ẑ.
FIXTURE_POWER_W = 1.0
FIXTURE_A = (0.0, 0.0, 0.9)
MIDPOINT_COARSE = (24, 48)
MIDPOINT_FINE = (96, 192)


def _frobenius(m: np.ndarray) -> float:
    return float(np.linalg.norm(m, ord="fro"))


def build_report(out_dir: str | Path | None = None) -> dict[str, Any]:
    cleanup = None
    if out_dir is None:
        cleanup = tempfile.TemporaryDirectory()
        out = Path(cleanup.name)
    else:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)

    try:
        geo = run_p0_b2(out)
        feed = run_p0_c1(out, geometry_manifest_sha256=geo["manifest_sha256"])
        rotations = threefold_rotations(BASELINE.axis)
        r120 = rotations[1]
        r3_err = _frobenius(r120 @ r120 @ r120 - np.eye(3))

        analytic = analytic_force_N(FIXTURE_POWER_W, FIXTURE_A)
        gauss, power_gauss = gauss_force_N(FIXTURE_POWER_W, FIXTURE_A)
        iso, power_iso = gauss_force_N(FIXTURE_POWER_W, (0.0, 0.0, 0.0))
        coarse, _ = midpoint_force_N(FIXTURE_POWER_W, FIXTURE_A, *MIDPOINT_COARSE)
        fine, _ = midpoint_force_N(FIXTURE_POWER_W, FIXTURE_A, *MIDPOINT_FINE)

        tensor = ConvergenceTensor()
        tensor.declare("mesh", MESH_TOLERANCE)
        tensor.declare("radiation", RADIATION_TOLERANCE)
        tensor.declare("surface", SURFACE_TOLERANCE)
        mesh_eps = tensor.measure("mesh", coarse[2], fine[2])
        rad_eps = tensor.measure("radiation", analytic[2], gauss[2])
        # No second enclosing surface is supplied, so surface stays DECLARED.
        cert = ConvergenceCertificate(tensor, required=("mesh", "surface"))

        cancel = tensor.residual_closure(gauss, tuple(-x for x in gauss), (0.0, 0.0, 0.0), max(abs(gauss[2]), 1e-30))
        unbalanced = tensor.residual_closure(gauss, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), max(abs(gauss[2]), 1e-30))

        try:
            require_nonnegative_pattern((0.0, 0.0, 1.1))
            positivity = "ACCEPTED"
        except InvalidPattern as exc:
            positivity = str(exc)

        mirror = mirror_45_xz()
        probe = np.array([0.2, -0.4, 0.7])
        even, odd = even_odd(probe, mirror)
        mirror_algebra_err = _frobenius(mirror @ mirror - np.eye(3))
        even_err = float(np.linalg.norm(mirror @ even - even))
        odd_err = float(np.linalg.norm(mirror @ odd + odd))

        eta = eta_p(analytic, FIXTURE_POWER_W)
        iso_norm = math.sqrt(sum(x * x for x in iso))
        return {
            "version": __version__,
            "L0_mm": BASELINE.L0_mm,
            "s_scale": BASELINE.s,
            "fold_angle_rad": BASELINE.fold_angle_rad,
            "scale_ladder_mm": list(BASELINE.scale_ladder_mm),
            "rodrigues_R3_minus_I_fro": r3_err,
            "model_count": len(geo["openscad"]),
            "geometry_payload_sha256": geo["manifest_sha256"],
            "Z0_ohm": feed["Z0_ohm"],
            "port_position_mm": list(feed["port_position_mm"]),
            "enclosure_bc": feed["enclosure_bc"],
            "ware_modifies_feed": bool(feed["category_locks"]["ware_modifies_feed"]),
            "single_port": bool(feed["category_locks"]["single_port_only"]),
            "port_inside_enclosure": _port_inside(out),
            "feed_payload_sha256": feed["manifest_sha256"],
            "P_W": FIXTURE_POWER_W,
            "a_z": FIXTURE_A[2],
            "c_m_s": C_LIGHT_M_S,
            "Fz_analytic_N": analytic[2],
            "Fz_gauss_N": gauss[2],
            "Fx_gauss_N": gauss[0],
            "Fy_gauss_N": gauss[1],
            "rel_err_gauss": rel_err(gauss[2], analytic[2]),
            "power_gauss_W": power_gauss,
            "power_isotropic_W": power_iso,
            "Fz_midpoint_coarse_N": coarse[2],
            "Fz_midpoint_fine_N": fine[2],
            "midpoint_mesh_epsilon": mesh_eps,
            "mesh_tolerance_declared": MESH_TOLERANCE,
            "mesh_status": tensor.status("mesh").value,
            "radiation_epsilon": rad_eps,
            "radiation_tolerance_declared": RADIATION_TOLERANCE,
            "radiation_status": tensor.status("radiation").value,
            "surface_status": tensor.status("surface").value,
            "eta_p_analytic": eta,
            "eta_p_status": eta_p_status(eta),
            "isotropic_F_norm_N": iso_norm,
            "positivity_a_1_1": positivity,
            "pair_cancel_residual": cancel,
            "unbalanced_residual": unbalanced,
            "mirror45_M2_err": mirror_algebra_err,
            "mirror45_even_err": even_err,
            "mirror45_odd_err": odd_err,
            "certificate": cert.reason(),
            "certifies_physical_residual": False,
            "out_dir": str(out if out_dir is not None else ""),
        }
    finally:
        if cleanup is not None:
            cleanup.cleanup()


def _port_inside(out: Path) -> bool:
    import json

    payload = json.loads((out / "CD-N3_feed_faraday_manifest.json").read_text())
    return bool(payload["topology"]["metadata"]["port_appears_inside_enclosure_volume"])


def format_report(r: Mapping[str, Any]) -> str:
    ladder = ",".join(f"{x:.6f}" for x in r["scale_ladder_mm"])
    port = ",".join(f"{x:.6f}" for x in r["port_position_mm"])
    lines = [
        f"momentum-closure {r['version']}",
        "classification=RESEARCH",
        "claim_level=1",
        "physical_thrust=UNSUPPORTED",
        "ware_momentum_flux=UNSUPPORTED",
        "mesh_converged_residual=UNSUPPORTED",
        "energy_extraction=UNSUPPORTED",
        "",
        "[geometry]",
        f"L0_mm={r['L0_mm']:.6f}",
        f"s_scale={r['s_scale']:.6f}",
        "s_is_angle=false",
        f"fold_angle_rad={r['fold_angle_rad']:.12f}",
        f"fold_equals_s={str(math.isclose(r['fold_angle_rad'], r['s_scale'])).lower()}",
        f"scale_ladder_mm={ladder}",
        f"rodrigues_R3_minus_I_fro={r['rodrigues_R3_minus_I_fro']:.6e}",
        f"model_count={r['model_count']}",
        f"geometry_payload_sha256={r['geometry_payload_sha256']}",
        "",
        "[feed]",
        f"Z0_ohm={r['Z0_ohm']}",
        f"port_position_mm={port}",
        f"port_inside_enclosure={str(r['port_inside_enclosure']).lower()}",
        f"single_port={str(r['single_port']).lower()}",
        f"enclosure_bc={r['enclosure_bc']}",
        f"ware_modifies_feed={str(r['ware_modifies_feed']).lower()}",
        f"feed_payload_sha256={r['feed_payload_sha256']}",
        "",
        "[radiation_fixture]",
        "pattern=P/4pi*(1+a·rhat)",
        "note=classical_far_field_identity_not_a_device",
        f"P_W={r['P_W']}",
        f"a_z={r['a_z']}",
        f"c_m_s={r['c_m_s']}",
        f"Fz_analytic_N={r['Fz_analytic_N']:.12e}",
        f"Fz_gauss_N={r['Fz_gauss_N']:.12e}",
        f"Fx_gauss_N={r['Fx_gauss_N']:.12e}",
        f"Fy_gauss_N={r['Fy_gauss_N']:.12e}",
        f"rel_err_gauss={r['rel_err_gauss']:.6e}",
        f"power_gauss_W={r['power_gauss_W']:.12f}",
        f"Fz_midpoint_coarse_N={r['Fz_midpoint_coarse_N']:.12e}",
        f"Fz_midpoint_fine_N={r['Fz_midpoint_fine_N']:.12e}",
        f"midpoint_mesh_epsilon={r['midpoint_mesh_epsilon']:.12e}",
        f"mesh_tolerance_declared={r['mesh_tolerance_declared']:.6e}",
        f"mesh_status={r['mesh_status']}",
        f"eta_p_analytic={r['eta_p_analytic']:.6f}",
        f"eta_p_status={r['eta_p_status']}",
        f"isotropic_F_norm_N={r['isotropic_F_norm_N']:.12e}",
        f"power_isotropic_W={r['power_isotropic_W']:.12f}",
        f"positivity_a_1_1={r['positivity_a_1_1']}",
        f"pair_cancel_residual={r['pair_cancel_residual']:.12e}",
        f"unbalanced_residual={r['unbalanced_residual']:.12e}",
        "",
        "[mirror]",
        "operator=householder_normal_45deg_xz",
        f"mirror45_M2_err={r['mirror45_M2_err']:.6e}",
        f"mirror45_even_err={r['mirror45_even_err']:.6e}",
        f"mirror45_odd_err={r['mirror45_odd_err']:.6e}",
        "",
        "[convergence]",
        f"radiation_epsilon={r['radiation_epsilon']:.6e}",
        f"radiation_tolerance_declared={r['radiation_tolerance_declared']:.6e}",
        f"radiation_status={r['radiation_status']}",
        f"surface_status={r['surface_status']}",
        "surface_measured=false",
        f"certificate={r['certificate']}",
        "certifies_physical_residual=false",
        "",
        "not_thrust=true",
        "not_propulsion=true",
        "not_completed_physical_law=true",
    ]
    if r["mesh_status"] != AxisStatus.FAILED.value:
        lines.append(f"mesh_status_unexpected={r['mesh_status']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit CD-N3 geometry, the SMA/coax feed, and the classical "
            "far-field fixture F = P a / (3c). Does not claim thrust."
        )
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Directory for JSON manifests and OpenSCAD (default: temporary)",
    )
    args = parser.parse_args(argv)
    print(format_report(build_report(args.out)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
