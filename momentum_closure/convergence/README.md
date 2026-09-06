# Multidimensional Convergence Tensor

Implemented in `momentum_closure/convergence/tensor.py`.

## Axes
- h (mesh), R (surface radius), delta_theta (angular), delta_f (frequency)
- BC (boundary), tau (solver tolerance), delta_t (timestep)

## Fail-closed rules
- Tolerances must be declared before evaluation
- Missing evidence → NOT_CERTIFIED (never implicit PASS)
- Force residual is always a 3-vector

## Tests
```
python -m pytest tests/test_convergence_tensor.py -v
# 21 passed
```

## Quick use
```python
from momentum_closure import ConvergenceTensor, ConvergenceAxis

t = ConvergenceTensor(required_axes=[ConvergenceAxis.MESH, ConvergenceAxis.ANGULAR])
t.declare_tolerances({ConvergenceAxis.MESH: 1e-3, ConvergenceAxis.ANGULAR: 1e-3})
t.add_point({"h": 0.1, "delta_theta": 0.05}, (1e-9, 0, 0))
t.add_point({"h": 0.05, "delta_theta": 0.05}, (1.001e-9, 0, 0))
cert = t.evaluate()
print(cert.overall_status, cert.is_certified)
```
