# Claims — momentum-closure (Sweep-083)

**Classification:** RESEARCH  
**Claim level:** 1 (conceptual) unless a blob is present and executable  
**Census SHA (tree):** `ba13d1b9850df7a39371ffdcaa4809ab5d226955` before this lock

## Hierarchy

Code > documentation > roadmap.

## Verified this cycle (tree + Actions API)

| Feature | State |
|---------|-------|
| RESEARCH classification badge in README | VERIFIED (docs) |
| Geometry package blobs (`momentum_closure/geometry/*.py`) | VERIFIED present |
| `COMPATIBLE_CLOSURE.md` surface-integral statement | VERIFIED (docs) |
| GitHub Actions workflows | NONE (`list_workflows` total_count=0) |
| Releases / tags | NONE |
| `momentum_closure/convergence/tensor.py` | **ABSENT** |
| `tests/test_convergence_tensor.py` | **ABSENT** |
| pytest “21 passed” | **UNVERIFIED** (no test tree; no CI) |
| Import `from momentum_closure import ConvergenceTensor` | **BROKEN** — `__init__.py` imports missing `tensor` |
| Mesh-converged residual / physical thrust | **FORBIDDEN / not claimed** |

## Planned (explicit, not implemented here)

| Feature | State |
|---------|-------|
| Convergence tensor module | PLANNED |
| Fail-closed certification state machine | PLANNED (specified in docs only) |
| Full-wave / BEM adapter (v1.8) | PLANNED |
| Product CI | PLANNED (do not add until tensor + tests exist) |

## Rule

Do not treat README “Implemented” rows as evidence. Until `tensor.py` and tests exist on `main`, those rows are **UNVERIFIED**.
