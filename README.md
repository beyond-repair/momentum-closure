<div align="center">

# Momentum Closure

### Why a residual force, if any, must show up as a **surface integral**

[![RESEARCH](https://img.shields.io/badge/classification-RESEARCH-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/claim_level_1-conceptual-7c3aed?style=for-the-badge)](CLAIM_STATUS.md)
[![Sweep-158](https://img.shields.io/badge/sweep-158_claim_cap-red?style=for-the-badge)](CLAIM_STATUS.md)

</div>

---

## Why this exists

People hear “Ware term” and imagine free energy.
**Momentum closure** is the discipline layer: if the model produces a net push, it must appear as a **non-canceling boundary flux** of an effective stress tensor — not as a verbal miracle.

## Why you need it

| Need | Use this repo |
|------|----------------|
| Understand the residual-force *story* | Surface form of F |
| Avoid false “proofs” | Notes + numerical bookkeeping only — **no** converged physical residual here |
| Find working evaluators | Go to **stress-tensor-modification** |
| Claim ledger | [CLAIM_STATUS.md](CLAIM_STATUS.md) / [CLAIMS.md](CLAIMS.md) |

## How it works (conceptual)

Surface force is the flux of T_eff. Complementary far-field/channel flux must cancel it for a closed box. See [COMPATIBLE_CLOSURE.md](COMPATIBLE_CLOSURE.md) and coherence-drive MATH_THEORY_CLOSURE.

**Status:** conceptual notes + geometry / RF-feed helpers + ConvergenceTensor (numerical tolerances & status). **No** mesh-converged residual demonstration. **No** released physical thrust claim. Those claims are **UNSUPPORTED**.

## Related

- Evaluators: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
- Governance: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)

---

## Install, run, and test

Python 3.10+. From a clone of the default branch:

```bash
python -m pip install -e ".[dev]"
momentum-closure
python -m pytest -q
```

`momentum-closure` prints the CD-N3 scale ladder, the SMA/coax feed, and the classical far-field identity `F = P a / (3c)` for `P = 1 W`, `a = 0.9`. Optional `--out DIR` writes the JSON manifests and OpenSCAD.

What the command is allowed to say:

- Gauss–Legendre on that pattern reproduces `0.9/(3c)` newtons.
- A midpoint Riemann sum on the same pattern does **not** meet the a-priori mesh tolerance `1e-3`. That failure is printed. The tolerance is not loosened.
- Pairing the fixture force with its opposite cancels in the bookkeeping residual. That is not a device.
- `physical_thrust`, `ware_momentum_flux`, `mesh_converged_residual`, and `energy_extraction` stay **UNSUPPORTED**.

No full-wave solve, no BEM adapter, and no propulsion result are in this repository.

## Momentum Closure Framework (v1.7)

### Implementation status (Sweep-158 tree + local pytest)

| Component | State |
|-----------|--------|
| Field representation + SI dimensional checks | PLANNED (specified) |
| Single-channel momentum ledger | PLANNED (specified) |
| Formal involutive ±45° mirror + even/odd | **checked** (Householder, algebra only) |
| Analytic radiation fixtures + positivity | **checked** (see far-field row; `|a|>1` is INVALID_INPUT) |
| Fail-closed certification state machine | PLANNED (specified) |
| Multidimensional convergence tensor (`tensor.py`) | **VERIFIED present** (bookkeeping only) |
| Classical far-field fixture `F = P a / (3c)` | **checked** (Gauss matches; midpoint mesh **FAILED** at declared `1e-3`) |
| Surface-invariance pairwise ε metric | DECLARED, not measured (no second surface) |
| Regression tests | **present** (`pytest`; tensor tests need only pytest, fixture/geometry tests need numpy) |
| Geometry helpers | VERIFIED present (`momentum-closure` or `run_p0_b2`) |
| RF feed helpers | VERIFIED present (`run_p0_c1`) |
| Docs-presence CI | VERIFIED present |
| Full-wave / BEM adapter | PLANNED |

Package `__init__.py` imports `.convergence.tensor` — **resolved**. ConvergenceTensor never certifies a physical residual; it only records declared tolerances and numerical status. The CLI audit's mesh axis is a midpoint quadrature comparison and is expected to print `FAILED` against tolerance `1e-3`.

### Key invariant

Classical conservation must close **before** any Ware / Proca (or other) hypothesis comparison is permitted.

---

*Classical conservation closes first. Hypothesis testing is last and read-only. No false anomalies from synthetic or uncertified runs.*
