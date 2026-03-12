Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the endpoint-seed obstruction
has been reduced to one explicit unresolved channel.

Current target:
Decide whether the unresolved best-seed channel
- `R1 -> H_L1`

is already an orbit-phase problem on a reduced model, or whether the project
still needs a genuinely larger generic splice alphabet.

Known assumptions:
- `025` remains the correct reduced grouped target.
- `028`, `029`, `031`, and `032` isolate the best seed and kill the smallest
  static repair families.
- `033` proves the best-seed defect graph is bounded, with only one unresolved
  channel, and kills the natural `2`-state / `3`-state transducer branch on the
  current local alphabet.

Attempt A:
  Idea:
  Project the unresolved `BBB` corridor into reduced coordinates and test
  whether it already carries the same kind of large/small orbit split seen in
  the earlier reduced grouped-base analysis.
  What works:
  `034` gives an exact positive model.
  After the initial `R1` alternate-`2` entry, the corridor projects to
  `(s, layer)` and follows the exact source-parameterized rule
  `F_rho`, where `rho = u_source + 1`.
  The projected phase space splits explicitly into:
  - one small orbit of size `m`
  - one large orbit of size `m(m-1)`
  with the small orbit
  `M_rho = {(rho, layer): layer != 2} union {(rho+1,2)}`.
  So the unresolved channel already has the same qualitative orbit split that
  `023` exposed in the reduced grouped-base setting.
  Where it fails:
  This is a reduced phase model, not yet a local realization. It does not by
  itself tell us how to expose the phase to the local rule.

Attempt B:
  Idea:
  Use the phase model to reinterpret the old short/long delay split.
  What works:
  `034` shows the short/long split is exactly one full large-orbit lap.
  Verified on `m=5,7,9,11`:
  - phase period:
    `m(m-1)`
  - short family:
    `Delta_short = (m-3)m^2 - 1`
  - long family:
    `Delta_long = Delta_short + m(m-1)`
  - shared phase residue:
    `Delta mod m(m-1) = m^2 - 3m - 1`
  The source slice `u_source = 3` is the unique exceptional family; all other
  source slices use the short law.
  So the delay gap from `033` is not accidental. It is literally one extra lap
  on the extracted large orbit.
  Where it fails:
  The model still leaves open how a local mechanism should read or carry this
  phase. That is now the real next problem.

Candidate lemmas:
- [C] The unresolved best-seed channel projects to an exact reduced phase model
  on `(s, layer)`.
- [C] For each source slice, that phase model has one small orbit of size `m`
  and one large orbit of size `m(m-1)`.
- [C] The short/long delay families differ by exactly one full large-orbit lap.
- [C] The exceptional source slice is exactly `u_source = 3`.
- [H] The missing state is orbit phase, not a tiny generic transducer state.
- [H] The next live local branch should expose or carry phase, not just widen a
  generic transducer alphabet.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop bounded-state transducer synthesis on the current local alphabet
- search for the smallest local observable or carrier that exposes the
  extracted corridor phase
- or search for the smallest coupled mechanism that changes the corridor phase
  map itself

Next branching options:
1. Main branch:
   a phase-exposing local mechanism keyed to the reduced `(s, layer)` corridor
   phase.
2. Secondary branch:
   a coupled perturbation that changes the corridor phase map rather than
   reading it.
3. Only then:
   revisit local synthesis on the enriched phase-aware alphabet.

Claim status labels:
  [P] `019`, `023`, `025`
  [C] `028`, `029`, `031`, `032`, `033`, `034`
  [H] the live obstruction is orbit phase, not tiny generic transducer memory
  [O] full D5 decomposition
