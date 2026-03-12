# D5-RAW-BIRTH-MARKER-TRANSPORT-039

## Research note

Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, after `037` made the best-seed
corridor phase visible on raw current coordinates and `038` showed that the
simple birth-local bit alphabet does not isolate the source marker.

Current target:
Replace the vague next target

- “find a richer source-local marker somehow”

by the sharper target

- **first extract the exact raw current-coordinate birth formulas for the
  source and entry slices, then search only for the smallest carrier
  persistence / trigger mechanism that transports that birth marker through the
  visible raw odometer.**

The reason for the sharpened target is that the `038` no-go applies only to
its simple bit alphabet. A direct exact-coordinate check on the current bundle
suggests that the source and entry slices are already exact on raw current
coordinates, so the live issue may already have shifted from **birth** to
**transport**.

Known assumptions:
- `025` remains the correct reduced target:
  - omit-base plus edge-tied point cocycle defect,
  - grouped base orbit size `m^2`,
  - full grouped orbit size `m^3`.
- `032` isolates the best endpoint seed
  - left `[2,2,1]`,
  - right `[1,4,4]`.
- `033` reduces the best-seed defect to the unresolved channel
  - `R1 -> H_L1`.
- `035` prunes static phase gates on the earlier raw/current alphabet.
- `036` lifts the corridor from the projected `(s,layer)` picture to an exact
  traced rule on `(q,a,layer)`.
- `037` shows that the lifted corridor state is already visible on raw
  `(q,w,layer)` and extracts the raw odometer `chi` with universal targets
  - regular target `(m-1,m-2,1)` via `[2]`,
  - exceptional target `(m-2,m-1,1)` via `[1]`.
- `038` shows, in the simple birth-local neighborhood alphabet built from
  current plus one-step predecessor/successor `phase_align/wu2` bits, that:
  - there are no source-marker isolators up to projection size `5`,
  - there are no entry-marker isolators up to projection size `5`,
  - the exceptional source slice is already cheap at birth via
    `pred2_wu2` or `pred4_wu2`.

New prep facts checked while preparing this `039` spec:
- For `m = 5,7,9,11`, the full source slice `R1` is exactly
  \[
  \{\text{layer}=1,\ q=m-1,\ w=0,\ u\neq 0\}.
  \]
- On the same checked moduli, the exceptional source slice is exactly
  \[
  \{\text{layer}=1,\ q=m-1,\ w=0,\ u=3\}.
  \]
- The alt-`2` entry slice of that source class is exactly
  \[
  \{\text{layer}=2,\ q=m-1,\ w=1,\ u\neq 0\},
  \]
  and the exceptional entry slice is exactly
  \[
  \{\text{layer}=2,\ q=m-1,\ w=1,\ u=3\}.
  \]
- On representative regular and exceptional corridor traces from `036`, the
  current raw `u` value drifts through all residues, so the family bit is not
  statically recoverable later from current `u`; it still needs initialization
  at birth and transport.

These prep facts are exact checks on the current bundle and should be saved as
first-class `039` outputs before any wider carrier search.

Attempt A:
  Idea:
  Treat the source-local marker as an exact raw current-coordinate predicate,
  not as a small projection in the `038` bit alphabet.
  What works:
  - The source slice appears to be exactly the raw birth class
    `layer=1, q=m-1, w=0, u!=0` on every checked `m = 5,7,9,11`.
  - The exceptional family bit appears to be even cheaper than `038` claimed:
    inside that source class it is simply `u=3` at birth.
  - The entry slice also has an exact raw formula:
    `layer=2, q=m-1, w=1, u!=0`, with exceptional entry `u=3`.
  - If those formulas are confirmed and saved, then marker birth is no longer
    the live obstruction.
  Where it fails:
  - Exact raw birth formulas do not themselves transport the marker.
  - The current raw `u` value is not constant along the corridor, so the
    exceptional bit cannot be re-read statically later from current `u`.
  - The open issue becomes carrier persistence / transport, not birth.

