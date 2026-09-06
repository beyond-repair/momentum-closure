<div align="center">

# Momentum Closure

### Why a residual force, if any, must show up as a **surface integral**

[![RESEARCH](https://img.shields.io/badge/classification-RESEARCH-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/claim_level_1-conceptual-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Sweep-083](https://img.shields.io/badge/sweep-083_claim_cap-red?style=for-the-badge)](CLAIMS.md)

</div>

---

## Why this exists

People hear “Ware term” and imagine free energy.
**Momentum closure** is the discipline layer: if the model produces a net push, it must appear as a **non-canceling boundary flux** of an effective stress tensor — not as a verbal miracle.

## Why you need it

| Need | Use this repo |
|------|----------------|
| Understand the residual-force *story* | Surface form of F |
| Avoid false “proofs” | Notes only — **no** converged physical residual here |
| Find working evaluators | Go to **stress-tensor-modification** |
| Claim ledger | [CLAIMS.md](CLAIMS.md) |

## How it works (conceptual)

Surface force is the flux of T_eff. Complementary far-field/channel flux must cancel it for a closed box. See [COMPATIBLE_CLOSURE.md](COMPATIBLE_CLOSURE.md) and coherence-drive MATH_THEORY_CLOSURE.

**Status:** conceptual notes + geometry helpers. **No** mesh-converged residual demonstration. **No** released physical thrust claim.

## Related

- Evaluators: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
- Governance: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)

---

## Momentum Closure Framework (v1.2 → v1.7 spec)

### Implementation status (Sweep-083 tree audit)

| Component | State |
|-----------|--------|
| Field representation + SI dimensional checks | PLANNED (specified) |
| Single-channel momentum ledger | PLANNED (specified) |
| Formal involutive ±45° mirror + even/odd | PLANNED (specified) |
| Analytic radiation fixtures + positivity | PLANNED (specified) |
| Fail-closed certification state machine | PLANNED (specified) |
| Multidimensional convergence tensor (`tensor.py`) | **UNVERIFIED / ABSENT** |
| Surface-invariance pairwise ε metric | **UNVERIFIED / ABSENT** |
| Regression tests (`tests/test_convergence_tensor.py`) | **UNVERIFIED / ABSENT** |
| pytest “21 passed” | **UNVERIFIED** (no CI; workflows=0) |
| Geometry helpers | VERIFIED present |
| Full-wave / BEM adapter | PLANNED |

Package `__init__.py` still imports `.convergence.tensor`. That import is **broken** until the module exists.

### Key invariant

Classical conservation must close **before** any Ware / Proca (or other) hypothesis comparison is permitted.

---

*Classical conservation closes first. Hypothesis testing is last and read-only. No false anomalies from synthetic or uncertified runs.*
