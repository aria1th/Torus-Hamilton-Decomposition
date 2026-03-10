# GPT 5.4 Pro — Session 21 Briefing

## Context
You are continuing the d=5 Hamilton decomposition project.
This is a fresh session. Below is the complete current state.

---

## Template for your responses

```
Return the research note:
Problem:
Current target:
Known assumptions:
Attempt A:
  Idea:
  What works:
  Where it fails:
Attempt B:
  Idea:
  What works:
  Where it fails:
Candidate lemmas:
Needed computations/search:
Next branching options:
Claim status labels:
  [P] [C] [H] [F] [O]
```

If any large code execution or code construction & search is required which is over container, request work template:

```
Work Template:
    Task ID:
    Question:
    Purpose:
    Inputs / Search space:
    Allowed methods:
    Success criteria:
    Failure criteria:
    Artifacts to save:
    - code
    - raw logs
    - summary report
    - discovered examples / counterexamples
    - tables / plots / proof-supporting computations
    Return format:
    Reproducibility requirements:
```

---

## What the problem is

Construct a 5-color Hamilton decomposition of
$$D_5(m) = \mathrm{Cay}((\mathbb{Z}_m)^5, \{e_0,e_1,e_2,e_3,e_4\})$$
for all $m \ge 3$.

The approach: construct a cyclic-equivariant master permutation field
$$\Pi_\theta \in S_5, \qquad f_c(x) = x + e_{\Pi_{\theta(x)}(c)}$$
that satisfies outgoing-Latin, incoming-Latin, and triangular admissibility.

Key theorem (proved): the **orbit-anchor reconstruction lemma** gives
$$\Pi_\theta(c) = a(\rho^{-c}\theta) + c$$
where $a: \Theta \to \mathbb{Z}_5$ is the anchor function.

---

## Where we are now — bottleneck evolution

```
~~clean frame absent~~      → master field solved this (Session 11-13)
~~Latin infeasibility~~     → free-anchor solved this (Session 14)
~~dynamic collapse~~        → diagnosed, R₀=(q+1,w,v+1,u), U₀=id (Session 16)
~~ad-hoc phase bits~~       → δ-partition scan ruled these out (Session 20)
**automaton-derived tail-phase class** → CURRENT CORE PROBLEM
```

---

## Sessions 18–20 results (CRITICAL — please read carefully)

### Session 18: Pilot grammar extraction
- Θ_AB + phase_align yields exactly **2 rigid pilot grammars** on 20879 pilot-realized states:
  - **Strict-collapse**: layer 0 = σ=(1,2,3,4,0), layer 1 = σ³=(3,4,0,1,2), layers 2+ = id
    - Return law: R₀(q,w,v,u) = (q+1, w, v+1, u)
  - **Clean-nonclock**: layer 0 = σ³, layer 1 = id, layers 2+ = id
    - Return law: R₀(q,w,v,u) = (q, w, v+1, u)
- **Both grammars freeze layers 2+ to identity.** The phase-align refinement can only change the first 2 kicks.
- **Key conclusion**: next refinement must target the layer-2 tail grammar itself.

### Session 19: Predecessor bit scan
- Tested all one-step-lagged copies of existing atoms (pred_any_phase_align, pred_sig0_phase_align, pred_sig1_wu2, pred_sig4_wu2)
- Baseline total excess: m=5: 70, m=7: 2673, m=9: 12707
- Best predecessor bits give only marginal reduction (~10-15%)
- **Conclusion**: reusing existing atoms with one-step lag is insufficient

### Session 20: Tail phase scan
- Scanned all one-bit partitions of the hidden nonzero phase set δ ∈ ℤ_m* for m=5,7,9
- **Pure δ-partitions outperform all affine-mixed predicates (aq+bw+cu+δ=t)**
- Best arbitrary δ-partitions:
  - m=5: {1,2} → excess 14 (baseline 70), 80% reduction
  - m=7: {1,3,5} → excess 1282 (baseline 2673), 52% reduction
  - m=9: {1,2,5,6} → excess 8150 (baseline 12707), 36% reduction
- **But**: optimal subset drifts with m — no uniform arithmetic rule
- **Conclusion**: the next bit must come from the return automaton / compatibility hypergraph, not from ad-hoc arithmetic

---

## Your task for this session

The three open problems from Sessions 18-20:

1. **Build the compatibility hypergraph / return automaton** on the residual tail family
   - Extract the equivalence relation on nonzero δ induced by identical predecessor-tail local data
   - Find the coarsest 2-coloring of hidden phase classes that separates the collapse motifs

2. **Compare automaton-derived partition** against pilot-optimal arbitrary δ-partitions for m=5,7,9
   - Does the automaton partition match or explain the pilot-optimal subsets?

3. **Use the result as the next quotient bit** and design the Codex template for the refined quotient search

Alternatively, if you see a better path forward (e.g., proving a no-go theorem or proposing a fundamentally different approach), explain your reasoning.

---

## Attached files (in order of importance)

### Must read:
1. `d5_phase_align_tail_phase_scan_note.md` — Session 20 full research note (tail phase scan)
2. `d5_phase_align_pilot_grammar_note.md` — Session 18 full research note (pilot grammar)
3. `d5_phase_align_simple_predecessor_bit_scan_note.md` — Session 19 quick scan
4. `d5_join_quotient_dynamic_collapse_note_v1.md` — Session 16 dynamic collapse diagnosis

### For reference:
5. `d5_master_field_orbit_anchor_note_v2.md` — orbit-anchor reconstruction lemma + Schema A/B no-go
6. `d5_master_field_branch_note_v1.md` — master field conditional theorem
7. `d5_gpt54pro_strategic_analysis_v2.md` — your own 2nd strategic analysis

### Data files (attach if token budget allows):
8. `d5_phase_align_tail_phase_scan_summary.json` (65KB) — full δ-partition scan data
9. `d5_phase_align_pilot_grammar_analysis_summary.json` (9KB) — grammar rigidity data
10. `d5_phase_align_simple_predecessor_bit_scan.json` (7KB) — predecessor scan data

---

## Notation reminders
- $\theta = (\text{layer}, \text{sig})$ where layer ∈ {0,1,2,3,4+} and sig encodes phase relationships
- $\delta = v - q \pmod{m}$ is the "hidden tail phase"
- Strict-collapse: all Latin-feasible fields use only {σ, id} permutations, yielding trivial U₀
- Dynamic collapse: Latin is satisfied but R₀ is trivial (pure translation, no nontrivial section return)
- Quotient Θ_AB: join of Schema A and Schema B, 9427 states, 1899 rotation orbits
