# Momentum Closure Framework Review (v1.2 → v1.7)

**Repository:** [beyond-repair/momentum-closure](https://github.com/beyond-repair/momentum-closure)  
**Purpose of this document:** Self-contained summary for replication, review, and validation by another AI or research team. Consolidates findings, architectural decisions, mathematical corrections, test posture, and next steps.

---

## 1. Project overview

**Objective:** Numerically rigorous framework for validating electromagnetic momentum closure in radiation fields, ensuring conservation laws and dimensional consistency while structurally preventing false anomaly claims.

**Key innovation:** Closed-surface validation harness that separates **measurement**, **classical budgeting**, and **hypothesis comparison**.

**Hard invariant:** Classical conservation must close before any Ware/Proca (or other) interpretation is permitted.

---

## 2. Mathematical foundation

### 2.1 Dimensional correction

$$
\boxed{F_{\rm rad} = \frac{1}{c} \oint_S \mathbf{S}\, dA}
$$

\(S/c^2\) is momentum density; \(S/c\) is radiation pressure / force-per-area for outgoing fields.

### 2.2 Analytic fixtures (permanent regression targets)

**Isotropic**

$$
\frac{dP}{d\Omega} = \frac{P}{4\pi} \quad\Rightarrow\quad \mathbf{F}=0.
$$

**Dipole-like**

$$
\frac{dP}{d\Omega} = \frac{P}{4\pi}(1+a\cos\theta) \quad\Rightarrow\quad \boxed{F_z = \frac{aP}{3c}},\quad F_x=F_y=0.
$$

**Arbitrary vector**

$$
\frac{dP}{d\Omega} = \frac{P}{4\pi}(1+\mathbf{a}\cdot\hat{\mathbf{r}}) \quad\Rightarrow\quad \boxed{\mathbf{F}=\frac{P}{3c}\mathbf{a}}.
$$

**Positivity:** \(1+\mathbf{a}\cdot\hat{r}\ge0\) (sufficient \(|\mathbf{a}|\le1\)). Invalid → `INVALID_INPUT` before solver evaluation.

**Target numeric example (v1.7):** \(P=1\,\mathrm{W}\), \(a=0.9\)

$$
F_{\rm rad} = \frac{0.9}{3c} \approx 1.00069\times10^{-9}\,\mathrm{N}
$$

→ engine must converge to approximately \((0,0,1.00069\times10^{-9})\,\mathrm{N}\) with opposite mechanical recoil.

### 2.3 Radiation-efficiency invariant

$$
\eta_p = \frac{c|\mathbf{F}_{\rm rad}|}{P}.
$$

| Regime | Interpretation |
|--------|----------------|
| \(\eta_p < 1\) | Ordinary directional radiation |
| \(\eta_p \approx 1\) | Highly collimated |
| \(\eta_p > 1\) | `INVALID / INVESTIGATE` (not automatic anomaly evidence) |

Investigate first: missing power, wrong surface orientation, incomplete angular integration, near-field contamination, normalization error, material momentum, numerical instability.

---

## 3. Architectural design

### 3.1 Physical region separation

```
SOURCE / MATTER
      │
MATERIAL DOMAIN
      │
VACUUM / EXTERIOR
      │
ENCLOSING SURFACE   ← prefer region where intended momentum formulation is valid
      │
RADIATION / ABSORBING REGION
```

### 3.2 Field representation lock

Authoritative input: \((\mathbf{E},\mathbf{H})\). Derive \(\mathbf{B}=\mu_0\mathbf{H}\) **only** where the medium model explicitly permits it. For general material regions store \(\mathbf{D},\mathbf{B},\mathbf{E},\mathbf{H}\) together with `medium_model`, `epsilon`, `mu`, `dispersion`, `loss_model`, `units`. Prevents accidental vacuum Maxwell-stress application inside material domains.

### 3.3 Momentum ledger (single-channel)

Every physical contribution has exactly one accounting location / `channel_id`:

- `EM_BOUNDARY_FLUX`
- `EM_FIELD_STORAGE`
- `MECHANICAL_APPLIED`
- `MECHANICAL_REACTION`
- …

A diagnostic cannot create a second ledger entry for the same physical transfer. Makes G12 machine-checkable.

### 3.4 Dimensional analysis as executable code (G9)

Every reported quantity carries a dimensional signature. Engine rejects mismatches such as `force_N = power_W` before numerical comparison.

### 3.5 Formal ±45° / mirror operator

Define involutive mirror \(M:\mathbb{R}^3\to\mathbb{R}^3\) with \(M^2=I\).

$$
X_{\rm even}=\frac{X+MX}{2},\qquad X_{\rm odd}=\frac{X-MX}{2}.
$$

Must verify algebraically:

$$
M(X_{\rm even})=X_{\rm even},\qquad M(X_{\rm odd})=-X_{\rm odd}.
$$

### 3.6 Residual hierarchy (vector-first)

$$
\mathbf{R}_0 \;\rightarrow\; \mathbf{R}_{\rm odd}+\mathbf{R}_{\rm even}
$$

then

$$
\mathbf{R}_{\rm odd} = R_\parallel\hat{n} + \mathbf{R}_\perp.
$$

A scalar parallel residual cannot be reported without retaining the transverse vector (alignment errors, mesh artifacts, improper mirror, etc.).

### 3.7 Null hierarchy

| Level | Test |
|-------|------|
| N0 | Mathematical zero: \(E=H=0\Rightarrow F=0\) |
| N1 | Symmetric excitation → intended force zero |
| N2 | Mirrored pair → odd force ≈ 0 |
| N3 | Instrumentation/control: known force injected and recovered |
| N4 | Blind corruption: pipeline must reject the run |

### 3.8 Certification dependency graph (fail-closed)

Raw fields → Input integrity (G0/G9/G17) → Numerical convergence (G3/G10) → Independent EM accounting → Closure (G4–G6) → Surface/symmetry/null (G11–G16) → Provenance/independent implementation (G8,G17,G18) → Physical + adversarial (G19–G22) → **CERTIFIED** → Residual R₀ → Odd/Even → Systematics → Hypothesis comparison only.

Each gate emits a signed `GateResult` (status, measured_value, threshold, units, input_hash, implementation_id, evidence_hash). Missing evidence → `NOT_CERTIFIED`.

### 3.9 Surface invariance & multidimensional convergence

Pairwise normalized disagreement across surfaces \(S_i\):

$$
\epsilon_{ij}=\frac{\|\mathbf{F}_i-\mathbf{F}_j\|}{\max(F_{\rm floor},\|\mathbf{F}_i\|,\|\mathbf{F}_j\|)}.
$$

Require \(\max_{i,j}\epsilon_{ij}\le\epsilon_{\rm surface}\) (tolerance declared a priori). Report the entire radius/mesh/angular sweep, not only the final selected surface.

Convergence evidence required across: mesh \(h\), surface radius \(R\), angular quadrature \(\Delta\theta\), frequency resolution, boundary treatment, solver tolerance, timestep (as applicable) — represented as a convergence tensor.

### 3.10 Independent implementation (G18) & cancellation escalation

Compare two mathematically independent formulations (e.g. tensor/vectorized vs component-wise). Relative difference must stay below threshold.

Cancellation factor:

$$
\kappa_F = \frac{|F_1|+|F_2|}{|F_{\rm residual}|+F_{\rm floor}}.
$$

If \(\kappa_F\) exceeds declared threshold, certification requires higher precision, independent implementation, tighter tolerances, repeated evaluation, and/or perturbation tests. The system cannot simply report the tiny difference.

### 3.11 Hypothesis isolation

Hypothesis layer receives **only** a `CertifiedResidual` object. No access to raw measurement that would permit changing the classical budget. Ware (or any other) term is **never** included in \(F_{\rm classical}\).

---

## 4. v1.7 data contracts & engine

### FieldSample (no implicit units)

```
FieldSample
├── position[m]
├── E[V/m]
├── H[A/m]
├── B[T]
├── surface_normal
├── surface_weight[m²]
├── timestamp[s]
├── frequency[Hz]
├── surface_id
└── provenance_hash
```

### ClosureResult (vector residual always)

```
ClosureResult
├── force_stress_N[3]
├── power_W
├── radiation_momentum_N[3]
├── field_momentum_Ns[3]
├── storage_derivative_N[3]
├── closure_residual_N[3]
├── eta_p / eta_p_status / eta_p_bound
├── surface_invariance
├── convergence
├── conditioning
├── mirror_decomposition
└── certification
```

### Regime selection

Engine selects applicable conservation equation:

- `STEADY_FAR_FIELD`
- `TRANSIENT` (retain \(d\mathbf{P}_{\rm EM}/dt\))
- `NEAR_FIELD`
- `MATERIAL_BOUNDARY`

Does **not** assert \(\mathbf{F}_{\rm rad}=-\mathbf{F}_T\) as a universal identity for arbitrary near-field solutions.

### Power consistency invariant

$$
\epsilon_P = \frac{|P_{\rm surface}-P_{\rm expected}|}{\max(P_{\rm floor},|P_{\rm expected}|)}.
$$

Failure blocks force certification.

---

## 5. Classifier terminal states

Only one terminal classification is emitted:

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

Cannot jump from “large measured force” directly to hypothesis without passing through conservation closure.

---

## 6. Implementation posture

| Layer | Status |
|-------|--------|
| v1.2 computed-metrics / audit schema | Documented; synthetic fixtures intentionally ineligible for G7–G8 |
| v1.5 certification core (fail-closed, vector residual, surface invariance, cancellation) | Specified |
| v1.6 physics-integrity primitives (field validation, SI dimensions, ledger, mirror, fixtures, positivity, state machine) | Locally implemented & verified (5 tests passed); constructor defect corrected |
| v1.7 full-wave closure engine design | Specified; target analytic dipole fixture defined |
| v1.8+ | Convergence engine + integrated analytic fixture + BEM/full-wave adapter |

**Local v1.6 artifact SHA-256 (not present in this repo):**  
`99edd892eabdf162538ce96e33c0dbb8aa449548d87050ba2572e4dcba81a007`

This repository currently holds conceptual notes + the present consolidated review. Working code remains in related evaluators / local artifacts until deliberately pushed.

---

## 7. Review questions for replicating AI / team

1. **Mathematical validation** — Does the dimensional correction (\(1/c\) vs \(1/c^2\)) hold for all test cases? Are analytic fixture results reproducible to machine precision under refinement?
2. **Architectural rigor** — Is ODD/EVEN separation correctly enforced? Are hypothesis terms excluded from the classical budget?
3. **Numerical robustness** — Do G0–G6 (and later gates) pass for arbitrary field inputs, not only the analytic fixture? Is the control-volume residual vectorially correct?
4. **Reproducibility** — Can SHA-256 hashes be regenerated from provided telemetry? Does the machine-readable audit match the expected schema?
5. **Next steps** — What additional validation is required before integrating `fullwave_bem.py` (or equivalent)? Should the ±45° mirror decomposition be tested in isolation as a permanent CI unit?

---

## 8. Final notes

- **No false anomalies:** Synthetic data and uncertified runs cannot produce anomaly claims.
- **Open for extension:** Audit schema and ledger channels can be extended for additional physical channels.
- **Key invariant remains:** Classical conservation closes first; hypothesis testing is last and read-only.

*Ready for peer stress-test, independent re-implementation of the integrity layer, and progressive connection to full-wave field data.*
