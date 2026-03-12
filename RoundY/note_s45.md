The summary is enough; I did not reopen the tar.

The level I want next is very specific:

**one seed pair, one bit of memory, one explicit Latin-repair gate.**

Not a broader word catalog, not another selector sweep, and not a larger static promotion.
`028–031` say the reduced target is still right, but the obstruction has moved entirely into **Latin repair of endpoint-separated words**.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Do **not** continue with static endpoint-word search.
The next honest branch is:

**collision-driven Latin repair around one `030` seed pair.**

More concretely, the right level is:

* fix one promising endpoint-separated seed pair from `030`,
* extract its exact Latin collision certificate from the failed static promotions `029/031`,
* add the smallest dynamic state that can distinguish the colliding uses,
* and test whether one-bit memory or one localized repair gate is enough.

Known assumptions:

* I am taking your summary as sufficient for this turn; I did not reopen the tarballs.
* `025` identified the correct reduced target:

  * omit-base plus edge-tied point cocycle defect,
  * with grouped base orbit size `m^2`,
  * and full grouped orbit size `m^3`.
* `028` confirms the key missing local state is endpoint orientation on the active edge.
* `029` blocks the smallest static two-layer realization:

  * `2500` exact candidates,
  * only `4` Latin/clean/strict survivors,
  * all `4` are just the baseline word `(4,4;2,2)` with the four cocycle-defect choices,
  * `0` nonbaseline Latin survivors,
  * `0` endpoint-asymmetric Latin survivors,
  * `0` target hits.
* `030` shows the richer path-level branch is not empty:

  * `6` desired left 3-step words,
  * `6` desired right 3-step words,
  * `18` opposite-sign pairs,
  * `14` already distinct at both layer `2` and layer `3` across `m=5,7,9`.
* `031` kills the smallest static three-layer promotion:

  * `72` exact candidates per modulus,
  * `0` Latin survivors on `m=5,7,9`.
* So the new obstruction is sharp:
  **endpoint separation is necessary, but fixed static endpoint words are still insufficient because Latin fails before grouped-orbit considerations even begin.**

Attempt A:
Idea:
Read `028–031` as a structural no-go for static endpoint-word realization of the `025` reduced target.

What works:

* This is stronger than “we tried a few tunings.”
* `028` says the reduced target really is edge-oriented.
* `029` says the simplest static two-layer realization has no nonbaseline Latin point.
* `030` says the path-level seed words do exist and are genuinely asymmetric.
* `031` says even promoting those seed words statically to three layers still gives zero Latin survivors.
* Therefore the failure is not:

  * wrong reduced target,
  * lack of endpoint-separated path words,
  * or insufficient static palette size.
* The failure is:
  **Latin blocks any purely static endpoint-word promotion.**

Where it fails:

* It does not yet tell us the smallest dynamic repair that works.
* It only prunes the whole static branch.

Attempt B:
Idea:
Replace “find better endpoint words” by “repair the exact Latin collision of one good endpoint seed pair.”

What works:

* This is the smallest possible next step.
* It uses the positive part of `030` instead of discarding it.
* The right workflow is:

  1. pick one of the `14` distinct-at-both-layers seed pairs,
  2. compute the exact outgoing/incoming Latin collision support from the failed static promotion,
  3. ask whether those collisions are resolved by one additional bit of path memory or one localized repair gate.
* This is exactly the level where the branch is now informative.
* It is also the right analogue of the earlier d3/d4 lesson: once the reduced target is known, the next job is not bigger search but the minimal repair mechanism.

Where it fails:

* We do not yet know whether the smallest repair is:

  * predecessor/current one-bit memory,
  * current/successor one-bit memory,
  * or a one-class exceptional repair word.
* That is the next computation.

Candidate lemmas:

* [C] The `025` reduced target remains the right one.
* [C] `028` shows endpoint orientation is necessary.
* [C] `029` rules out the smallest static two-layer endpoint-word realization.
* [C] `030` shows there are genuine endpoint-separated path-level seed pairs.
* [C] `031` rules out the smallest static three-layer promotion of those seed pairs.
* [H] Therefore the next missing ingredient is not another static word choice, but an explicit Latin-repair mechanism.
* [H] The next smallest live branch is one seed pair + one-bit memory / one repair gate.
* [F] Another broader static endpoint-word catalog search is the right next move.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Do **not** widen the seed catalog further first.

