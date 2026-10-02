# Claim status — momentum-closure

**Classification:** RESEARCH  
**Claim level:** 1 (conceptual / mathematical framework)  
**Sweep-158** (2026-09-20)

## Explicit tokens (docs-presence)

The following claims remain **UNSUPPORTED**:

- Mesh-converged residual / physical thrust — **UNSUPPORTED**
- Full-wave / BEM adapter — **UNSUPPORTED**
- Product CI green for physics residual — **UNSUPPORTED** (docs + unit tests only)
- Any energy-extraction or propulsion performance number — **UNSUPPORTED**
- Ware term supplying a net momentum flux — **UNSUPPORTED** (not computed here)

## Feature matrix

| Feature | State |
|---------|-------|
| Geometry helpers | VERIFIED present |
| RF feed helpers | VERIFIED present |
| Surface-integral statement (docs) | VERIFIED (docs) |
| Convergence tensor (`tensor.py`) | VERIFIED present (does not certify a physical residual) |
| Far-field fixture `F = P a /(3c)` | classical identity check only; midpoint mesh misses declared `1e-3` |
| Unit tests (`tests/`) | VERIFIED present (tensor + geometry/feed + far-field fixture) |
| Docs-presence CI | VERIFIED present |
| Product / residual CI | ABSENT (not required at L1) |
| Releases / tags | NONE |
