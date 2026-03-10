# Task: D5-DYNAMIC-COLLAPSE-CORE-001

## Executive Summary
- `[C]` The stable joined-quotient field has an exact three-motif return automaton for color `0`:
  - layer `0` uses `12340` and kicks `q`,
  - layer `1` uses `34012` and kicks `v`,
  - layers `2,3,4+` use `01234` and freeze.
- `[C]` This forces the exact first-return law
  - `R_0(q,w,v,u) = (q+1, w, v+1, u)`
  and therefore forces `U_0 = id` on `(w,u)` and monodromy `0`.
- `[C]` The missing information is a hidden phase
  - `delta := v-q mod m`,
  which the stable return preserves, but the joined quotient `Theta_AB` does not record.
- `[C/H]` The first tail-entry conflict is already visible at the canonical state
  - `L=2|sig=20006` on `m=7`,
  which appears with both `delta=0` and `delta!=0` but must receive the same local permutation because it is a single `Theta_AB` state.
- `[C/H]` Recommended refinement:
  - add one cyclic-equivariant bit
    `phase_align_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m = 0}`.

## Exact Stable-Field Return Law And Forced Consequences
- Deterministic verification passed on `m=5,7,9,11,13`:
  - `R_0(q,w,v,u) = (q+1, w, v+1, u)`
- Stable field palette by layer:
  - layer `0`: permutation `12340`, color-0 output `1`
  - layer `1`: permutation `34012`, color-0 output `3`
  - layers `2,3,4+`: permutation `01234`, color-0 output `0`
- Forced step effects in `(q,w,v,u)`:
  - layer `0`: `(q,w,v,u) -> (q+1,w,v,u)`, so `delta=v-q` decreases by `1`
  - layer `1`: `(q,w,v,u) -> (q,w,v+1,u)`, so `delta` increases by `1`
  - layers `2,3,4+`: `(q,w,v,u)` unchanged, so `delta` is preserved
- Since one full return visits those motifs in order `0 -> 1 -> 2+ -> ... -> 2+`, the net effect is:
  - `q` increases by `1`
  - `v` increases by `1`
  - `w,u` do not move
  - `delta = v-q` is invariant
- Consequences:
  - section return `U_0` is the identity on `(w,u)`
  - every monodromy is `0`

Files:
- `data/return_law_summary.json`
- `data/return_automaton.json`

## Minimal Dynamic-Collapse Motifs
### 1. The `kick-kick-freeze` automaton
- `M0_q_kick`
  - layer bucket `0`
  - permutation `12340`
  - color-0 output `1`
- `M1_v_kick`
  - layer bucket `1`
  - permutation `34012`
  - color-0 output `3`
- `M2_freeze_tail`
  - layer buckets `2,3,4+`
  - permutation `01234`
  - color-0 output `0`

This three-motif family is already enough to force the return law above.

### 2. The first explicit tail conflict
- Canonical background path on `m=7`:
  - step `0`: `L=0|sig=00000`
  - step `1`: `L=1|sig=20200`
  - step `2`: `L=2|sig=20006`
- The tail-entry state `L=2|sig=20006` is already phase-collapsing.
- Two concrete vertices with the same `Theta_AB` state but different hidden phase:
  - aligned example: `[0,1,0,1,0]`, so `delta = 0`
  - misaligned example: `[4,5,0,4,3]`, so `delta = 6`
- Both vertices map to the same joined quotient state
  - `L=2|sig=20006`
  and therefore must share one local permutation on `Theta_AB`.
- In the stable field that shared permutation is `01234`, so the tail cannot branch on phase and the collapse is locked in immediately upon entering layer `2`.

### 3. Collision counts on the representative-color return
- Multi-`delta` states seen along one full `P_0 -> P_0` return:
  - `m=5`: `124`
  - `m=7`: `2338`
  - `m=9`: `4002`
  - `m=11`: `4212`
  - `m=13`: `4212`
- States split by the proposed `phase_align` bit:
  - `m=5`: `51`
  - `m=7`: `893`
  - `m=9`: `1843`
  - `m=11`: `2165`
  - `m=13`: `2260`

So the collapse is not globally diffuse. It is driven by a finite family of phase-colliding tail motifs that the current quotient merges.

Files:
- `data/phase_collision_table.json`
- `data/canonical_background_path.json`
- `data/minimal_collapse_core.json`

## Proposed One-Bit Refinement And Why It Is The Right One
- Recommended extra bit:
  - `phase_align_c(x) = 1_{(v_c-q_c) mod m = 0}`
  - equivalently
    `phase_align_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m = 0}`
- Refined quotient:
  - `Theta_AB_plus_phase_align`
  - `theta_plus(x) = (L(x), (s_c(x), phase_align_c(x))_{c in Z/5Z})`
- Why this bit is the right refinement:
  - the stable return law preserves `delta_c := v_c-q_c`, so `delta_c` is the hidden invariant controlling the collapse;
  - `Theta_AB` merges aligned and non-aligned phase fibers into one local state;
  - `phase_align_c` is the smallest simple cyclic-equivariant test that separates those fibers while leaving the five existing atoms untouched.
- This is a true grammar refinement, not a different search objective:
  - the conflicting cases are genuinely the same `Theta_AB` state,
  - so no solver on the current quotient can assign them different permutations.

File:
- `data/candidate_refinement.json`

## Suggested Next Search Configuration
- Next quotient:
  - `Theta_AB_plus_phase_align`
- Same search style:
  - free-anchor cyclic-equivariant CP-SAT search
  - outgoing Latin on all quotient states
  - incoming Latin on predecessor-pattern classes for `m=5,7,9`
- Same validation targets:
  - `m=5,7,9,11,13`
  - representative-color diagnostics `clean_frame`, `strict_clock`, `U_0` cycle structure, monodromies, full color cycle counts
- Suggested next script names:
  - `scripts/torus_nd_d5_join_phase_align_search.py`
  - `scripts/torus_nd_d5_join_phase_align_validate.py`

This is a sharper branch than “add one more bit” in the abstract. The evidence points to one specific missing bit: the alignment of the hidden phase `v-q`.
