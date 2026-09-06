# Pure Geometry (P0-B.2)

Locked classical baseline for CD-N3.

## Category locks

- `s = 0.45` is a **non-dimensional scale factor only**
- `s` is **never** an angle; `θ0` is **not invented**
- 3-fold symmetry from Rodrigues `R(120°)` about `â` only
- Ware layer **forbidden** from modifying this baseline

## Scale ladder

`L_k = L0 · s^k` with `L0 = 100 mm`:

| k | L (mm) |
|---|--------|
| 0 | 100.0 |
| 1 | 45.0 |
| 2 | 20.25 |
| 3 | 9.1125 |

## Models

- `CD-N3-P` — positive polarity
- `CD-N3-M` — geometric mirror
- `CD-N3-N` — null / control

## Generate

```python
from momentum_closure.geometry.generator import run_p0_b2
run_p0_b2("geometry_out")
```

Outputs JSON manifest + OpenSCAD sources.
