# RESEARCH lock — momentum-closure

Sweep-158 (2026-09-20). Governing source: `beyond-repair/ADL-Governance`.

This repository is a **Coherence Drive / Ware program satellite**: conceptual momentum-closure notes plus a Python package for numerical convergence bookkeeping.

## What is here

- Surface-integral discipline statement (`COMPATIBLE_CLOSURE.md`).
- Geometry helpers under `momentum_closure/geometry/`.
- RF-feed helpers under `momentum_closure/rf_feed/`.
- Multidimensional convergence tensor (`momentum_closure/convergence/tensor.py`) for declaring tolerances before measurement and recording numerical closure status only.
- Unit tests under `tests/` for the tensor, geometry/feed, and the classical far-field fixture.
- Console script `momentum-closure` (install with `pip install -e ".[dev]"`). It prints a midpoint-mesh **failure** against declared tolerance `1e-3`. That miss is kept.
- Docs-presence CI workflow.

## What is not here

- No mesh-converged residual force demonstration. The midpoint fixture comparison fails its declared tolerance on purpose; it is not retuned.
- No physical thrust claim. `F = 0.9/(3c)` is ordinary radiation recoil of a 1 W dipole pattern, not a drive.
- No full-wave / BEM adapter.
- No product releases / tags.
- No claim elevation beyond Level 1 (mathematical / conceptual framework).

Runnable evaluators live in `stress-tensor-modification`. Program index: `coherence-drive`.

**Claim level remains 1.** Do not promote to ACTIVE until higher-evidence gates (if ever) are met under ADL-Governance.
