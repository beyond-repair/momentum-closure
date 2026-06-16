# Momentum Closure (Coherence Drive)

**© 2026 Brian Ware / AtomicDreamlabs — All Rights Reserved. Proprietary Technology.**

**Finding:** Net force is physically closed. Residual ΔF after Poynting subtraction is non-zero and mesh-invariant — the Ware term (via topological pinch) supplies real momentum flux from fractal LDOS gradient.

**Purpose**  
Complete closure method, equations, validation, and blind-build instructions for thrust verification in simulation/hardware.

**License**  
See LICENSE file. All rights reserved.

## 1. Momentum Closure Equations
Net surface force from effective tensor:
\[
\mathbf{F}_{\rm surface} = \oint T_{\rm eff}^{ij} \, dA
\]

Poynting flux (radiation momentum):
\[
\Phi = \oint \mathbf{S} \cdot dA, \quad \mathbf{S} = \mathbf{E} \times \mathbf{H}
\]

Residual (Ware / true thrust):
\[
\Delta F = \mathbf{F}_{\rm surface} - \frac{\Phi}{c}
\]

ΔF non-zero at n=3 due to aft-face pinch (92.1% contribution, see topological-pinch repo). Direct consequence of master \( T_{\mu\nu}^{\rm eff} = T_{\mu\nu} + W T_{\mu\nu}^{\rm info} \) (Proca variation + fractal VEV).

## 2. Blind-Build Validation Checklist
- [ ] Clone master ware-constant-phenomenology, stress-tensor-modification, topological-pinch, m2-renormalization-law, ware-constant-derivation.  
- [ ] Use physics_evaluator.py (updated).  
- [ ] Run evaluate_force_density(...) for n=2,3,4 at fixed α=0.45.  
- [ ] Confirm boundary-only computation; ΔF non-zero + mesh-invariant (L/50→L/400).  
- [ ] Symmetric geometry yields ΔF ≈0; reproduce M2 ratios (0.795/1.000/1.259).  
- [ ] Cross-check ghost-free bound (W(n)<0.125), r_0(M_b) coherence, and |A|^4 saturation.

## 3. Usage in Downstream Work
```python
from physics_evaluator import MaxwellStressTensorEvaluator

evaluator = MaxwellStressTensorEvaluator(model='M2')
results = evaluator.evaluate_force_density(
    E, H, ldos_field, n=3, mesh_dx=mesh_dx, mesh_L=mesh_L
)

print(f"Surface Force: {results['F_total']}")
print(f"Poynting Momentum: {results.get('Phi', 0) / 3e8}")
print(f"Residual ΔF (Ware thrust): {results['delta_F_Ware']}")