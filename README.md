<div align="center">

# Momentum Closure

### Why a residual force, if any, must show up as a **surface integral**

[![RESEARCH](https://img.shields.io/badge/classification-RESEARCH-f59e0b?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/claim_level_1-conceptual-7c3aed?style=for-the-badge)](https://github.com/beyond-repair/ADL-Governance)

</div>

---

## Why this exists

People hear “Ware term” and imagine free energy.  
**Momentum closure** is the discipline layer: if the model produces a net push, it must appear as a **non-canceling boundary flux** of an effective stress tensor — not as a verbal miracle.

## Why you need it

| Need | Use this repo |
|------|----------------|
| Understand the residual-force *story* | Surface form of \(\mathbf{F}\) |
| Avoid false “proofs” | Notes only — **no** converged physical residual here |
| Find working code | Go to **stress-tensor-modification** |

## How it works (conceptual)

$$
\mathbf{F}_{\rm surface} = \oint T_{\rm eff}^{ij}\, dA_j
$$

with

$$
T_{\rm eff} = T_{\rm EM} + W(n)\,\chi_{\rm vac}\,(\nabla\Psi_{\rm info})
$$

(as frozen in [MATH_THEORY_CLOSURE](https://github.com/beyond-repair/coherence-drive/blob/main/docs/MATH_THEORY_CLOSURE.md)).

**Status:** conceptual notes. **No** mesh-converged residual demonstration in this repository. **No** released physical thrust claim.

## Related

- Evaluators: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)  
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)