Attempt B:
  Idea:
  If the raw birth formulas were to fail under a stricter admissibility notion,
  move to the smallest richer source-edge or source->entry coupled mechanism.
  What works:
  - `038` already suggests predecessor-facing information is informative.
  - A source->entry birth event is the natural place to initialize a carrier.
  What fails:
  - This branch should now be secondary. It is only needed if the exact raw
    birth formulas are not admissible, not stable, or not sufficient for the
    intended local mechanism class.

Candidate lemmas:
- [C-pre039] For the best seed and checked `m = 5,7,9,11`, the source slice
  `R1` is exactly the raw current-coordinate class
  `layer=1, q=m-1, w=0, u!=0`.
- [C-pre039] The exceptional source slice is exactly `u=3` inside that class.
- [C-pre039] The alt-`2` entry slice is exactly
  `layer=2, q=m-1, w=1, u!=0`, with exceptional entry `u=3`.
- [H] Therefore the `038` no-go does not show that birth itself is hidden; it
  only shows that birth is not readable from the simple `phase_align/wu2`
  neighborhood alphabet.
- [H] If the raw birth formulas are accepted, then the live obstruction shifts
  from source-marker birth to family-tagged carrier transport along the visible
  raw odometer.
- [F] “The family bit is still the hard part of the next branch.”
- [F] “The live obstruction is definitely source-marker birth even after exact
  raw-coordinate checks.”
- [O] Full D5 Hamilton decomposition remains open.

Needed computations/search:
1. **Exact raw birth-formula extraction**
   Save and verify the exact source and entry formulas on `m = 5,7,9,11`:
   - source `R1`;
   - exceptional source;
   - entry `alt-2(R1)`;
   - exceptional entry.

2. **Admissibility / minimality diagnosis**
   Decide whether those formulas are allowed local observables for the active
   mechanism class.
   - If yes, treat birth as solved.
   - If no, state the exact admissibility restriction that blocks them.

3. **Birth-state initialization**
   Initialize the smallest carrier states at birth:
   - `off`,
   - `active_reg`,
   - `active_exc`,
   using the exact source predicate plus the exceptional birth test `u=3`.

4. **Carrier persistence / transport search**
   Search only for the smallest mechanism that transports `active_reg` and
   `active_exc` through the `BBB` corridor while using the already-visible raw
   odometer `(q,w,layer)` / `chi` to fire at:
   - regular target `(m-1,m-2,1)` with exit `[2]`,
   - exceptional target `(m-2,m-1,1)` with exit `[1]`.

5. **Fallback only if needed**
   If exact raw birth formulas are not admissible or do not survive the carrier
   design, then move to the smallest richer source-edge / source->entry coupled
   mechanism, rather than reopening generic search.

Next branching options:
1. Main branch:
   confirm and save the exact raw source/entry birth formulas, then search only
   for the smallest family-tagged carrier persistence mechanism.
2. Secondary branch:
   prove a no-go for any mechanism that tries to persist the carrier using only
   current raw coordinates and no active state.
3. Fallback branch:
   source-edge or source->entry coupled birth if the exact raw birth formulas
   are not admissible in the intended mechanism class.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `035`, `036`, `037`, `038`
  [C-pre039] exact raw source / entry formulas checked during spec prep on
            `m = 5,7,9,11`, not yet saved as a standalone artifact
  [H] birth may already be solved; transport may now be the live obstruction
  [F] family-bit-hardness / birth-hardness as the unique next bottleneck
  [O] full D5 decomposition open

## Work template

