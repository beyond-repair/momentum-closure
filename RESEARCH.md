# RESEARCH lock — momentum-closure

Sweep-158 (2026-09-20). Governing source: `beyond-repair/ADL-Governance`.

This repository is a **Coherence Drive / Ware program satellite**: conceptual momentum-closure notes plus a Python package for numerical convergence bookkeeping.

## What is here

- Surface-integral discipline statement (`COMPATIBLE_CLOSURE.md`).
- Geometry helpers under `momentum_closure/geometry/`.
- RF-feed helpers under `momentum_closure/rf_feed/`.
- Multidimensional convergence tensor (`momentum_closure/convergence/tensor.py`) for declaring tolerances before measurement and recording numerical closure status only.
- Unit tests (`tests/test_convergence_tensor.py`) — 4 passed locally.
- Docs-presence CI workflow.

## What is not here

- No mesh-converged residual force demonstration.
- No physical thrust claim.
- No full-wave / BEM adapter.
- No product releases / tags.
- No claim elevation beyond Level 1 (mathematical / conceptual framework).

Runnable evaluators live in `stress-tensor-modification`. Program index: `coherence-drive`.

**Claim level remains 1.** Do not promote to ACTIVE until higher-evidence gates (if ever) are met under ADL-Governance.
