# P0-C.1 RF Feed + Faraday Enclosure

Single-port SMA/coax excitation into an explicit PEC Faraday boundary.

## Category locks

- Classical SMA/coax only (`Z0 = 50 Ω`)
- Single port (`port_index = 1`)
- Enclosure BC = `PEC`
- Ware does **not** modify feed or enclosure
- Scale factor `s` is **not** used as an angle

## Defaults

| Quantity | Value |
|----------|-------|
| Port position | `(0, 0, -60)` mm |
| Pin axis | `+z` |
| Enclosure | cylinder R=80 mm, H=120 mm |
| Wall | 2 mm |

## Generate

```python
from momentum_closure.rf_feed import run_p0_c1
run_p0_c1("geometry_out", geometry_manifest_sha256="...")
```

Next: P0-C.2 / P0-C.3 eigenmode sweep + classical Maxwell stress export.
