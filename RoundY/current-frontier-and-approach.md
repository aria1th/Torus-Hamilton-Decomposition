# Current Frontier And Approach

This note is the compact working guide for the current D5 branch.

It has four jobs:

1. state the **real current problem**
2. explain the **current working approach**
3. preserve the **research-note / work-template format**
4. list the **critical theorem targets** worth proving or extracting next

Use it together with:

- [README.md](./README.md)
- [d5_progress_master_summary.md](./d5_progress_master_summary.md)
- [d5_autonomous_perturbation_note_v25.md](./autonomous/d5_autonomous_perturbation_note_v25.md)
- [routeY_status_summary_045.md](./routeY_status_summary_045.md)
- [d5_carry_transition_horizon_followup_045.md](./d5_carry_transition_horizon_followup_045.md)
- [theorem/d5_proof_program_050.md](./theorem/d5_proof_program_050.md)
- [theorem/d5_boundary_reset_and_tau_proof_052.md](./theorem/d5_boundary_reset_and_tau_proof_052.md)
- [theorem/d5_positive_theorem_chain_054.md](./theorem/d5_positive_theorem_chain_054.md)
- [theorem/d5_boundary_reset_uniform_proof_attempt_055.md](./theorem/d5_boundary_reset_uniform_proof_attempt_055.md)
- [theorem/d5_CJ_branch_proof_reduction_056.md](./theorem/d5_CJ_branch_proof_reduction_056.md)
- [DOCUMENT_FOR_EXTERNAL_REVIEW.md](../DOCUMENT_FOR_EXTERNAL_REVIEW.md)
- [formal/README-D5.md](../formal/README-D5.md)

RoundY D5 support files now live in:

- `RoundY/specs/` for executable specs and work templates
- `RoundY/checks/` for small JSON prep checks and follow-up summaries
- `RoundY/theorem/` for theorem-shaping notes and snippets
- root `RoundY/` for session summaries such as `codex_work_s59.md`

## Current real problem

After artifacts `017–055`, the live D5 obstruction is no longer:

- missing clean frame
- missing Latin feasibility
- missing any mixed witness
- missing a better one-bit separator
- missing a slightly larger tiny transducer

The actual frontier is:

**find an admissible/local coding of the countdown carrier `tau`, now that the
structural theorem branch is explicit, the first carry-only admissible
catalogs are dead, the carry sheet is already the first exact future-transition
event, the first exact checked-range carry coding is known, and the internal
`tau` dynamics have already reduced to countdown plus tiny reset law**

`R1 -> H_L1`

for the best endpoint seed

- left `[2,2,1]`
- right `[1,4,4]`.

What is already known:

- `019`: the canonical mixed witness has an explicit reduced return-map model
- `023–025`: the right reduced perturbation target is known
- `032`: the best local endpoint seed is isolated
- `033`: the defect graph is bounded and tiny transducers are pruned on the
  current alphabet
- `034`: the unresolved corridor admits a first-pass projected phase model on
  `(s, layer)`
- `035`: the first raw static phase-exposure layer is already pruned
- `036`: `(s, layer)` is only a first-pass projected phase lap, and the traced
  long corridor lifts exactly to `(q, a, layer)`
- `037`: that lifted state is already visible on raw `(q,w,layer)`, so the
  next live problem is corridor localization rather than phase exposure
- `038`: in a simple one-step neighborhood alphabet, the exceptional source bit
  is already birth-local, while the source marker and entry marker are still
  absent up to projection size `5`
- `039`: in exact raw current coordinates, the source and entry birth classes
  are already explicit, and the family bit then drifts through all residues
  later, so it must be transported
- `040`: the first richer source-edge / lagged lifts of the same simple `038`
  row still fail, while the raw current coordinate family already closes the
  reduced control logic on the checked active union
- `041`: the first `025`-style grouped-state-descending admissible families
  still fail exactly; `w` already descends as `s-u`, but the fire predicates do
  not descend to current grouped state `(s,u,v)`, even after conditioning on
  family
- `042`: the carry-slice bit `1_{q=m-1}` is the smallest verified trigger lift,
  but the closed structural object is better read as a tiny finite cover over
  `B = (s,u,v,layer,family)`, with fiber size at most `3` on the checked range
- `043`: that cover sharpens to
  `B`, then `B+c`, then a residual binary noncarry sheet over `B+c`;
  the minimal deterministic cover over `B+c` is `2`-sheet on the checked
  active union, and the residual sheet is not the obvious bit `1_{q=m-2}` on
  `m=7,9,11`
