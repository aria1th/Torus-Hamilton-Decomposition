# D5-COORDINATE-EXPOSURE-ADMISSIBILITY-041

## Question

For the unresolved best-seed channel

- `R1 -> H_L1`

in the fixed best seed pair

- `left = [2,2,1]`
- `right = [1,4,4]`

can the already-solved raw current-coordinate control logic from `037`/`039`/`040`
be exposed in the **admissible reduced class** implied by `025`
(omit-base plus edge-tied point cocycle defect),
or else can one prove that the first admissible coordinate-exposure classes still
cannot realize the needed observables?

## Purpose

`040` moves the frontier again.

The live obstruction is no longer:

- hidden corridor phase,
- family-bit transport,
- tagged-carrier design,
- or richer recombinations of the simple `038` bit row.

Those are already resolved at the reduced raw-control level.

What remains is narrower:

- the reduced control logic is exact on **raw current coordinates**, but
- those coordinates are not yet known to be available in the intended admissible
  cyclic-equivariant / local / cocyclic class.

So the next honest branch is:

**coordinate exposure / admissibility**, not controller synthesis.

## Fixed facts to treat as established

### 1. Reduced target from `025`

The correct reduced target remains:

- omit-base
- plus edge-tied point cocycle defect.

### 2. Best-seed obstruction from `033`

The best seed pair

- `left = [2,2,1]`
- `right = [1,4,4]`

reduces the open branch to the single unresolved channel

- `R1 -> H_L1`.

### 3. Corridor phase from `036` and `037`

The long `BBB` corridor is already explicit, and on the active union its phase is
visible on raw current coordinates. In particular, `037` shows:

- raw current `(q,w,layer)` supports the odometer description,
- regular and exceptional targets are explicit,
- the problem is not hidden phase exposure anymore.

### 4. Birth / tag transport from `039`

`039` fixes the reduced raw 3-state carrier model:

- `off`
- `active_reg`
- `active_exc`

with exact birth formulas on raw current coordinates:

- source:
  - `layer = 1, q = m-1, w = 0, u != 0`
- exceptional source:
  - `layer = 1, q = m-1, w = 0, u = 3`
- entry:
  - `layer = 2, q = m-1, w = 1, u != 0`
- exceptional entry:
  - `layer = 2, q = m-1, w = 1, u = 3`

and target rules:

- `active_reg` fires at `(q,w,layer) = (m-1, m-2, 1)` by direction `2`
- `active_exc` fires at `(q,w,layer) = (m-2, m-1, 1)` by direction `1`

while raw current `u` drifts later, so the family tag must still be born and
transported.

### 5. Simple local observable no-go from `038` and `040`

The whole simple `038` observable family is now exhausted as the next reduced
realization class.

Even after using:

- full current 24-bit simple row,
- source-edge alt-2 paired rows,
- lag-1 full-row temporal pairs,
- lag-2 full-row temporal pairs,

`040` still finds:

- no source isolator,
- no entry isolator,
- no stable exceptional trigger,
- no stable large-modulus regular trigger in the lag families.

So the next branch must **not** be another lift of the same simple row.

### 6. Exact raw realization on current coordinates from `040`

On checked moduli `m = 5,7,9,11`, `040` shows:

- birth is exact on raw current coordinates,
- current `(q,w,u,layer)` separates active source families on the active union,
- active-conditioned current `(q,w,layer)` fires with zero prehits.

So the reduced control problem is already solved on raw current coordinates.

## Main 041 target

Determine whether the needed raw current-coordinate observables can be exposed
inside the admissible reduced class, or whether there is an exact obstruction.

This should be treated as a **coordinate-coding / admissibility** problem.

Not a transducer problem.
Not a hidden-phase problem.
Not a tagged-carrier design problem.

## Minimal quantities that actually need admissible exposure

Treat the following decomposition as the first object to compress.

### Already cheap / fixed

- `layer` is already in the simple row.
- the source exceptional split already has cheap source-local witnesses in `038`.
- the active carrier states themselves are fixed at the reduced level.

### Still needing admissible realization

The next branch should ask whether one can expose just enough coordinate data to
implement the already-known logic.

At birth, enough to decide:

- `q = m-1`
- `w = 0`
- `u = 0` versus `u = 3` versus other nonzero residues

At fire time, under active conditioning, enough to decide:

- regular target: `(q,w,layer) = (m-1,m-2,1)`
- exceptional target: `(q,w,layer) = (m-2,m-1,1)`

The first admissibility attempt should therefore **not** insist on exposing the
entire coordinate tuple globally if a smaller quotient already suffices.

