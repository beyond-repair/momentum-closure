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
| Understand the residual-force *story* | Surface form of \(\mathbf{F}\) |
| Avoid false “proofs” | Notes only — **no** converged physical residual here |
| Find working code | Go to **stress-tensor-modification** |
| Physics-integrity / certification framework | See [Framework v1.2–v1.7](#momentum-closure-framework-v12--v17) below |

## How it works (conceptual)

$$
\mathbf{F}_{\rm surface} = \oint T_{\rm eff}^{ij}\, dA_j
$$

with

$$
T_{\rm eff} = T_{\rm EM} + W(n)\,\chi_{\rm vac}\,(\nabla\Psi_{\rm info})
$$

(as frozen in [MATH_THEORY_CLOSURE](https://github.com/beyond-repair/coherence-drive/blob/main/docs/MATH_THEORY_CLOSURE.md)).

**Status:** conceptual notes + evolving certification architecture. **No** mesh-converged residual demonstration in this repository. **No** released physical thrust claim.

## Related

- Evaluators: [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification)  
- Index: [coherence-drive](https://github.com/beyond-repair/coherence-drive)

---

## Momentum Closure Framework (v1.2 → v1.7)

This section consolidates the self-contained review of the **numerically rigorous** electromagnetic momentum-closure validation harness. It is structured for replication, peer review, and progressive implementation.

### Project objective

Develop a framework that validates electromagnetic momentum closure in radiation fields, enforces conservation laws and dimensional consistency, and structurally prevents false anomaly claims from synthetic or uncertified data.

**Key invariant:** Classical conservation must close **before** any Ware / Proca (or other) hypothesis comparison is permitted.

### Mathematical foundation (locked)

**Radiation-force relation (dimensional correction):**

$$
\boxed{F_{\rm rad} = \frac{1}{c} \oint_S \mathbf{S}\, dA}
$$

- \(S/c^2\) is momentum density; \(S/c\) is radiation pressure / force-per-area for outgoing fields.

**Analytic fixture (exact net radiated momentum rate):**

For

$$
\frac{dP}{d\Omega} = \frac{P}{4\pi}(1 + a\cos\theta),
$$

the exact result is

$$
\boxed{\mathbf{F}_{\rm rad} = \frac{aP}{3c}\hat{z}}, \qquad \mathbf{F}_{\rm stress} = -\mathbf{F}_{\rm rad}.
$$

General vector form:

$$
\frac{dP}{d\Omega} = \frac{P}{4\pi}(1 + \mathbf{a}\cdot\hat{\mathbf{r}}) \quad\Rightarrow\quad \mathbf{F} = \frac{P}{3c}\mathbf{a}.
$$

Positivity requirement: \(1 + \mathbf{a}\cdot\hat{r} \ge 0\) (sufficient: \(|\mathbf{a}|\le 1\)). Invalid fixtures must return `INVALID_INPUT` before evaluation.

**Radiation-efficiency invariant:**

$$
\eta_p = \frac{c|\mathbf{F}_{\rm rad}|}{P}.
$$

- \(\eta_p < 1\): ordinary directional radiation  
- \(\eta_p \approx 1\): highly collimated  
- \(\eta_p > 1\): `INVALID / INVESTIGATE` (missing power, orientation error, near-field contamination, material momentum, etc. — **not** automatic evidence of anomalous propulsion).

### Architectural design (fail-closed)

```
RAW FIELDS / FieldSample
        │
┌───────▼────────┐
│ Field Integrity │  (units, finite values, medium model)
│ + SI dimensions │  → G0 / G9 / G17
└───────┬────────┘
        │
┌───────▼────────┐
│ Physical Model  │  (SOURCE / MATTER → MATERIAL → VACUUM → SURFACE → RADIATION)
│ / Material      │
└───────┬────────┘
        │
┌───────▼────────────────────┐
│ Independent EM Accounting  │
│ Maxwell stress             │
│ Poynting flux              │
│ radiation momentum         │
│ field storage (transient)  │
└───────┬────────────────────┘
        │
   CONSERVATION + Closure residual (vector-first)
        │
┌───────▼────────┐
│ Surface / Mesh │  convergence tensor (h, R, Δθ, Δf, BC, τ, Δt)
│ / Angular      │  surface-invariance metric
└───────┬────────┘
        │
┌───────▼────────┐
│ Null hierarchy │  N0–N4 + formal involutive ±45° mirror operator
│ + Controls     │
└───────┬────────┘
        │
┌───────▼────────┐
│ Provenance +   │  SHA-256, independent implementation (G18)
│ Independent    │  cancellation conditioning (κ_F)
└───────┬────────┘
        │
     G0–G22 certification state machine (fail-closed)
        │
   CERTIFIED → VECTOR R₀ → ODD/EVEN → PARALLEL/TRANSVERSE
        │
   STATISTICS + SYSTEMATICS
        │
   HYPOTHESIS TEST (read-only; never enters classical budget)
```

**Momentum ledger (single-channel accounting):**  
Every physical contribution has exactly one `channel_id` (e.g. `EM_BOUNDARY_FLUX`, `EM_FIELD_STORAGE`, `MECHANICAL_APPLIED`, `MECHANICAL_REACTION`). Diagnostics cannot create a second ledger entry for the same transfer.

**Hypothesis isolation:**  
Ware (or any other) hypothesis is compared **descriptively** to the observed residual only after full certification. It is **never** included in \(F_{\rm classical}\).

**CertifiedResidual object** (hypothesis layer receives only this):

```
CertifiedResidual
├── vector_N
├── odd_vector_N / even_vector_N
├── parallel_N / transverse_vector_N
├── statistical_uncertainty_N
├── systematic_bound_N
├── convergence_certificate
├── surface_certificate
├── null_certificate
├── provenance_certificate
└── independent_implementation_certificate
```

### Core equations (v1.7 engine)

Maxwell stress tensor:

$$
\mathbf{T} = \varepsilon_0\Bigl(\mathbf{E}\mathbf{E}^T - \tfrac12 E^2 I\Bigr) + \frac1{\mu_0}\Bigl(\mathbf{B}\mathbf{B}^T - \tfrac12 B^2 I\Bigr).
$$

Surface force / power / radiation momentum (discrete):

$$
\mathbf{F}_T = \sum_i (\mathbf{T}_i\cdot\hat n_i) w_i, \quad
P = \sum_i (\mathbf{S}_i\cdot\hat n_i) w_i, \quad
\mathbf{F}_{\rm rad} = \frac1c \sum_i (\mathbf{S}_i\cdot\hat n_i)\hat n_i w_i.
$$

Regime selection (not a universal identity):

- `STEADY_FAR_FIELD`  
- `TRANSIENT` (retain \(d\mathbf{P}_{\rm EM}/dt\))  
- `NEAR_FIELD`  
- `MATERIAL_BOUNDARY`

For steady outgoing radiation:

$$
\mathbf{F}_{\rm matter} + \mathbf{F}_{\rm EM,out} \approx 0.
$$

For transient:

$$
\mathbf{F}_{\rm matter} + \mathbf{F}_{\rm EM,boundary} + \frac{d\mathbf{P}_{\rm EM}}{dt} \approx 0.
$$

**Hard architectural invariant:**  
Maxwell stress ≠ radiation momentum ≠ three independent forces. They are different mathematical representations / diagnostics of the same electromagnetic momentum accounting.

### Certification & classifier (fail-closed)

Each gate produces a signed `GateResult` (status, measured_value, threshold, units, input_hash, implementation_id, evidence_hash). Missing evidence → `NOT_CERTIFIED`, not PASS.

Terminal classification hierarchy (single terminal state only):

```
INPUT_INVALID
→ NUMERICALLY_UNRESOLVED
→ CLASSICAL_CLOSURE_FAIL
→ PROVENANCE_FAIL
→ CONTROL_FAIL
→ SYSTEMATICALLY_LIMITED
→ NO_RESIDUAL
→ RESIDUAL_DETECTED
→ HYPOTHESIS_COMPATIBLE
```

A run reaches `RESIDUAL_DETECTED` only when **all applicable gates G0–G22** are certified. Only then:

$$
\mathbf{R}_0 = \mathbf{F}_{\rm measured} - \mathbf{F}_{\rm classical}
$$

followed by odd/even and parallel/transverse decomposition. Hypothesis comparison is the final, read-only step.

**Null hierarchy (N0–N4):** mathematical zero, symmetric excitation, mirrored pair, instrumentation/control, blind corruption.

**Formal mirror operator:** involutive \(M\) with \(M^2 = I\); even/odd projectors verified algebraically.

**Cancellation conditioning:** if \(\kappa_F\) (sum of absolute terms over residual) exceeds threshold, require higher precision / independent implementation / perturbation tests before accepting the residual.

### Implementation status (as of local v1.6 / v1.7 design)

| Component | Status |
|-----------|--------|
| Field representation + SI dimensional checks | Implemented (v1.6) |
| Single-channel momentum ledger | Implemented |
| Formal involutive ±45° mirror + even/odd | Implemented |
| Analytic radiation fixtures + positivity | Implemented |
| Fail-closed certification state machine | Implemented |
| Regression tests | 5 passed (v1.6 local) |
| Full-wave / BEM adapter + multidimensional convergence engine | Next (v1.7 → v1.8) |
| Real experimental telemetry + G7–G8 eligibility | Requires `fixture_status == REAL_EXPERIMENTAL_RUN` + SHA-256 provenance |

**Local artifact note (v1.6):**  
SHA-256 `99edd892eabdf162538ce96e33c0dbb8aa449548d87050ba2572e4dcba81a007` (physics-integrity layer). No matching code has been pushed to this repository; the present commit updates documentation only.

### Next steps

1. **v1.8** — Integrate analytic fixture into the closure engine; multidimensional convergence + surface-invariance sweep; automated certificate generation.  
2. Adapter for existing full-wave / BEM field data (`FieldSample` contract: position, E, H, B, normal, weight, timestamp, frequency, surface_id, provenance_hash — no implicit units).  
3. Promote permanent CI tests for isotropic / dipole / arbitrary-vector analytic fixtures.  
4. Only after classical closure is certified may any residual enter hypothesis comparison.

### Review checklist for replicators

1. Dimensional consistency: is \(F_{\rm rad} = (1/c)\oint\mathbf{S}\,dA\) enforced everywhere?  
2. Hypothesis isolation: does Ware (or any other) term ever enter \(F_{\rm classical}\)?  
3. Synthetic data: can it ever produce an anomaly claim? (Must be blocked by provenance / fixture_status.)  
4. Vector residual: is the full vector retained (no premature collapse to a single parallel component)?  
5. Surface invariance & convergence tensor: are they reported, not just a final selected surface?  
6. Cancellation: is high \(\kappa_F\) escalated rather than accepted?  
7. Gate evidence: is every PASS backed by a hashable evidence object?

---

*Classical conservation closes first. Hypothesis testing is last and read-only. No false anomalies from synthetic or uncertified runs.*