- `044`: the theorem branch becomes explicit:
  the residual sheet can be chosen as
  `d = 1_{next carry u >= m-3}`,
  so the checked active branch factors as
  `B <- B+c <- B+c+d`
  with `d` a binary anticipation sheet
- `045`: the first carry-only admissible catalogs are pruned exactly:
  `0` exact candidates across the checked
  current-edge / label / delta core catalog up to size `5`,
  low-cardinality `025`-style gauge-transition catalog up to size `5`,
  and targeted point-defect catalog up to size `4`.
  Full `B -> B_next` and `B -> B_next -> B_next2` grouped transition classes
  also fail.
  The best negatives are `next_dn` and `dn + next_dn`, exact on `m=5` but
  missing only regular carry `B`-states on `m=7,9,11`.
- `046`: the carry sheet is already an exact future-transition event on the
  checked active grouped base.
  The minimal exact future `dn` horizon is `m-3` on `m=5,7,9,11`, the minimal
  exact future grouped-state horizon is `m-2`, and the exact future window
  compresses to
  current `B` plus
  `initial flat-run length where dn=(0,0,0,1)` plus
  `first nonflat dn`.
  Flat-run length alone is not exact, and the `H-1` ambiguity is confined to
  regular carry `B`-states.
- `047`: that exact future carry target sharpens further.
  The boundary event class at `tau=0` is genuinely `3`-class minimal:
  `wrap`, `carry_jump`, `other`.
  The first exact checked-range quotient is
  `B + min(tau,8) + epsilon4`.
  Equivalently, the first exact checked-range transition-sheet coding is
  current `B` plus current `epsilon4` plus the next `7` future binary
  flat/nonflat indicators after the current step.
  So the live hidden datum is `tau`, not a vague larger future sheet.
- `048`: `tau` itself now has exact internal dynamics on the checked active
  nonterminal branch.
  Whenever `tau > 0`, the next value is exactly `tau-1`.
  All nontrivial dynamics are confined to the boundary `tau=0`, where
  `wrap -> 0`, `carry_jump` resets exactly on `(s,v,layer)`, and `other`
  resets exactly on `(s,u,layer)`.
  So the live local target is better read as a countdown carrier with a tiny
  reset law.
