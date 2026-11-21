"""
Dual Mechanistic-Cryptographic Gate (DMCG)

Mechanistic arm: dual residual style joint confirm.
  classical > 0.04 and abs(sigma) >= 0.005  (thresholds locked; do not rewrite)
Cryptographic arm: SHA-256 commitment of the evidence must verify.
Both must pass for latch and talent.

Consumes the Dual Residual decision table without modification.
Private Nursery. Not a rewrite of dual-residual.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Optional

# Locked Dual Residual thresholds. Do not change.
CLASSICAL_OWNED_THRESH = 0.04
SECOND_SOLID_FLOOR = 0.005
TALENT2_SIGMA_THRESH = 0.1
TALENT3_CLASSICAL = 0.2

@dataclass
class Evidence:
    classical: float
    sigma: float
    dual_owned: bool
    crypto_valid: bool
    latched: bool
    talent: str
    commitment: str

def dual_confirm(classical: float, sigma: float) -> bool:
    """Joint mechanistic confirm. Thresholds locked."""
    return classical > CLASSICAL_OWNED_THRESH and abs(sigma) >= SECOND_SOLID_FLOOR

def compute_talent(classical: float, sigma: float, dual: bool) -> str:
    if not dual:
        return "None"
    if abs(sigma) > TALENT2_SIGMA_THRESH:
        return "T2"
    if classical > TALENT3_CLASSICAL:
        return "T3"
    return "T1"

def make_commitment(classical: float, sigma: float, nonce: str = "") -> str:
    """Canonical SHA-256 commitment of the mechanistic decision."""
    payload = f"{classical:.8f}|{sigma:.8f}|{nonce}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def verify_commitment(classical: float, sigma: float, commitment: str, nonce: str = "") -> bool:
    return make_commitment(classical, sigma, nonce) == commitment

class DualMechanisticCryptographicGate:
    """Dual gate: mechanistic residual confirm AND cryptographic commitment."""

    def __init__(self) -> None:
        self.latched = False
        self.last: Optional[Evidence] = None

    def evaluate(self, classical: float, sigma: float, commitment: str, nonce: str = "") -> Evidence:
        mech = dual_confirm(classical, sigma)
        crypto = verify_commitment(classical, sigma, commitment, nonce)
        both = mech and crypto
        talent = compute_talent(classical, sigma, both)
        e = Evidence(
            classical=classical,
            sigma=sigma,
            dual_owned=mech,
            crypto_valid=crypto,
            latched=both,
            talent=talent,
            commitment=commitment,
        )
        if both and not self.latched:
            self.latched = True
        self.last = e
        return e

    def is_open(self) -> bool:
        return self.latched

if __name__ == "__main__":
    g = DualMechanisticCryptographicGate()
    c, s = 0.15, 0.02
    good = make_commitment(c, s, "nursery")
    e = g.evaluate(c, s, good, "nursery")
    assert e.latched and e.talent == "T1" and g.is_open(), "good path failed"
    bad = g.evaluate(c, s, "deadbeef" * 8, "nursery")
    assert not bad.latched and not bad.crypto_valid, "bad crypto should refuse"
    refuse = g.evaluate(0.01, 0.001, make_commitment(0.01, 0.001), "")
    assert not refuse.latched and not refuse.dual_owned, "below floor should refuse"
    print("ALL GREEN — Dual Mechanistic-Cryptographic Gate")
