# Associative Return Memory (ARM)

## A Relation-Centric Memory Layer for Recomputable Quantum and Quantum-Inspired States

**White Paper v0.5 — English publication draft**  
**Concept:** Alexandra Naumova  
**Date:** June 2026

---

## Abstract

Quantum processors have moved from laboratory demonstrations to publicly documented hardware systems, while scalable quantum memory remains a central bottleneck for distributed quantum computing, quantum repeaters, and memory-assisted algorithms. Existing approaches typically frame memory as either physical preservation of a quantum state, random access to data in superposition, or associative retrieval of stored patterns.

This white paper proposes **Associative Return Memory (ARM)**, a relation-centric memory layer in which memory does not store a state as an addressable object. Instead, memory stores a **return relation**: a structured link by which a state can be recomputed, reactivated, or returned under an Observer-Commander criterion.

The core thesis is:

> Memory stores relations; states are events of recomputation.

In ARM, a state is treated as the result of a computational process conditioned by input cues, relation weights, context, and an observer-selected criterion. Classical storage records observations and updates relation weights, but it does not claim to preserve the complete pre-observation state.

ARM is positioned as a bridge between quantum memory, qRAM, quantum associative memory, and quantum-inspired AI memory. The proposal is intended to be tested first through simulation (**ARM-Sim v0.6**) and later through constrained quantum-circuit analogues.

---

## 1. Motivation

Contemporary quantum processing units are no longer purely hypothetical. IBM documents Heron-class processors; Google has reported Willow processors in the context of below-threshold surface-code memories; Quantinuum announced a 56-qubit H2 trapped-ion system; and IonQ publishes roadmap and product materials around trapped-ion systems and algorithmic-qubit targets.

These systems demonstrate that state preparation, gate control, mid-circuit measurement, and error correction are progressing rapidly. However, the memory problem is not solved by the existence of a QPU alone.

A quantum processor can generate and transform state, but a practical architecture also needs a way to preserve, return, or re-enter useful computational states without treating measurement as ordinary reading. Quantum memory research addresses physical preservation and retrieval. qRAM addresses coherent data access. Quantum associative memory addresses pattern recall.

ARM begins from the same practical pressure but asks a different architectural question:

> What if memory should not store the state, but store the relation by which the state can be recomputed when needed?

---

## 2. Problem statement

The memory problem addressed by ARM can be expressed as four constraints:

1. The useful object is not always a classical value; it may be a computational state, a distribution, or a relation among states.
2. Direct observation produces a classical trace but changes what can be accessed thereafter.
3. Repeated use of a useful state often requires re-preparation, recomputation, error correction, or a separate physical memory mechanism.
4. Existing memory architectures often separate storage from computation, while stateful intelligence-like behavior requires memory to participate in recomputation.

The central research question is:

> How can a system remember a state without storing the state itself?

---

## 3. Core thesis

ARM proposes that the remembered object is not the state `S`, but a return relation `R` that can reinstantiate `S` as a computation under a criterion `K`.

### Central formula

```text
S_t = C(x_t, R, W, K, H)
```

Where:

- `S_t` is the returned state at time `t`;
- `C` is the recomputation operator;
- `x_t` is the current cue or stimulus;
- `R` is the set of stored return relations;
- `W` are learned weights or significance values;
- `K` is the Observer-Commander criterion;
- `H` is the history of observations stored classically.

Short form:

> Memory stores relations.  
> State is recomputed.  
> Observation updates future return.

---

## 4. Architecture

ARM contains five layers:

| Layer | Function | Stored object |
|---|---|---|
| QPU / state generator | Generates and transforms candidate states | No persistent state claim |
| Relation memory | Stores links by which states can be returned | Relations, weights, keys, context links |
| Observer-Commander | Selects criterion or basis of return | Current task criterion `K` |
| Observation log | Stores final observations and outcomes | Classical traces `H` |
| Feedback controller | Updates relation weights and future return likelihood | Weight updates, stability, novelty |

The architecture is deliberately agnostic about whether the first implementation is physical quantum hardware, a quantum circuit simulator, a quantum-inspired vector system, or an AI memory layer.

What matters is the separation between relation storage and state recomputation.

---

## 5. Formal model

Let memory be a graph:

```text
M = (V, E, W)
```

where nodes represent cues, partial patterns, state descriptors, contexts, or observation traces. Edges `E` are return relations.

A relation `r_i` can be defined as:

```text
r_i = (k_i, T_i, w_i, sigma_i, nu_i)
```

Where:

- `k_i` is an activation key;
- `T_i` is a recomputation transform or target-generating rule;
- `w_i` is relation strength;
- `sigma_i` is stability;
- `nu_i` is novelty or exploration potential.

Given a cue `x` and Observer-Commander criterion `K`, ARM computes relation activation:

```text
a_i = score_K(x, k_i, w_i, sigma_i, nu_i)
```

A probability-like return distribution may be defined as:

```text
p_i = exp(beta * a_i) / sum_j exp(beta * a_j)
```

The returned state is not read from memory as a stored value. It is recomputed from the selected or sampled relation:

```text
S_return = T_i(x, context)
```

After observation `y`, relation weights are updated:

```text
w_i(t+1) = update(w_i(t), y, success, K)
```

This makes ARM a closed loop: observation does not merely record what happened; it changes the future likelihood of returning similar states.

---

## 6. Relation to existing work