- `049`: the stronger source-memory refinement also survives a larger direct
  replay range.
  Through `m=19`, with `rho = source_u + 1 mod m`,
  `tau` is exact on `(s,u,v,layer,rho)`,
  `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
  `c` is exact on `(u,rho,epsilon4)`,
  and `q ≡ u-rho+1_{epsilon4=carry_jump} mod m`.
  But `rho` is not recoverable from `(B,tau,epsilon4)` once `m>=7`, so this is
  a stronger constructive refinement, not the theorem-side minimal object.
- `050`: the two narrow proof-support checks also persist through `m=19`.
  The `048` reset law remains exact on the same theorem-side quotients, and
  the explicit `047/048` witness pair persists with the same `m-4` lower-bound
  shape.
- `052`: the proof-direction evidence stays stable through `m=19`.
  The expected per-modulus horizon pattern persists, the positive-route
  reset-law support stays exact, and the negative-route witness support
  remains stable.
- `055`: the positive route sharpens further through `m=23`.
  The `carry_jump` branch formula, the raw identity
  `q = 1-s-v-layer`, the `other`-branch subtype law, and `wrap -> 0`
  all remain exact on the extended checked range.
  So the honest positive-route target is no longer a vague uniform reset law;
  it is the proof of the two branch lemmas `CJ` and `OTH`.

So the next branch should be read as:

**admissible/local coding of the countdown carrier `tau`, now that the
structural theorem branch is explicit, the carry sheet is already the first
exact future-transition event, the exact checked-range coding boundary is
known, and the internal `tau` dynamics have been reduced to countdown plus
tiny reset law**.

## What the current approach should be

The right mental order is:

1. keep the reduced model fixed
2. understand the obstruction in the smallest exact coordinates available
3. only then search for the smallest local realization that matches that model

In practice, that means:

- do not reopen broad one-bit scans
- do not reopen generic `2`-state / `3`-state transducer searches on the same
  alphabet
- do not widen static endpoint-word families unless a phase-aware ingredient is
  added

The guiding proof picture is now:

- theorem branch:
  the active best-seed mechanism is already cleanly described by
  `B <- B+c <- B+c+d`;
- local branch:
  the remaining work is to code the carry event admissibly, not to invent a
  new reduced controller;
- bridge:
  once the carry event is local, the reduced trigger logic should slot into the
  existing `025` grouped target and the finite-cover theorem becomes the clean
  structural wrapper around it.

The proof program itself now has two honest routes sharing that same picture:

- negative route:
  package `046/047/048` into a bounded-horizon reduction and then apply the
  explicit witness family showing that no fixed future flat/nonflat horizon
  can code the carry sheet uniformly in `m`;
- positive route:
  package `048/050/052/055/056` into a countdown/reset theorem where `tau` is
  the main hidden datum, `tau_next = tau-1` away from the boundary, and the
  `tau=0` reset is governed by the small current-state classes `wrap`,
  `carry_jump`, and `other`, with the remaining burden reduced to the two
  branch lemmas `CJ` and `OTH`;
- compute route:
  allow the stronger current-memory refinement `(B,rho)` from `049` when the
  goal is constructive support rather than the theorem-side minimal object.

The first honest next moves are:

1. separate trigger-level lifts from closed structural lifts
2. target the carry sheet before any attempt to localize the residual sheet
3. treat the structural object as
   `B <- B+c <- B+c+d`
   with `d = 1_{next carry u >= m-3}` a binary anticipation sheet
4. do not reopen the first carry-only catalogs already killed by `045`
5. do not describe the next object as an amorphous broader future sheet when
   `046–048` already reduce it to a countdown carrier with tiny reset law
6. only then open genuinely new observable families, not lifts of the same
   simple `038` row
7. treat `epsilon` as a secondary boundary correction and the positive
   countdown of `tau` as the main hidden datum
8. keep the theorem-side object minimal, but allow compute branches to use the
   stronger current-memory refinement `(B,rho)` when they are explicitly
   constructive rather than theorem-packaging

## Brief explanation of `docs/suggested_workflow.md`

The workflow note is not just project-management advice. It encodes the
research pattern that already worked on this project.

The short version is:

1. **Explorer**
   writes a research note, not a final answer
2. **Executor**
   turns the sharp part into exact computation / search / counterexample checks
3. **Critic**
   attacks the current branch, especially the claimed bottleneck
4. **Synthesizer**
   compresses results into a real branch choice
5. **Human**
   chooses the next direction

What matters most from that workflow:

- first outputs are **research assets**, not final truths
- every failed branch must return a usable obstruction, not only “no”
- every computational task should have a narrow question, explicit failure
  criterion, and reproducible artifacts
- the next branch should be chosen only after the obstruction is sharpened

That is exactly how the D5 branch progressed from:

`dynamic collapse -> mixed witness -> reduced target -> endpoint seed -> defect quotient -> corridor phase`

## Research note template

This is copied from `docs/template_to_use.md` and should stay stable:

```text
Return the research note :
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

If any large code execution or code construction & search is required which is over container, request work template: (You can use 300s of compute internally, we can use more if required.)

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

## Critical theorem targets

These are the theorem-shaped objects worth seeking now.

### A. Already extracted, worth formalizing cleanly

1. **Mixed return-map theorem**
   For the canonical mixed witness, prove the explicit reduced first-return and
   grouped-return formulas from `019`.

2. **Reduced perturbation target theorem**
   Prove the reduced-model statement behind `025`:
   omit-base plus edge-tied point cocycle defect gives a single grouped orbit
   of size `m^3`.

3. **Best-seed defect quotient theorem**
   Prove the exact bounded defect law from `033`:
   per color, four overfull families against four hole families, with only
   `R1 -> H_L1` unresolved.

4. **Corridor phase theorem**
   Prove the `034` phase model:
   after the initial `R1` alt-`2` entry, the corridor projects to `(s, layer)`
   and follows the exact map `F_rho`, with one small orbit of size `m` and one
   large orbit of size `m(m-1)`.

5. **Static phase-gate no-go theorem**
   Formalize the `035` boundary:
   no `1`- or `2`-coordinate raw current-cell projection isolates the first
   `H_L1` exit on every best-seed corridor, and every static `B`-state gate
   built from the separating `3`-coordinate projections fails incoming Latin on
   the pilot range.

6. **Corridor lift theorem**
   Formalize the `036` clarification:
   the `034` `(s, layer)` rule is only a first-pass projected lap, while the
   traced long corridor follows an exact lifted rule on `(q, a, layer)` up to
   first exit.

7. **Raw odometer theorem**
   Formalize the `037` extraction:
   the lifted state is already visible on raw `(q,w,layer)`, and the traced
   corridor is an exact `m^3` odometer with two universal first-exit targets.

### B. The next real theorem targets

