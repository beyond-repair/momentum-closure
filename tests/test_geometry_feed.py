"""Geometry category locks and classical SMA/coax feed."""

import math
from pathlib import Path

import pytest

pytest.importorskip("numpy")

import numpy as np

from momentum_closure.geometry.generator import generate_baseline, run_p0_b2
from momentum_closure.geometry.params import GeometryParams
from momentum_closure.geometry.rodrigues import rodriques_matrix, threefold_rotations
from momentum_closure.rf_feed.manifest import run_p0_c1
from momentum_closure.rf_feed.params import FaradayEnclosure, FeedParams
from momentum_closure.rf_feed.topology import build_sma_coax_feed


def test_s_is_scale_not_fold_angle():
    params = GeometryParams()
    assert params.s == pytest.approx(0.45)
    assert params.fold_angle_rad == pytest.approx(2.0 * math.pi / 3.0)
    assert not math.isclose(params.s, params.fold_angle_rad)
    locks = params.to_dict()["category_locks"]
    assert locks["s_is_not_angle"] is True
    assert locks["ware_modifies_geometry"] is False
    with pytest.raises(ValueError):
        GeometryParams(n=4)
    with pytest.raises(ValueError):
        GeometryParams(s=1.2)


def test_rodrigues_order_three_about_z():
    rotations = threefold_rotations((0.0, 0.0, 1.0))
    r120 = rotations[1]
    assert np.allclose(r120 @ r120 @ r120, np.eye(3), atol=1e-12)
    assert np.allclose(rotations[2], r120 @ r120, atol=1e-12)
    # s is not an argument of the rotation.
    direct = rodriques_matrix((0.0, 0.0, 1.0), 2.0 * math.pi / 3.0)
    assert np.allclose(direct, r120, atol=1e-12)


def test_baseline_models_and_manifest(tmp_path: Path):
    models = generate_baseline()
    assert [m.model_id for m in models] == ["CD-N3-P", "CD-N3-M", "CD-N3-N"]
    signs = [m.metadata["polarity_sign"] for m in models]
    assert signs == [1.0, -1.0, 0.0]
    # Mirror variant flips the y coordinate of the level-0 sector-0 triangle.
    p = np.array(models[0].vertices_mm["level0_sector0"])
    m = np.array(models[1].vertices_mm["level0_sector0"])
    assert np.allclose(m[:, 1], -p[:, 1])
    result = run_p0_b2(tmp_path)
    assert Path(result["manifest"]).is_file()
    assert len(result["manifest_sha256"]) == 64
    assert len(result["openscad"]) == 3
    assert result["scale_ladder_mm"] == pytest.approx([100.0, 45.0, 20.25, 9.1125])


def test_feed_is_single_port_classical(tmp_path: Path):
    topo = build_sma_coax_feed()
    assert topo.feed.Z0_ohm == pytest.approx(50.0)
    assert topo.port_face["single_port"] is True
    assert topo.port_face["port_index"] == 1
    assert topo.enclosure.bc_type == "PEC"
    assert topo.metadata["category_locks"]["ware_modifies_feed"] is False
    assert topo.metadata["port_appears_inside_enclosure_volume"] is False
    with pytest.raises(ValueError):
        FeedParams(inner_diameter_mm=5.0, outer_diameter_mm=4.0)
    with pytest.raises(ValueError):
        FaradayEnclosure(shape="sphere")
    result = run_p0_c1(tmp_path, geometry_manifest_sha256="abc")
    assert Path(result["manifest"]).is_file()
    assert Path(result["openscad"]).is_file()
    assert result["Z0_ohm"] == pytest.approx(50.0)
    assert result["enclosure_bc"] == "PEC"
