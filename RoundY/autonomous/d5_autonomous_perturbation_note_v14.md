Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after `038`, where the small
birth-local bit family no longer seems to be the right place to search for the
marker.

Current target:
Decide whether birth is already explicit on raw current coordinates, so that
the next reduced obstruction is tagged carrier transport rather than birth
discovery.

Known assumptions:
- `033` reduces the best-seed defect to the unresolved channel `R1 -> H_L1`.
- `036` and `037` extract the lifted and then raw visible corridor odometer.
- `038` shows the simple birth-local `phase_align/wu2` neighborhood alphabet
  does not isolate the source or entry marker up to size `5`, but does isolate
  the exceptional source slice cheaply.

Attempt A:
  Idea:
  Test the smallest richer observable before any wider carrier search: exact
  raw current coordinates at birth.
  What works:
  `039` verifies exactly on `m = 5,7,9,11` that:
  - source `R1` is exactly `layer=1, q=m-1, w=0, u!=0`
  - exceptional source is exactly `u=3` inside that source class
  - entry `alt-2(R1)` is exactly `layer=2, q=m-1, w=1, u!=0`
  - exceptional entry is exactly `u=3` inside that entry class
  So birth is already explicit at the reduced raw-coordinate level.
  Where it fails:
  This still does not realize a local mechanism. It only shows the reduced
  birth target is no longer vague.

Attempt B:
  Idea:
  Check whether the family bit can be re-read later from current raw
  coordinates, which would make transport unnecessary.
  What works:
  It fails in the right way.
  On representative regular and exceptional corridor traces, current raw `u`
  visits all residues mod `m` for every checked `m = 5,7,9,11`.
  So the family bit must still be initialized at birth and transported.
  Where it fails:
  This does not yet build the transport mechanism itself.

Candidate lemmas:
- [C] The best-seed raw birth source class is exactly
  `layer=1, q=m-1, w=0, u!=0`.
- [C] The exceptional source tag is exactly `u=3` inside that class.
- [C] The raw birth entry class is exactly `layer=2, q=m-1, w=1, u!=0`.
- [C] The exceptional entry tag is exactly `u=3` inside that class.
- [C] Current raw `u` drifts through all residues on representative regular and
  exceptional corridor traces.
- [H] At the reduced-model level, the next live obstruction is tagged carrier
  transport, not birth.
- [O] Admissibility of exact raw birth observables for the intended local
  mechanism class is still open.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- keep the raw birth formulas fixed as the reduced birth target
- search only for the smallest mechanism that transports
  `active_reg / active_exc` through the visible raw odometer corridor
- if needed, separate the reduced transport problem from the admissibility
  question for raw birth observables

Next branching options:
1. Main branch:
   tagged carrier transport on top of exact raw birth.
2. Secondary branch:
   admissibility / no-go theorem for exact raw birth observables.
3. Fallback branch:
   richer source-edge / temporal birth mechanism only if exact raw birth is not
   admissible in the intended class.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `035`, `036`, `037`, `038`, `039`
  [H] birth is already solved at the reduced raw-coordinate level; transport is
      now the live reduced obstruction
  [F] “birth itself is still the live reduced obstruction”
  [O] local admissibility of exact raw birth observables
  [O] full D5 decomposition
