# Dual Mechanistic-Cryptographic Gate

Private Nursery. Unpublished. Not a filed title.

**Dual gate**: mechanistic residual confirmation (Dual Residual style, locked thresholds) **AND** cryptographic commitment (SHA-256) must both pass before the irreversible latch and talent are granted.

## Mechanistic arm

Consumes the Dual Residual decision table without rewriting it:

```
dual_owned = classical > 0.04 && |sigma| >= 0.005
if (!dual_owned) -> None
else if (|sigma| > 0.1) -> T2
else if (classical > 0.2) -> T3
else -> T1
```

## Cryptographic arm

Caller supplies a SHA-256 commitment of the canonical evidence (`classical|sigma|nonce`). The gate recomputes and verifies. Mismatch refuses even if the mechanistic side confirms.

## Use

```python
from dmcg import DualMechanisticCryptographicGate, make_commitment

g = DualMechanisticCryptographicGate()
commitment = make_commitment(0.15, 0.02, nonce="nursery")
e = g.evaluate(0.15, 0.02, commitment, nonce="nursery")
# e.latched is True only when both arms pass
```

Run `python dmcg.py` for the self-test (ALL GREEN).

## Status

Research-grade. Private. Not production. Thresholds locked. Not a rewrite of dual-residual or χ-Dual Talent Gate.

Copyright (c) 2026 Heywood Geblomi / Blanton's Hilltop Nursery. All rights reserved.