| Paradigm | Primary goal | What is stored/accessed | ARM distinction |
|---|---|---|---|
| Quantum memory | Preserve quantum states for later retrieval | Physical quantum state | ARM stores return relations; state can be recomputed rather than preserved as object. |
| qRAM | Access data with quantum addresses | Memory cells addressed coherently | ARM is not primarily address → content; it is cue + criterion → relation → state. |
| Quantum associative memory | Retrieve stored pattern from partial/noisy query | Stored pattern distribution | ARM generalizes recall to relation-weighted state recomputation and observation feedback. |
| Quantum cognition | Model context-dependent decisions with quantum-like probability | Mathematical state/model | ARM can serve as a memory architecture for quantum-inspired cognitive systems. |
| Classical AI vector memory | Retrieve semantically close documents/facts | Embeddings and documents | ARM returns computational states, not only facts or nearest-neighbor text chunks. |

The proposed novelty is not the isolated existence of associative recall, quantum memory, or qRAM. The novelty is the explicit architectural thesis that memory stores a return relation, while the remembered state is a recomputation event governed by an observer-selected criterion and updated by classical observation traces.

---

## 7. ARM-Sim v0.6 prototype

ARM-Sim v0.6 is a minimal reproducible code prototype accompanying this white paper. It implements:

- relation memory with cues, targets, weights, stability, and novelty;
- an Observer-Commander criterion;
- probability-like relation activation;
- returned/recomputed state selection;
- classical observation logs;
- feedback updates.

It is intentionally quantum-inspired rather than a claim of physical quantum simulation.

The prototype includes three experiments:

1. **Recall under noisy cues** — tests whether stored relations can return the intended state as cue corruption increases.
2. **Observer-Commander criteria** — tests how similarity, stability, novelty, and hybrid criteria change the returned relation.
3. **Feedback learning** — tests whether observation logs can modify future relation-return likelihood.

---

## 8. Limitations and falsifiability

ARM should be treated as a model, not as a proven physical memory device. Its claims can fail in several ways:

- if relation-return simulation performs no better than direct nearest-neighbor retrieval under controlled benchmarks;
- if feedback updates destabilize memory and prevent reliable state return;
- if the architecture cannot be translated into useful quantum-circuit or quantum-inspired computational primitives;
- if the Observer-Commander criterion adds complexity without measurable benefit;
- if expert review shows that the memory/recomputation distinction is already fully covered by an existing formalism.

The strongest falsifiable claim is:

> Relation-centric memory can outperform state-centric storage or nearest-neighbor retrieval in tasks where the required output is a recomputed state conditioned by context, history, and observer criterion.

---

## References

1. IBM Quantum Documentation. Processor types: Heron processor family. IBM Quantum Platform documentation. URL: https://quantum.cloud.ibm.com/docs/guides/processor-types
2. Acharya, R. et al. *Quantum error correction below the surface code threshold*. Nature 638, 920–926 (2025). DOI: 10.1038/s41586-024-08449-y. arXiv:2408.13687.
3. Google Quantum AI. *Meet Willow, our state-of-the-art quantum chip*. Google Research Blog, 9 Dec 2024. URL: https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/
4. Quantinuum. *Quantinuum launches trapped-ion 56-qubit quantum computer H2-1*. Press release, 5 Jun 2024. URL: https://www.quantinuum.com/press-releases/quantinuum-launches-industry-first-trapped-ion-56-qubit-quantum-computer-that-challenges-the-worlds-best-supercomputers
5. IonQ. Roadmap and trapped-ion system specifications. URL: https://www.ionq.com/roadmap
6. NIST. *Quantum Networks: Glossary and quantum memory/repeater terminology*. URL: https://www.nist.gov/pml/productsservices/quantum-networks-nist/quantum-networks-nist-glossary
7. Giovannetti, V., Lloyd, S., and Maccone, L. *Quantum random access memory*. Physical Review Letters 100, 160501 (2008). DOI: 10.1103/PhysRevLett.100.160501. arXiv:0708.1879.
8. Giovannetti, V., Lloyd, S., and Maccone, L. *Architectures for a quantum random access memory*. Physical Review A 78, 052310 (2008). DOI: 10.1103/PhysRevA.78.052310. arXiv:0807.4994.
9. Ventura, D. and Martinez, T. *Quantum associative memory*. Information Sciences 124(1–4), 273–296 (2000). DOI: 10.1016/S0020-0255(99)00101-2. arXiv:quant-ph/9807053.
10. Trugenberger, C. A. *Probabilistic quantum memories*. Physical Review Letters 87, 067901 (2001). DOI: 10.1103/PhysRevLett.87.067901.
11. Trugenberger, C. A. *Quantum pattern recognition*. Quantum Information Processing 1, 471–493 (2002). DOI: 10.1023/A:1024022632303. arXiv:quant-ph/0210176.
12. Ezhov, A. A., Nifanova, M. Yu., and Ventura, D. *Quantum associative memory with distributed queries*. Information Sciences 128(3–4), 271–293 (2000). DOI: 10.1016/S0020-0255(00)00057-8.
13. Busemeyer, J. R. and Bruza, P. D. *Quantum Models of Cognition and Decision*. Cambridge University Press (2012). DOI: 10.1017/CBO9780511997716.
14. Li, A. et al. *Systems architecture for quantum random access memory*. MICRO 2023. DOI: 10.1145/3613424.3614270. arXiv:2306.03242.