Work Template:
    Task ID:
    D5-RAW-BIRTH-MARKER-TRANSPORT-039

    Question:
    For the unresolved best-seed channel
        R1 -> H_L1
    in the seed pair
        left = [2,2,1], right = [1,4,4],
    is the source-local marker already exact on raw current coordinates, and if
    so does the next live problem reduce to transporting a family-tagged active
    carrier through the already-visible raw odometer corridor?

    Purpose:
    `037` made the corridor phase visible on raw `(q,w,layer)`.
    `038` proved only that the source marker is not isolatable in the simple
    birth-local `phase_align/wu2` neighborhood alphabet up to size `5`.
    The next honest step is to test the smallest richer observable first:
    exact raw current coordinates at birth. If the source and entry slices are
    already exact there, then the branch should pivot immediately from “birth”
    to “transport”.

    Inputs / Search space:
    - reduced target:
      - `025` omit-base + edge-tied point cocycle defect
    - best-seed unresolved channel:
      - `032`, `033`
    - raw odometer / targets:
      - `037`
    - simple birth-local no-go and cheap exceptional bit:
      - `038`
    - best seed:
      - left = `[2,2,1]`
      - right = `[1,4,4]`
    - checked moduli:
      - `m in {5,7,9,11}`
    - candidate exact raw birth coordinates:
      - source current `(layer,q,w,u)`
      - entry current `(layer,q,w,u)` after alt-`2`
    - carrier states to test only after birth extraction:
      - `off`
      - `active_reg`
      - `active_exc`

    Allowed methods:
    - exact extraction of source and entry slices from the existing best-seed
      defect/corridor pipeline
    - exact matching against raw current-coordinate formulas
    - saving explicit source/entry formula tables
    - representative and, if cheap, exhaustive checked-modulus transport
      diagnostics for the family bit
    - tiny carrier persistence / trigger search only after birth formulas are
      explicit
    - no reopened broad one-bit scans
    - no reopened generic bounded-state transducer search on the old alphabet
    - no broad seed widening

    Success criteria:
    1. Produce an explicit raw current-coordinate formula for the source slice
       `R1`, or prove that no such stable formula exists on the checked moduli.
    2. Produce the explicit exceptional-source formula inside that source class.
    3. Produce an explicit raw current-coordinate formula for the entry slice
       `alt-2(R1)`, or prove that no such stable formula exists.
    4. State clearly whether source-marker birth is already solved once exact
       raw current coordinates are allowed.
    5. If birth is solved, initialize the smallest plausible carrier states
       `off / active_reg / active_exc` at birth.
    6. Determine whether the next live obstruction is:
       - carrier persistence / transport,
       - admissibility of exact raw birth observables,
       - or a genuinely richer source-edge / temporal mechanism.

    Failure criteria:
    - the proposed exact raw birth formulas are not stable across `m=5,7,9,11`,
    - or they collide outside the intended source / entry targets,
    - or the intended local mechanism class forbids using them,
    - or carrier transport still depends irreducibly on a missing state that is
      not captured by `off / active_reg / active_exc`.
    - If failure occurs, state the exact missing reduced coordinate or coupling
      requirement.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - `source_birth_formula_rows.json`
    - `entry_birth_formula_rows.json`
    - `birth_formula_summary.json`
    - `family_bit_transport_drift_summary.json`
    - `carrier_initialization_spec.json`
    - `transport_nogo_or_candidate_summary.json`
    - proof-supporting computations

    Return format:
    - explicit source birth predicate
    - explicit exceptional-source birth predicate
    - explicit entry predicate
    - verdict on whether birth is already solved
    - smallest plausible carrier state set
    - strongest obstruction if transport still needs more than that
    - explicit recommendation for the next local branch

    Reproducibility requirements:
    - fixed best seed pair `[2,2,1] / [1,4,4]`
    - fixed moduli `5,7,9,11`
    - deterministic extraction order
    - saved JSON summaries for source/entry birth formulas and any transport
      diagnostics
    - exact scripts for formula verification and carrier checks
    - explicit separation of:
      - `037/038` inherited facts,
      - prep-checked `039` birth-formula facts,
      - new `039` transport findings