## Primary candidate mechanism class for 041

The most natural next family is not another bit-neighborhood alphabet.
It is:

- **admissible coordinate surrogates** built from the `025` framework,
  especially edge-tied point cocycles or affine coordinate cocycles anchored by
  the omit-base defect.

The first search should ask whether the omitted base / grouped-orbit structure
already provides a canonical gauge in which one can recover one or more of:

- `q mod m`
- `w mod m`
- `u mod m`
- or just the smaller predicate-level quotients actually needed for birth and fire.

## Allowed methods

- exact extraction of coordinate predicates on checked moduli `m in {5,7,9,11}`
- search for admissible edge-tied point cocycles or affine cocycle models whose
  values agree with the needed coordinate predicates on:
  - source class,
  - active union,
  - first-exit targets
- search for low-rank cocycle quotients rather than full coordinate exposure
- exact grouped-orbit / omit-base anchoring analysis
- proof-oriented no-go tests for first admissible coordinate-exposure classes
- machine-readable validation across the fixed checked moduli

## Explicitly discouraged for 041

- no more projection search inside the `038` simple row family
- no generic bounded-state transducer synthesis
- no reopening of hidden phase extraction
- no reopening of family-bit-at-birth search as if still unresolved
- no broad carrier search with unconstrained logic

## Success criteria

A 041 branch succeeds if it does at least one of the following.

### Success mode A: positive admissible exposure

1. Identify an admissible observable family in the `025` reduced class that
   realizes the needed raw control predicates, either exactly or via an
   equivalent quotient.
2. Show how birth is decided in that family.
3. Show how the regular / exceptional active trigger is decided in that family.
4. Validate on `m = 5,7,9` and control `m = 11`.
5. Produce the smallest surviving exposed quantity, not merely a larger
   coordinate package.

### Success mode B: exact first obstruction

1. Show that the first admissible coordinate-exposure family still cannot
   realize the needed predicates.
2. State the exact missing ingredient, for example:
   - one more cocycle coordinate,
   - one anchored gauge choice,
   - one source-edge memory bit,
   - or a genuinely nonlocal coordinate quantity.
3. Record a minimal collision / obstruction certificate.

## Failure criteria

Failure occurs if the branch does not determine whether the already-known raw
carrier logic can be expressed in the intended admissible reduced class.

If failure occurs, report the exact unresolved gap beyond raw coordinates:

- not “marker,”
- not “phase,”
- but the precise missing admissibility ingredient.

## Candidate lemmas

- [C] `037` + `039` + `040` already solve the reduced control logic on raw
  current coordinates.
- [C] Families built only from the simple `038` row are exhausted as the next
  realization alphabet.
- [H] The next honest branch is admissible exposure of coordinate-level
  observables, or a no-go theorem for the first such admissible families.
- [H] The minimal admissible exposure may be strictly smaller than full
  `(q,w,u,layer)`.
- [F] Another larger search in the same simple row family is the right next move.
- [O] Full D5 Hamilton decomposition remains open.

## Needed computations / search

1. Save the exact reduced predicate package implied by `040`:
   - birth predicates,
   - family split,
   - active trigger predicates.
2. Enumerate the smallest admissible coordinate-surrogate families suggested by
   the `025` framework.
3. Test whether any such family realizes the needed predicates on
   `m = 5,7,9,11`.
4. If a family survives, save:
   - explicit formulas,
   - validation tables,
   - collision summary.
5. If no family survives, save:
   - exact obstruction tables,
   - minimal collision certificates,
   - strongest next missing ingredient.

## Next branching options after 041

1. **Main branch:**
   admissible coordinate exposure via edge-tied / affine cocycle models.
2. **Secondary branch:**
   first no-go theorem for low-rank admissible coordinate-surrogate families.
3. **Only then:**
   reopen broader realization only if the admissible coordinate branch fails.

## Artifacts to save

- code
- raw logs
- summary report
- admissible_observable_catalog_041.json
- reduced_coordinate_predicates_041.json
- coordinate_exposure_validation_041.json
- coordinate_admissibility_obstruction_041.json
- proof-supporting computations

## Return format

- explicit statement of the smallest raw predicates that must be realized
- explicit admissible family tested
- positive realization formula or exact obstruction
- whether full `(q,w,u,layer)` exposure was needed or a smaller quotient sufficed
- strongest recommendation for the next branch

## Reproducibility requirements

- fixed best seed pair `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- deterministic extraction order
- saved JSON outputs for all surviving or obstructed admissible families
- explicit separation of:
  - old raw-control facts from `037/039/040`
  - new `041` admissibility / exposure facts
