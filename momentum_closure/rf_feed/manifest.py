"""Emit P0-C.1 feed + Faraday enclosure manifest and OpenSCAD preview."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..geometry.params import BASELINE
from .params import DEFAULT_ENCLOSURE, DEFAULT_FEED, FaradayEnclosure, FeedParams
from .topology import FeedTopology, build_sma_coax_feed


def emit_feed_manifest(
    topology: FeedTopology,
    path: Path | str,
    geometry_manifest_sha256: Optional[str] = None,
) -> str:
    """Write machine-readable feed manifest; return SHA-256."""
    path = Path(path)
    payload: Dict[str, Any] = {
        "schema_version": "P0-C.1",
        "phase": "P0-C.1",
        "description": (
            "Single-port SMA/coax feed into explicit Faraday (PEC) enclosure. "
            "Classical Maxwell baseline only. Ware layer does not modify feed "
            "or enclosure. Geometry scale factor s is not used as an angle."
        ),
        "geometry_reference": {
            "L0_mm": BASELINE.L0_mm,
            "n": BASELINE.n,
            "s_scale_only": BASELINE.s,
            "models": list(BASELINE.models),
            "geometry_manifest_sha256": geometry_manifest_sha256,
        },
        "topology": topology.to_dict(),
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    payload["manifest_sha256"] = digest
    text = json.dumps(payload, indent=2, sort_keys=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return digest


def emit_feed_openscad(
    topology: FeedTopology,
    path: Path | str,
) -> None:
    """Minimal OpenSCAD preview of enclosure + coax port."""
    path = Path(path)
    f = topology.feed
    e = topology.enclosure
    lines = [
        f"// Auto-generated P0-C.1 — SMA/coax feed + Faraday enclosure",
        f"// Z0 = {f.Z0_ohm} ohm, single port, classical baseline only",
        f"// ware_modifies_feed = false",
        "",
        f"enc_r = {e.radius_mm};",
        f"enc_h = {e.height_mm};",
        f"wall = {e.wall_thickness_mm};",
        f"pin_r = {f.inner_diameter_mm / 2.0};",
        f"pin_len = {f.pin_length_mm};",
        f"outer_r = {f.outer_diameter_mm / 2.0};",
        f"diel_r = {f.dielectric_od_mm / 2.0};",
        f"flange = {f.flange_thickness_mm};",
        f"port_z = {f.port_position_mm[2]};",
        "",
        "// Faraday enclosure (transparent shell for preview)",
        "difference() {",
        "  cylinder(h = enc_h, r = enc_r, center = true);",
        "  cylinder(h = enc_h - 2*wall, r = enc_r - wall, center = true);",
        "}",
        "",
        "// Coax port at bottom",
        "translate([0, 0, port_z]) {",
        "  // centre pin",
        "  color(\"gold\") cylinder(h = pin_len, r = pin_r);",
        "  // outer conductor flange",
        "  color(\"silver\") difference() {",
        "    cylinder(h = flange, r = outer_r);",
        "    translate([0,0,-0.1]) cylinder(h = flange + 0.2, r = diel_r);",
        "  }",
        "}",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def run_p0_c1(
    out_dir: Path | str = "geometry_out",
    feed: Optional[FeedParams] = None,
    enclosure: Optional[FaradayEnclosure] = None,
    geometry_manifest_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """P0-C.1 entry point: build feed topology and emit manifests."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    topo = build_sma_coax_feed(
        feed=feed,
        enclosure=enclosure,
        geometry_L0_mm=BASELINE.L0_mm,
    )
    manifest_path = out / "CD-N3_feed_faraday_manifest.json"
    digest = emit_feed_manifest(
        topo,
        manifest_path,
        geometry_manifest_sha256=geometry_manifest_sha256,
    )
    scad_path = out / "CD-N3_feed_faraday.scad"
    emit_feed_openscad(topo, scad_path)

    return {
        "manifest": str(manifest_path),
        "manifest_sha256": digest,
        "openscad": str(scad_path),
        "Z0_ohm": topo.feed.Z0_ohm,
        "port_position_mm": list(topo.feed.port_position_mm),
        "enclosure_bc": topo.enclosure.bc_type,
        "category_locks": topo.metadata["category_locks"],
    }