8. **Grouped-state no-go theorem**
   Formalize the `041` boundary:
   any observable family that descends to the current grouped state `(s,u,v)`
   still fails to realize the fire predicates, even after conditioning on the
   carried family bit.

9. **Carry-slice theorem**
   Formalize the `042` trigger-level lift:
   exceptional fire descends to
   `B = (s,u,v,layer,family)`,
   regular fire descends to `B` plus the carry bit
   `c = 1_{q=m-1}`,
   and `c` is not a function of `B`.

10. **Residual two-sheet theorem**
   Extract the `044` structural lift cleanly:
   over the checked active union, the minimal deterministic cover over `B+c`
   is `2`-sheet, its support lies entirely on the regular noncarry branch,
   and it can be chosen as
   `d = 1_{next carry u >= m-3}`.

11. **First carry-family no-go theorem**
   Formalize the `045` boundary:
   no exact carry realization appears in the first admissible
   current-edge / `1`-step / `2`-step / low-cardinality anchored-gauge
   catalogs, and the full `B -> B_next` and `B -> B_next -> B_next2` grouped
   transition classes still fail.

12. **Deep-transition carry-sheet theorem**
   Formalize the `046` extraction:
   the minimal exact future `dn` horizon is `m-3`,
   the minimal exact future grouped-state horizon is `m-2`,
   and the exact future window compresses to
   current `B` plus
   `initial flat-run length + first nonflat dn`.

13. **Exact checked-range carry-coding theorem**
   Formalize the `047` extraction:
   the `tau=0` boundary event class is genuinely `3`-class minimal,
   the first exact checked-range quotient is
   `B + min(tau,8) + epsilon4`,
   and the first exact checked-range transition-sheet coding is
   current `B` plus current `epsilon4` plus the next `7` future binary
   flat/nonflat indicators after the current step.

14. **Localized-carrier theorem**
   Identify the smallest local mechanism that can create and preserve a marker
   on the intended corridor while using the visible raw odometer phase to fire
   at the right target.

15. **Carry-priority local theorem**
   Show that the next honest local target is still the carry sheet `c`,
   not the full anticipation sheet `d`.

16. **Residual-sheet no-go / coordinatization theorem**
   Prove either:
   - the anticipation sheet `d` is not any small current observable in the
     intended local class, or
   - the smallest admissible observable that realizes it.

17. **Visible-phase no-go theorem**
   Strengthen the computational `033/034/035/036/037` obstruction into a real
   statement: visible raw phase alone is insufficient without corridor
   localization.

18. **Local-to-reduced realization theorem**
   Show that if a local mechanism realizes the extracted phase target while
   preserving the reduced `025` structure to first order, then the grouped
   orbit target follows.

19. **Bridge-to-full-D5 theorem**
   Convert the right reduced/local realization into the full Hamilton
   decomposition statement for D5.

### C. Useful supporting lemmas

These are smaller but likely necessary.

1. **Exceptional-slice lemma**
   In `034/036`, the exceptional long-delay family is exactly `u_source = 3`.

2. **Delay law lemma**
   The short/long delays are:
   - `Delta_short = (m-3)m^2 - 1`
   - `Delta_long = Delta_short + m(m-1)`

3. **Orbit-residue lemma**
   The first-exit residue mod the large-orbit period is
   `m^2 - 3m - 1`.

4. **Small-orbit description lemma**
   For source parameter `rho`, the excluded orbit is
   `M_rho = {(rho, layer): layer != 2} union {(rho+1,2)}`.

5. **Lifted entry/exit lemma**
   In `036`, the lifted entry and first-exit states are:
   - entry `(m-1, 0, 2)`
   - regular exit `(m-1, m-4, 1)` via `[2]`
   - exceptional exit `(m-2, m-4, 1)` via `[1]`

6. **Raw-target lemma**
   In `037`, the universal raw first-exit targets are:
   - regular `(m-1, m-2, 1)` via `[2]`
   - exceptional `(m-2, m-1, 1)` via `[1]`

## Practical search guidance

If starting a new branch, ask these first:

1. Does the proposal localize to the intended corridor, or only restate the
   already-visible raw phase?
2. Does it add a real carrier / trigger mechanism, or only rename the odometer?
3. Can the branch be tested first on the best seed `[2,2,1] / [1,4,4]`?
4. Does failure produce a sharper obstruction than the previous branch?

If the answer to the first two is “no”, the branch is probably too weak.

## Short version

The current D5 branch should be thought of as:

**projected phase known, raw odometer known, corridor localization still
unknown**

That is the real frontier.