* The next exact work should be:

  1. **Collision certificate extraction**
     For each of the `14` promising `030` seed pairs, compute:

     * outgoing Latin collisions,
     * incoming Latin collisions,
     * the exact colliding local states,
     * which layer(s) the collision is witnessed on,
     * whether the collision disappears after conditioning on:

       * predecessor/current,
       * current/successor,
       * omitted-row / omitted-edge status.

  2. **Seed ranking**
     Rank the seed pairs by:

     * smallest collision support,
     * smallest number of colliding local classes,
     * clearest one-bit separator candidate.

  3. **Micro-family repair search**
     For the cleanest one or two seed pairs only, search the smallest dynamic repair family:

     * one-bit memory carrier, or
     * one localized repair gate,
       using the `030` word palette and preserving the `025` reduced target as closely as possible.

* The success question is now:
  **is one extra bit enough to repair Latin for at least one `030` seed pair?**

Next branching options:

1. Main branch:
   collision certificates + one-bit repair around one `030` seed pair.
2. Secondary branch:
   if one-bit repair fails for all promising seeds, move to the smallest two-state transducer.
3. Side theorem branch:
   formalize the static endpoint-word no-go from `029/031`.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-ENDPOINT-LATIN-REPAIR-032

```
Question:
Can one of the `14` endpoint-separated `030` seed pairs be promoted to a clean/strict realization of the `025` reduced target by adding the **smallest possible dynamic repair**:
either one bit of memory or one localized repair gate that resolves the exact Latin collisions seen in `029/031`?

Purpose:
`028–031` have already done the pruning:
- the reduced target is still right,
- endpoint orientation is necessary,
- but static endpoint words fail before grouped-orbit considerations.
So the next honest task is not a larger static search. It is to identify the exact Latin collision and test whether one extra bit repairs it.

Inputs / Search space:
- Reduced target:
  - `025` omit-base + edge-tied point cocycle defect
- Local branch diagnostics:
  - `028` endpoint orientation result
  - `029` static two-layer no-go
  - `030` endpoint word catalog
  - `031` static three-layer no-go
- Seed pool:
  - the `14` opposite-sign seed pairs from `030` that are distinct at both layer `2` and layer `3` on `m=5,7,9`
- Moduli:
  - primary `m in {5,7,9}`
  - first control `m=11`

Allowed methods:
- exact extraction of outgoing/incoming Latin collision certificates for each seed pair
- classification of collisions by local signature
- tests of whether collisions separate under:
  - predecessor/current one-bit context
  - current/successor one-bit context
  - omitted-row / omitted-edge one-bit context
- micro-family search only on the best seed pair(s):
  - default left/right endpoint words from `030`
  - one extra bit of memory or one repair gate
  - optional replacement by one alternate `030` word on one collision class
- direct all-color Latin testing
- clean-frame filtering
- strict-clock validation
- grouped reduction check against the `025` reduced target
- no broad selector sweep
- no larger static word catalog

Success criteria:
1. Identify at least one `030` seed pair with a compact exact collision certificate.
2. Show that the collision is resolved by one extra bit of context or one localized repair gate.
3. Find a nonbaseline all-color Latin/clean/strict realization on `m=5,7,9`.
4. Preserve the `025` reduced target at least to first order:
   - grouped base orbit size `m^2`,
   - intended omitted-edge cocycle behavior.
5. Preferably persist at `m=11`.

Failure criteria:
- every one of the `14` seed pairs requires more than one extra bit or more than one repair class, or
- every one-bit / one-gate repair still yields 0 Latin survivors, or
- every Latin repair destroys the `025` reduced target immediately.
- If failure occurs, state clearly whether the next smallest live branch is:
  - a two-state transducer,
  - or a defect-splice mechanism larger than one local repair.

Artifacts to save:
- code
- raw logs
- summary report
- seed_pair_collision_profiles.json
- seed_pair_rankings.json
- repair_microfamily_summary.json
- validation outputs
- discovered survivors / counterexamples
- proof-supporting computations

Return format:
- exact seed pairs analyzed
- exact Latin collision certificates
- ranking of the best seed pairs
- one-bit / one-gate repair families tested
- best nonbaseline survivor, if any
- strongest obstruction if none survives
- explicit recommendation: one-bit memory sufficient or not

Reproducibility requirements:
- fixed seed-pair list from `030`
- fixed moduli `5,7,9,11`
- deterministic enumeration order
- saved JSON summaries for collision certificates and repair tests
- exact scripts for all-color Latin / clean / strict validation
- explicit comparison against the `025` reduced target
```

The brief level I want is:

**one seed pair, one extra bit, one repair gate.**
If that fails cleanly, we will know the next branch really is a genuine two-state transducer, not just “a better fixed word choice.”
