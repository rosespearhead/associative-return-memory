"""Reproducible ARM-Sim experiments.

Run from repository root:

    python experiments/run_experiments.py
"""
from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import matplotlib.pyplot as plt

from arm_sim import build_memory, corrupt_pattern, random_patterns, bits

RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def experiment_recall_under_noise(seed: int = 7) -> None:
    rng = np.random.default_rng(seed)
    patterns = random_patterns(n_patterns=32, n_bits=12, rng=rng)
    noise_levels = np.linspace(0.0, 0.45, 10)
    rows = []

    for beta in [2.0, 4.0, 8.0]:
        for noise in noise_levels:
            mem = build_memory(patterns, beta=beta)
            trials = 400
            correct = 0
            mean_conf = 0.0
            for _ in range(trials):
                idx = int(rng.integers(0, len(patterns)))
                cue = corrupt_pattern(patterns[idx], noise, rng)
                returned, relation, conf = mem.return_state(cue, criterion="hybrid", expected=patterns[idx])
                correct += int(np.array_equal(returned, patterns[idx]))
                mean_conf += conf
            rows.append({
                "beta": beta,
                "noise": float(noise),
                "accuracy": correct / trials,
                "mean_confidence": mean_conf / trials,
            })

    csv_path = RESULTS / "experiment_1_recall_under_noise.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    plt.figure(figsize=(7.2, 4.5))
    for beta in sorted(set(r["beta"] for r in rows)):
        xs = [r["noise"] for r in rows if r["beta"] == beta]
        ys = [r["accuracy"] for r in rows if r["beta"] == beta]
        plt.plot(xs, ys, marker="o", label=f"beta={beta:g}")
    plt.xlabel("Bit-flip noise in cue")
    plt.ylabel("Return accuracy")
    plt.title("ARM relation-return accuracy under noisy cues")
    plt.ylim(-0.02, 1.02)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "experiment_1_recall_under_noise.png", dpi=180)
    plt.close()


def experiment_commander_criteria(seed: int = 11) -> None:
    rng = np.random.default_rng(seed)
    patterns = random_patterns(n_patterns=24, n_bits=10, rng=rng)
    mem = build_memory(patterns, beta=5.0)

    for i, rel in enumerate(mem.relations):
        if i < 8:
            rel.stability = 1.8
            rel.novelty = 0.4
            rel.weight = 1.2
        elif i < 16:
            rel.stability = 0.7
            rel.novelty = 2.1
            rel.weight = 1.1
        else:
            rel.stability = 0.8
            rel.novelty = 0.8
            rel.weight = 0.8

    cue = corrupt_pattern(patterns[5], 0.20, rng)
    criteria = ["similarity", "stability", "novelty", "hybrid"]
    rows = []
    for criterion in criteria:
        probs = mem.probabilities(cue, criterion=criterion)
        top = np.argsort(probs)[::-1][:5]
        for rank, idx in enumerate(top, start=1):
            rel = mem.relations[int(idx)]
            rows.append({
                "criterion": criterion,
                "rank": rank,
                "relation": rel.name,
                "target": bits(rel.target),
                "probability": float(probs[idx]),
                "stability": rel.stability,
                "novelty": rel.novelty,
            })

    csv_path = RESULTS / "experiment_2_commander_criteria.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    top_probs = []
    top_names = []
    for criterion in criteria:
        probs = mem.probabilities(cue, criterion=criterion)
        idx = int(np.argmax(probs))
        top_probs.append(float(probs[idx]))
        top_names.append(mem.relations[idx].name)

    plt.figure(figsize=(7.2, 4.5))
    plt.bar(criteria, top_probs)
    plt.ylabel("Top relation probability")
    plt.title("Observer-Commander criterion changes the returned relation")
    for i, name in enumerate(top_names):
        plt.text(i, top_probs[i] + 0.01, name, ha="center")
    plt.ylim(0, min(1.0, max(top_probs) + 0.2))
    plt.tight_layout()
    plt.savefig(RESULTS / "experiment_2_commander_criteria.png", dpi=180)
    plt.close()


def experiment_feedback_learning(seed: int = 13) -> None:
    rng = np.random.default_rng(seed)
    patterns = random_patterns(n_patterns=20, n_bits=12, rng=rng)
    mem = build_memory(patterns, beta=4.0)
    rows = []

    for epoch in range(1, 31):
        correct = 0
        trials = 200
        for _ in range(trials):
            idx = int(rng.integers(0, len(patterns)))
            cue = corrupt_pattern(patterns[idx], 0.25, rng)
            returned, rel, conf = mem.return_state(cue, criterion="hybrid", expected=patterns[idx])
            success = bool(np.array_equal(returned, patterns[idx]))
            correct += int(success)
            mem.update_from_observation(rel, success=success, lr=0.04)
        rows.append({
            "epoch": epoch,
            "accuracy": correct / trials,
            "mean_weight": float(np.mean([r.weight for r in mem.relations])),
        })

    csv_path = RESULTS / "experiment_3_feedback_learning.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    plt.figure(figsize=(7.2, 4.5))
    plt.plot([r["epoch"] for r in rows], [r["accuracy"] for r in rows], marker="o")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Observation feedback changes future return likelihood")
    plt.ylim(0, 1.02)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS / "experiment_3_feedback_learning.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    experiment_recall_under_noise()
    experiment_commander_criteria()
    experiment_feedback_learning()
    print(f"Wrote results to {RESULTS}")
