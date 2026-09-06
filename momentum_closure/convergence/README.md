# Multidimensional Convergence Tensor

**State (Sweep-083):** PLANNED / UNVERIFIED.

`momentum_closure/convergence/tensor.py` is **not** present on `main` (tree SHA `ba13d1b9…`).  
`tests/test_convergence_tensor.py` is **not** present.  
pytest “21 passed” is **not** an Actions-verified result.

Package `__init__.py` still imports `.tensor`. That import **cannot** succeed until the module is added.

## Axes (specified, not implemented here)

- h (mesh), R (surface radius), delta_theta (angular), delta_f (frequency)
- BC (boundary), tau (solver tolerance), delta_t (timestep)

## Fail-closed rules (specified)

- Tolerances declared before evaluation
- Missing evidence → NOT_CERTIFIED
- Force residual is a 3-vector

Do not paste usage examples that assume `ConvergenceTensor` exists until the blob lands.
