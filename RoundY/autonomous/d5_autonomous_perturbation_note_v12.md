Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the `036` clarification that
the long corridor lifts to `(q,a,layer)`.

Current target:
Decide whether that lifted corridor state is still hidden, or whether it is
already visible on raw current coordinates and therefore changes the next local
problem from “phase exposure” to “localized carrier”.

Known assumptions:
- `033` reduces the best-seed obstruction to the unresolved `R1 -> H_L1`
  corridor.
- `035` prunes raw static phase gates on the projected `(s,layer)` picture.
- `036` shows `(s,layer)` is only a first-pass lap and lifts the traced long
  corridor exactly to `(q,a,layer)` up to first exit.

Attempt A:
  Idea:
  Check whether the lifted coordinate `a` is already readable from raw current
  coordinates along the traced corridor.
  What works:
  `037` verifies exactly, on every traced state up to first exit and for every
  checked `m = 5,7,9,11`, that
  - `a = q + w - 1_{layer=1} mod m`.
  So the lifted corridor state is already visible on the raw current triple
  `(q,w,layer)`.
  The raw corridor rule also closes exactly:
  - `(q,w,0) -> (q+1,w,1)`
  - `(q,w,1) -> (q,w,2)`
  - `(q,w,2) -> (q,w+1,3)` if `q = m-1`, else `(q,w,3)`
  - otherwise `(q,w,layer) -> (q,w,layer+1 mod m)`
  Where it fails:
  This does not localize the intervention. It only shows phase is already
  visible once one is on the intended corridor.

Attempt B:
  Idea:
  Rewrite the corridor as a raw odometer and extract the minimal reduced target
  for the next local branch.
  What works:
  The raw odometer is exact.
  With the coordinate
  - `chi = m*(qHat + m*(wHat-1) - (m-1)) + (layer-2 mod m) mod m^3`,
  where `qHat = q - 1_{layer=1}` and
  `wHat = w - 1_{layer!=2}1_{qHat=m-1}`,
  the corridor has:
  - entry `(m-1,1,2)` at `chi = 0`
  - every traced step equal to `chi -> chi + 1`
  The first exits are two universal raw targets:
  - regular: `(m-1,m-2,1)` via `[2]`
  - exceptional: `(m-2,m-1,1)` via `[1]`
  and their phases differ by exactly `m(m-1)`.
  So the reduced missing state is no longer hidden phase. It is a localized
  corridor marker plus one family bit.
  Where it fails:
  This is still a reduced target, not yet a local realization.

Candidate lemmas:
- [C] The `036` lifted state is already visible on raw `(q,w,layer)`.
- [C] The traced corridor follows an exact raw-coordinate odometer.
- [C] The first exits are two universal raw odometer targets.
- [C] The target gap is exactly `m(m-1)`.
- [H] The next live branch is a localized carrier search, not a phase-exposure
  search.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop framing the next branch as “find phase”
- search for a corridor-local carrier born at the `R1` alt-`2` entry
- transport that carrier through `BBB`
- use the already-visible raw odometer phase to trigger at the regular or
  exceptional target according to a tiny family bit

Next branching options:
1. Main branch:
   a one-bit corridor-local marker plus one family bit.
2. Secondary branch:
   a theorem/no-go branch showing why visible raw phase alone is insufficient
   without corridor localization.
3. Only then:
   reopen wider local synthesis.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `035`, `036`, `037`
  [H] the next live target is localized carrier transport on top of visible raw
      phase
  [F] treating phase exposure itself as the main missing ingredient
  [O] full D5 decomposition
