"""ARM-Sim core.

Associative Return Memory (ARM) simulation.

This is a quantum-inspired simulator, not a physical quantum simulator.
It models the central ARM claim:

    memory stores return relations;
    states are recomputed under an Observer-Commander criterion;
    observations update future return likelihood.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple
import numpy as np

Criterion = Literal["similarity", "stability", "novelty", "hybrid"]
Mode = Literal["argmax", "sample"]


def bits(x: np.ndarray) -> str:
    """Return a compact bit-string representation of a binary vector."""
    return "".join(str(int(v)) for v in np.asarray(x).astype(int).ravel())


def hamming_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Similarity in [0, 1] for equal-length binary vectors."""
    a = np.asarray(a).astype(int)
    b = np.asarray(b).astype(int)
    if a.shape != b.shape:
        raise ValueError("Vectors must have the same shape")
    return float(np.mean(a == b))


def softmax(x: np.ndarray, beta: float = 1.0) -> np.ndarray:
    """Numerically stable softmax with inverse-temperature beta."""
    x = np.asarray(x, dtype=float)
    z = beta * (x - np.max(x))
    exp = np.exp(z)
    denom = exp.sum()
    if denom == 0 or not np.isfinite(denom):
        return np.ones_like(exp) / len(exp)
    return exp / denom


def corrupt_pattern(pattern: np.ndarray, noise: float, rng: np.random.Generator) -> np.ndarray:
    """Flip each bit with probability `noise`."""
    if not 0 <= noise <= 1:
        raise ValueError("noise must be in [0, 1]")
    pattern = np.asarray(pattern).astype(int)
    mask = rng.random(pattern.shape) < noise
    out = pattern.copy()
    out[mask] = 1 - out[mask]
    return out


def random_patterns(n_patterns: int, n_bits: int, rng: np.random.Generator) -> np.ndarray:
    """Generate unique binary patterns when possible."""
    if n_patterns > 2 ** n_bits:
        raise ValueError("n_patterns cannot exceed 2 ** n_bits")
    seen = set()
    patterns = []
    while len(patterns) < n_patterns:
        p = rng.integers(0, 2, size=n_bits, dtype=int)
        s = bits(p)
        if s not in seen:
            seen.add(s)
            patterns.append(p)
    return np.vstack(patterns)


@dataclass
class Relation:
    """A stored return relation.

    key: cue pattern that activates the relation.
    target: state returned/recomputed when the relation is selected.
    weight: learned strength or significance.
    stability: historical reliability score.
    novelty: exploration score.
    """

    name: str
    key: np.ndarray
    target: np.ndarray
    weight: float = 1.0
    stability: float = 1.0
    novelty: float = 1.0

    def score(self, cue: np.ndarray, criterion: Criterion = "hybrid") -> float:
        sim = hamming_similarity(cue, self.key)
        if criterion == "similarity":
            return self.weight * sim
        if criterion == "stability":
            return self.weight * sim * self.stability
        if criterion == "novelty":
            return self.weight * sim * self.novelty
        if criterion == "hybrid":
            return self.weight * sim * (0.70 * self.stability + 0.30 * self.novelty)
        raise ValueError(f"Unknown criterion: {criterion}")


@dataclass
class Observation:
    """Classical observation trace."""

    step: int
    cue: str
    criterion: Criterion
    returned_relation: str
    returned_state: str
    confidence: float
    success: Optional[bool] = None


@dataclass
class AssociativeReturnMemory:
    """Relation-centric memory.

    The memory does not store a single final state. It stores relations that can
    return/recompute states under an Observer-Commander criterion.
    """

    relations: List[Relation] = field(default_factory=list)
    beta: float = 6.0
    log: List[Observation] = field(default_factory=list)

    def add_relation(self, relation: Relation) -> None:
        self.relations.append(relation)

    def scores(self, cue: np.ndarray, criterion: Criterion = "hybrid") -> np.ndarray:
        if not self.relations:
            raise ValueError("No relations stored")
        return np.array([r.score(cue, criterion) for r in self.relations], dtype=float)

    def probabilities(self, cue: np.ndarray, criterion: Criterion = "hybrid") -> np.ndarray:
        """Return a probability-like distribution over relations."""
        return softmax(self.scores(cue, criterion), beta=self.beta)

    def amplitudes(self, cue: np.ndarray, criterion: Criterion = "hybrid") -> np.ndarray:
        """Quantum-inspired amplitude magnitudes for reporting/analysis."""
        return np.sqrt(self.probabilities(cue, criterion))

    def return_state(
        self,
        cue: np.ndarray,
        criterion: Criterion = "hybrid",
        mode: Mode = "argmax",
        rng: Optional[np.random.Generator] = None,
        expected: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, Relation, float]:
        """Return/recompute a state by activating a relation."""
        probs = self.probabilities(cue, criterion)
        if mode == "sample":
            rng = rng or np.random.default_rng()
            idx = int(rng.choice(len(self.relations), p=probs))
        elif mode == "argmax":
            idx = int(np.argmax(probs))
        else:
            raise ValueError("mode must be 'argmax' or 'sample'")

        relation = self.relations[idx]
        returned = relation.target.copy()
        confidence = float(probs[idx])
        success = None if expected is None else bool(np.array_equal(returned, expected))
        self.log.append(
            Observation(
                step=len(self.log) + 1,
                cue=bits(cue),
                criterion=criterion,
                returned_relation=relation.name,
                returned_state=bits(returned),
                confidence=confidence,
                success=success,
            )
        )
        return returned, relation, confidence

    def update_from_observation(self, relation: Relation, success: bool, lr: float = 0.08) -> None:
        """Update a relation after observation feedback."""
        target = 1.0 if success else 0.0
        relation.stability = (1 - lr) * relation.stability + lr * target
        relation.weight *= (1 + lr) if success else (1 - lr)
        relation.weight = float(np.clip(relation.weight, 0.05, 10.0))
        relation.novelty = float(np.clip(relation.novelty * (0.92 if success else 1.08), 0.1, 3.0))


def build_memory(patterns: np.ndarray, beta: float = 6.0) -> AssociativeReturnMemory:
    """Build a memory where each pattern is represented by a self-return relation."""
    mem = AssociativeReturnMemory(beta=beta)
    for i, p in enumerate(patterns):
        mem.add_relation(Relation(name=f"R{i:02d}", key=p.copy(), target=p.copy()))
    return mem
