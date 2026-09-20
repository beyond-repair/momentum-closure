# Claims — momentum-closure (Sweep-158)

**Classification:** RESEARCH  
**Claim level:** 1 (conceptual / mathematical framework)  
**Governing source:** beyond-repair/ADL-Governance

## Hierarchy

Code > documentation > roadmap.

## Verified this cycle (tree + local pytest)

| Feature | State |
|---------|-------|
| RESEARCH classification badge in README | VERIFIED (docs) |
| Geometry package blobs (`momentum_closure/geometry/*.py`) | VERIFIED present |
| RF-feed helpers | VERIFIED present |
| `COMPATIBLE_CLOSURE.md` surface-integral statement | VERIFIED (docs) |
| `momentum_closure/convergence/tensor.py` | **VERIFIED present** |
| `tests/test_convergence_tensor.py` | **VERIFIED present** (4 passed) |
| Import `from momentum_closure import ConvergenceTensor` | **VERIFIED** |
| Docs-presence workflow | VERIFIED present |
| Releases / tags | NONE |
| Mesh-converged residual / physical thrust | **FORBIDDEN / not claimed** |

## Planned (explicit, not implemented here)

| Feature | State |
|---------|-------|
| Fail-closed certification state machine beyond unit tests | PLANNED |
| Full-wave / BEM adapter (v1.8+) | PLANNED |
| Product residual CI | PLANNED (only if claim level rises with evidence) |

## Rule

Do not treat any README row as evidence of physical residual. ConvergenceTensor records numerical tolerances and status only; it never certifies a physical force.
