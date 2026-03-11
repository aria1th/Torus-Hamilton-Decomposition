# D5-ACTIVE-U0-MERGE-003

## Executive summary

I split the Session 22 source into:

- `tmp/note_s22.md`
- `tmp/codex_work_s22.md`

and then executed the Codex-side search on the smallest credible active two-bit family around the strict-clock seed.

Family searched:

- layer `0` anchor fixed to `1`
- layer `1` anchor fixed to `4`
- layer `4+` anchor fixed to `0`
- layer `2`, nonzero phase branch:
  anchor depends on `ctx = 2*b1 + b2`, with each context choosing either seed anchor `2` or alternate anchor `1`
- layer `3`, nonzero phase branch:
  anchor depends on the same `ctx`, with each context choosing either seed anchor `3` or alternate anchor `1`
- phase-aligned (`delta=0`) branches stay fixed at seed anchors `2` and `3`

This gives exactly `2^8 = 256` active tables. I searched all of them exactly on `m=5,7,9`.

Main result:

- only **one** rule survives the combined `Latin + clean_frame + strict_clock` filter
- that unique survivor is the original strict-clock seed itself:
  - layer 2 bits = `[0,0,0,0]`
  - layer 3 bits = `[0,0,0,0]`
  - layer 2 anchor always `2`
  - layer 3 anchor always `3`
- it still has trivial section dynamics:
  `U_0` has `m^2` fixed points and monodromy `0` on `m=5,7,9`

So this 256-rule active neighborhood is exhausted. Within this family, nontrivial `U_0` dynamics do **not** occur.

## What was tested

Reference data carried into this artifact:

- the exact `b1` and `b2` bits from Session 21
- the strict-clock seed `best_divergent_field`

Active family definition:

- `ctx = 2*b1 + b2 in {0,1,2,3}`
- layer 2 table has 4 binary choices:
  each context selects anchor `2` or `1`
- layer 3 table has 4 binary choices:
  each context selects anchor `3` or `1`

That is the smallest exact `(b1,b2)`-driven layer-2/3 family that interpolates between the known strict-clock seed and the strongest alternate constant-tail witness.

## Search outcome

Exhaustive search summary:

- total rules: `256`
- `Latin + clean_frame` survivors: `1`
- `Latin + clean_frame + strict_clock` survivors: `1`
- strict survivors with nontrivial `U_0`: `0`

Unique surviving rule:

- layer 2 bits: `[0,0,0,0]`
- layer 3 bits: `[0,0,0,0]`
- interpreted tables:
  - layer 2: every context uses anchor `2`
  - layer 3: every context uses anchor `3`

Pilot validation of that rule:

- `m=5`: clean frame `True`, strict clock `True`, `U_0` cycle count `25`, all cycle lengths `1`, all monodromies `0`
- `m=7`: clean frame `True`, strict clock `True`, `U_0` cycle count `49`, all cycle lengths `1`, all monodromies `0`
- `m=9`: clean frame `True`, strict clock `True`, `U_0` cycle count `81`, all cycle lengths `1`, all monodromies `0`

So this family produces no `U_0` merging at all.

## Strongest conclusion supported

The project has moved past the old “strict collapse” frontier, but this specific next family still fails.

What is now ruled out:

- a `(b1,b2)`-driven layer-2/3 grammar that only toggles between the seed anchors `2/3` and the alternate anchor `1`
- any rule in that 256-table neighborhood producing nontrivial `U_0` dynamics while preserving `Latin + clean_frame + strict_clock`

What remains plausible:

- active grammars that also use richer local data, such as old atom bits or `phase_align`
- a larger active palette neighborhood around the seed
- a structural no-go theorem for this minimal `(b1,b2)`-only family

The right handoff reading is:

- Session 21 killed the “passive-inert” story.
- Session 22 kills the smallest exact active `(b1,b2)` neighborhood around the seed.
- So the next honest branch must use richer local information than `(b1,b2)` alone, or prove that such minimal active families can never merge `U_0`.

## Files

- Search summary:
  - `data/active_search_summary.json`
- Best rule:
  - `data/best_rule.json`
- Reference inputs copied in:
  - `data/reference_b2_summary.json`
  - `data/reference_passive_divergence_summary.json`
- Raw log:
  - `logs/active_search.log`

Split Session 22 documents:

- `tmp/note_s22.md`
- `tmp/codex_work_s22.md`

New code:

- `scripts/torus_nd_d5_active_u0_merge_search.py`

## Reproducibility

Commands used:

```bash
python -m py_compile scripts/torus_nd_d5_active_u0_merge_search.py

python scripts/torus_nd_d5_active_u0_merge_search.py \
  --out artifacts/d5_active_u0_merge_003/data/active_search_summary.json \
  --no-rich
```

The bundle also includes `SHA256SUMS.txt`.
