# Momentum Closure ⊕ Topological Pinch

**Status:** Conceptual framework (claim level 1)  
**Does not establish continuum thrust.**  
**Stage-2 context:** Tested scalar and Proca P-E2 maps archived as null under STAGE2_ACCEPTANCE_CRITERION.

---

## 1. Two layers, one question

| Layer | Repo | Question |
|-------|------|----------|
| **Momentum closure** | this repo | If a residual force exists, where must it appear in the math? |
| **Topological pinch** | [topological-pinch](https://github.com/beyond-repair/topological-pinch) | Might asymmetry *localize* flux so cancellation fails? |

Momentum closure is **necessary bookkeeping**.  
Topological pinch is a **localization hypothesis**.  
Neither is a measured force.

---

## 2. Momentum closure (discipline)

Conservation of field momentum implies that any net push attributed to the field must show up as a **non-canceling surface flux**:

$$
\mathbf{F}_{\rm surface}
=
\oint_{\partial V} T_{\rm eff}^{ij}\, n_j\, dA
$$

with (Stage-1 freeze)

$$
T_{\rm eff}^{ij}
=
T_{\rm EM}^{ij}
+
W(n)\,\chi_{\rm vac}\,(\nabla\Psi_{\rm info})^{ij}.
$$

**Rules:**

1. Verbal “Ware thrust” without a surface integral is not momentum-closed.  
2. A nonzero integral on a discrete mesh is not continuum force until spherical control + joint refinement pass (acceptance criterion).  
3. Radiation / open boundaries require full momentum accounting (storage, outflow, radiation).

**Status of this repository:** conceptual notes only. No mesh-converged residual is claimed here. Executable stress evaluation lives in [stress-tensor-modification](https://github.com/beyond-repair/stress-tensor-modification).

---

## 3. Topological pinch (hypothesis)

**Statement:** On the 0.45 asymmetric Sierpinski-type hull, stress divergence or traction density concentrates on the **aft** face, so the closed-surface integral need not vanish by pairwise cancellation.

**Not established:**

- The historical “~92%” figure (unverified; see topological-pinch CLAIM_STATUS).  
- Continuum non-zero net \(\mathbf{F}\) under tested constitutive maps (Stage-2 null).

**What a valid pinch study would report:**

1. Partition \(\partial V\) into aft vs fore (or vertex-neighborhood) sets.  
2. Compute partial fluxes \(\mathbf{F}_A=\int_A T\cdot n\,dA\), \(\mathbf{F}_F=\int_F T\cdot n\,dA\).  
3. Localization metric, e.g.  
   \(L = |\mathbf{F}_A| / (|\mathbf{F}_A|+|\mathbf{F}_F|+\varepsilon)\).  
4. Mesh refinement of \(L\) **and** of net \(\mathbf{F}=\mathbf{F}_A+\mathbf{F}_F\).  
5. Spherical control: same partition logic must not invent a preferred axis on a sphere.

Localization without net \(|\mathbf{F}|\) above the control floor is **not** thrust.

---

## 4. How the two layers connect

```text
Momentum closure:   F must be ∮ T·n dA
        ↓
Topological pinch:  maybe |F_aft| ≫ |F_fore| on asymmetric geometry
        ↓
Stage-2 numerics:   under tested maps, net |F| stayed ≤ spherical floor
        ↓
Conclusion so far:  bookkeeping rule stands; pinch not established as continuum net force
```

Pinch cannot bypass momentum closure.  
Momentum closure cannot invent pinch without a solved field and floor test.

---

## 5. Relation to archived Stage-2 work

Under [STAGE2_ACCEPTANCE_CRITERION](https://github.com/beyond-repair/coherence-drive/blob/stage2-numerical-closure/docs/STAGE2_ACCEPTANCE_CRITERION.md):

- Scalar and Proca P-E2 exterior studies: net residual **≤ control floor** → archived **null**.  
- Reopening those maps solely via mesh/element/post-processing changes is **forbidden** without a new constitutive map or BVP ([ARCHIVED_NULL_REOPEN_POLICY](https://github.com/beyond-repair/coherence-drive/blob/stage2-numerical-closure/docs/ARCHIVED_NULL_REOPEN_POLICY.md)).

A future pinch study is only Stage-2-relevant if it is attached to a **frozen, independently motivated** field problem and passes the five-step criterion—including residual **above** floor.

---

## 6. Claim flags

```
experimental_validation     = false
thrust_validated            = false
energy_extraction_validated = false
target_fitting_performed    = false
mesh_converged_residual     = false   # in this repo
pinch_fraction_verified     = false
```

---

*This document is governance + conceptual structure. It is not a propulsion result.*
