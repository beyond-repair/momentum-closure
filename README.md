# Momentum Closure (Coherence Drive)

**© 2026 Brian Ware / AtomicDreamlabs — All Rights Reserved. Proprietary Technology.**

**Finding:** Net force in the Coherence Drive is now physically closed. The residual ΔF after subtracting radiation momentum is non-zero and mesh-invariant — the Ware term supplies real momentum flux, not conventional radiation pressure.

**Purpose of this Repo**  
This repository contains the complete momentum closure method, the exact equations, validation steps, and blind-build instructions. A new engineer can clone this repo and immediately verify that the drive produces genuine thrust.

**License**  
See LICENSE file in this repository. All rights reserved. No copying or distribution without explicit written permission.

## 1. Momentum Closure Equations
The net force is calculated as:

\[
\mathbf{F}_{\rm surface} = \oint T^{ij} \, dA
\]

Poynting flux (radiation momentum):

\[
\Phi = \oint \mathbf{S} \cdot dA, \qquad \mathbf{S} = \mathbf{E} \times \mathbf{H}
\]

Residual (anomaly / true thrust contribution):

\[
\Delta F = \mathbf{F}_{\rm surface} - \frac{\Phi}{c}
\]

At n=3 the residual ΔF is non-zero and stable under mesh refinement — this is the signature of the topological pinch.

## 2. Blind-Build Validation Checklist
- [ ] Use the updated `physics_evaluator.py` from the master repo  
- [ ] Run `evaluate_force_density(...)` for n=3  
- [ ] Confirm `F_surface` and `Phi` are both computed on boundary faces only  
- [ ] Verify ΔF is non-zero and mesh-invariant (L/50 → L/400)  
- [ ] Check that symmetric geometry (n=1 all faces) gives ΔF ≈ 0  

## 3. Usage in Downstream Work
```python
from physics_evaluator import MaxwellStressTensorEvaluator

evaluator = MaxwellStressTensorEvaluator(model='M2')
f_total, delta_F, F_surface, Phi, scaled_ldos = evaluator.evaluate_force_density(
    E, H, ldos_field, n=3, mesh_dx=mesh_dx, mesh_L=mesh_L
)

print(f"Surface Force: {F_surface}")
print(f"Poynting Momentum: {Phi / 3e8}")
print(f"Residual ΔF: {delta_F}")
