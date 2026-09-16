# Multidimensional Convergence Tensor

**State (Sweep-139):** IMPLEMENTED as a bookkeeping object.

`momentum_closure/convergence/tensor.py` now exists so the package imports.
It does **not** certify a physical residual force.

- Tolerances MUST be declared before `measure`.
- Missing axis -> NOT_CERTIFIED.
- Force residual is a 3-vector input to `residual_closure`.

Passing unit tests means the *definitions* execute. It does not mean
classical Maxwell momentum has closed on a Coherence Drive mesh.
