<div align="center">

# Momentum Closure

### Why a residual force, if any, must show up as a **surface integral**

[![RESEARCH](https://img.shields.io/badge/classification-RESEARCH-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/claim_level_1-conceptual-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Status](https://img.shields.io/badge/framework-v1.7_spec-blue?style=for-the-badge)](#momentum-closure-framework-v12--v17)

</div>

---

## Why this exists

People hear “Ware term” and imagine free energy.  
**Momentum closure** is the discipline layer: if the model produces a net push, it must appear as a **non-canceling boundary flux** of an effective stress tensor — not as a verbal miracle.

## Why you need it

| Need | Use this repo |
|------|----------------|
| Understand the residual-force *story* | Surface form of \\(\\mathbf{F}\\) |
| Avoid false “proofs” | Notes only — **no** converged physical residual here |
| Find working code | Go to **stress-tensor-modification** |
| Physics-integrity / certification framework | See [Framework v1.2–v1.7](#momentum-closure-framework-v12--v17) below |
| Multidimensional convergence tensor | [`momentum_closure/convergence/`](momentum_closure/convergence/) |

## How it works (conceptual)

$$
\\mathbf{F}_{\\rm surface} = \\oint T_{\\rm eff}^{ij}\\, dA_j
$$

with

$$
T_{\\rm eff} = T_{\\rm EM} + W(n)\\,\\chi_{\\rm vac}\\,(\\nabla\\Psi_{\\rm info})
$$

(as frozen in [MATH_THEORY_CLOSURE](https://github.com/beyond-repair/coherence-drive/blob/main/docs/MATH_THEORY_CLOSURE.md)).

**Status:** conceptual notes + evolving certification architecture + **implemented convergence tensor**. **No** mesh-converged residual demonstration in this repository. **No** released physical thrust claim.

## Related

- Evaluators: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)  
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)

---

## Momentum Closure Framework (v1.2 → v1.7)

### Implementation status

| Component | Status |
|-----------|--------|
| Field representation + SI dimensional checks | Specified (v1.6) |
| Single-channel momentum ledger | Specified |
| Formal involutive ±45° mirror + even/odd | Specified |
| Analytic radiation fixtures + positivity | Specified |
| Fail-closed certification state machine | Specified |
| **Multidimensional convergence tensor** | **Implemented** — `momentum_closure/convergence/tensor.py` |
| Surface-invariance pairwise ε metric | **Implemented** (inside ConvergenceTensor) |
| Regression tests (convergence) | **21 passed** |
| Full-wave / BEM adapter | Next (v1.8) |

### Convergence tensor (v1.7)

Axes: `h` (mesh), `R` (surface radius), `Δθ` (angular), `Δf` (frequency), `BC`, `τ` (solver tol), `Δt` (timestep).

Fail-closed rules:
- Tolerances declared **before** evaluation
- Missing evidence → `NOT_CERTIFIED` (never implicit PASS)
- Force residual always a 3-vector (no premature scalar collapse)
- Surface invariance: `max ε_ij ≤ ε_surface`
- Certificate sealed with SHA-256 evidence hash

```python
from momentum_closure import ConvergenceTensor, ConvergenceAxis

t = ConvergenceTensor(required_axes=[ConvergenceAxis.MESH, ConvergenceAxis.ANGULAR])
t.declare_tolerances({ConvergenceAxis.MESH: 1e-3, ConvergenceAxis.ANGULAR: 1e-3})
t.add_point({"h": 0.1, "delta_theta": 0.05}, (1e-9, 0, 0))
t.add_point({"h": 0.05, "delta_theta": 0.05}, (1.001e-9, 0, 0))
cert = t.evaluate()
assert cert.is_certified  # or inspect cert.overall_status / axis_results
```

Run tests:

```bash
python -m pytest tests/test_convergence_tensor.py -v
# 21 passed
```

See [momentum_closure/convergence/README.md](momentum_closure/convergence/README.md) for details.

### Key invariant

Classical conservation must close **before** any Ware / Proca (or other) hypothesis comparison is permitted.

---

*Classical conservation closes first. Hypothesis testing is last and read-only. No false anomalies from synthetic or uncertified runs.*
