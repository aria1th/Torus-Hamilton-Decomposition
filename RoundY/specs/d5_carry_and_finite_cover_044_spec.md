# D5-CARRY-AND-FINITE-COVER-044

## Question

After `043`, can the best-seed active branch be formulated and proved as

- grouped base `B = (s,u,v,layer,family)`,
- carry sheet `c = 1_{q=m-1}`,
- residual binary noncarry sheet `d`,

with the next concrete realization problem restricted to the carry sheet first?

Equivalently:

1. can we extract a theorem-level finite-cover normal form
   `B <- B+c <- B+c+d`
   on the checked active union; and
2. can we isolate the smallest admissible realization target as the carry bit
   rather than full raw `q` or the whole residual sheet?

## Purpose

`037-040` solved the reduced raw control logic.
`041` proved that first grouped-state-descending admissible families are too
small.
`042` showed that trigger logic needs only the carry-slice bit over the grouped
base, while the structural active lift over the grouped base has fiber size at
most `3`.
`043` sharpened this further:

- over `B+c`, the minimal deterministic cover is always `2`-sheet on the checked moduli,
- its support lies entirely on the regular noncarry branch,
- the residual sheet is not the obvious current bit `1_{q=m-2}` on `m=7,9,11`,
- short future-carry windows fail,
- but a theorem-friendly nonlocal coordinatization exists via time to next carry.

So the next honest branch is no longer “find a controller” or “expose raw q”.
It is:

- theorem branch: prove the finite-cover normal form,
- local branch: realize the carry sheet first.

## Fixed inputs / scope

- reduced target from `025`
- best seed pair from `032/033`
- raw odometer / active corridor extraction from `037`
- raw birth and tagged carrier logic from `039`
- raw coordinate realization summary from `040`
- grouped-state admissibility obstruction from `041`
- carry-slice and `<=3`-sheet cover from `042`
- refined `B <- B+c <- B+c+d` structure from `043`
- checked moduli `m in {5,7,9,11}`

## Main theorem target

Extract and verify a finite-cover normal form on the checked active union:

```text
Base:
    B = (s,u,v,layer,family)

First lift:
    c = 1_{q=m-1}

Second lift:
    d in {0,1}
```

with the following properties:

1. exceptional fire is a function of `B`;
2. regular fire is a function of `B+c`;
3. the active transition law is deterministic on `B+c+d`;
4. the support of `d` lies entirely on the regular noncarry branch;
5. `d` is not required on exceptional or carry states;
6. the checked branch is therefore a grouped base plus carry sheet plus residual binary noncarry sheet.

## Concrete local target

Do **not** search first for realization of the full residual sheet.
The smallest verified positive local target is:

```text
realize the carry bit c = 1_{q=m-1} admissibly.
```

Reason:

- it already closes the regular trigger logic,
- it is strictly smaller than the full structural lift,
- `043` shows the residual binary sheet is structurally exact but not a tiny current observable.

## Allowed methods

### Theorem branch

- exact active-union extraction on checked moduli;
- partition refinement / minimal deterministic cover extraction;
- search for a clean nonlocal coordinatization of the residual sheet;
- explicit comparison between:
  - raw `q`,
  - carry bit `c`,
  - residual sheet `d`,
  - time to next carry `tau`;
- identification of reset / merge behavior of `d` at carry states;
- formulation in odometer / skew-odometer language.

### Local branch

- admissible realization search only for the carry bit `c`;
- grouped + edge-tied + cocycle-style observables if they do not collapse to current `B`;
- tiny lifted admissible candidates that can encode carry status;
- no broad search for full raw `q`;
- no broad search for realization of `d` before carry is understood.

## Specific subquestions

### A. Structural theorem extraction

1. Is there a canonical choice of residual binary coordinate `d` over `B+c`?
2. Can `d` be described intrinsically by future return structure, e.g. a quotient of time to next carry?
3. Does `d` reset or become irrelevant immediately after each carry?
4. Can the active branch be described as a skew-odometer base with a binary noncarry cover?
5. Is the support of `d` exactly the regular noncarry region for all checked `m`?

### B. Carry realization

1. Can `c = 1_{q=m-1}` be realized in the admissible reduced class from `025`?
2. If not directly, can it be realized on a minimal lifted admissible state that is still much smaller than raw `q`?
3. Which admissible candidate separates carry from noncarry without collapsing to current grouped state?
4. Is there a no-go theorem for the first few admissible families beyond `041`?

## Success criteria

### Structural success

1. Produce a checked finite-cover theorem statement of the form `B <- B+c <- B+c+d`.
2. Verify that the minimal deterministic cover over `B+c` is binary on every checked modulus.
3. Verify that the support of `d` is regular noncarry only.
4. Give one theorem-friendly coordinatization of `d`, even if nonlocal.
5. State cleanly how D5 now fits the odometer narrative:
   - grouped / skew-odometer base,
   - carry sheet,
   - residual binary noncarry cover.

### Local success

1. Produce an admissible realization candidate for the carry bit `c`.
2. Verify it on `m = 5,7,9,11`.
3. Explain how this suffices for exact trigger logic even before `d` is realized.

## Failure criteria

Report failure separately for the two branches.

### Structural failure

- no clean intrinsic coordinatization of `d` is found beyond raw partition labels,
- or the claimed binary cover over `B+c` is unstable beyond the checked moduli.

### Local failure

- no admissible realization of `c` exists in the next intended observable family,
- or every candidate collapses to current grouped state and repeats the `041` obstruction.

If failure occurs, state whether the obstruction is:

- lack of an admissible carry observable,
- lack of a clean intrinsic sheet coordinate,
- or a deeper gap between raw control and admissible grouped realization.

## Artifacts to save

- code
- raw logs
- summary report
- finite-cover theorem note
- binary residual-sheet tables
- carry-realization candidate tables
- carry no-go tables if relevant
- JSON summaries for:
  - cover over `B`
  - cover over `B+c`
  - residual-sheet support
  - candidate carry observables
  - time-to-next-carry coordinatization

## Return format

- exact finite-cover formulation `B <- B+c <- B+c+d`
- support statement for `d`
- strongest intrinsic coordinatization found for `d`
- exact status of admissible carry realization
- recommendation for whether to continue with:
  - carry realization first,
  - structural theorem extraction first,
  - or a coupled but still carry-prioritized branch

## Strong recommendation

Prioritize in this order:

1. admissible realization of the carry sheet `c`;
2. clean theorem formulation of the residual binary sheet `d`;
3. only then attempt admissible realization of `d` if the global proof still needs it.

This keeps the concrete local branch small while preserving the cleaner
D3/D4/D5 odometer narrative.
