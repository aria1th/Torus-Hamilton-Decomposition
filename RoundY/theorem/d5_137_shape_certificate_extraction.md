# D5 137: recovered finite seed certificate from the 030/032 artifacts

## Purpose

This note executes the concrete compute request isolated in `136`.
The goal is to recover as much of the remaining front-end seed certificate as
possible from the artifacts already present in this repository, without
reopening unrelated graph-side work.

## Inputs actually used

The needed upstream artifact is available locally after all.

- `artifacts/d5_endpoint_word_catalog_030/data/candidate_pairs.json`
- `artifacts/d5_endpoint_latin_repair_032/data/seed_pair_rankings.json`

The extraction script is:

- `scripts/torus_nd_d5_shape_certificate_extract_137.py`

The generated outputs are:

- `RoundY/checks/d5_137_shape_certificate_summary.json`
- `RoundY/checks/d5_137_shape_certificate_extract/class_table.json`
- `RoundY/checks/d5_137_shape_certificate_extract/class_table.csv`
- `RoundY/checks/d5_137_shape_certificate_extract/raw_seed_rows.json`
- `RoundY/checks/d5_137_shape_certificate_extract/details.json`

## Operational symmetry model

For the present recovery, the seed classes are quotiented by the front-end
normalizations that are already safe to use at manuscript level:

1. cyclic relabeling of the direction alphabet `{1,2,3,4}`;
2. simultaneous reversal of both endpoint words;
3. left/right swap.

This is intentionally conservative.
It is enough to recover the finite class table and the unique bridge-type
class, without building in stronger equivalences that have not been explicitly
packaged in the current one-corner rewrite.

## Main result

Filtering the `030` candidate-pair catalog by

- `distinct_layer2_across_m = true`, and
- `distinct_layer3_across_m = true`

produces exactly `11` surviving seed pairs.
Under the operational symmetry model above, these reduce to exactly `5`
symmetry classes.

Exactly one of those classes is an oriented bridge-type class, namely the class
containing the canonical pair

- left word `[2,2,1]`
- right word `[1,4,4]`

So the finite class enumeration and the bridge-class uniqueness step required
by `136` can now be stated concretely from repository-local data.

## Recovered class table

| class | member seed ids | best representative | shape summary | status |
|---|---:|---|---|---|
| `C0` | `0,3,4,8` | `[2,2,1] / [1,4,4]` | left/right each in `{AAB, ABB}` | `bridge` |
| `C1` | `2,9` | `[1,4,4] / [2,1,2]` | left in `{AAB, ABB}`, right `ABA` | nonbridge |
| `C2` | `1,10` | `[4,4,1] / [2,2,1]` | left/right each in `{AAB, ABB}` | nonbridge |
| `C3` | `5,7` | `[4,1,4] / [2,2,1]` | left `ABA`, right in `{AAB, ABB}` | nonbridge |
| `C4` | `6` | `[4,1,4] / [2,1,2]` | left/right both `ABA` | nonbridge |

Every recovered class has the shared bridge symbol `1` after normalization.
Only `C0` has the full oriented bridge form needed by the normal-form lemma.

## Explicit bridge normalization

The bridge class `C0` contains the following normalized representatives and
maps to the canonical pair:

- seed `4`: `[2,2,1] / [1,4,4]` by identity;
- seed `3`: `[1,4,4] / [2,2,1]` by left/right swap;
- seed `0`: `[1,2,2] / [4,4,1]` by simultaneous reversal of both words;
- seed `8`: `[4,4,1] / [1,2,2]` by reversal plus swap.

Thus the unique bridge-type class does normalize exactly to
`[2,2,1] / [1,4,4]`, in the sense requested by `136`.

## What this closes, and what it does not

This recovery closes:

- the finite surviving seed list;
- the symmetry-reduced class table;
- the certification that exactly one class is of oriented bridge type;
- the explicit normalization of that class to `[2,2,1] / [1,4,4]`.

This recovery does not yet close:

- manuscript-grade dispositions `{duplicate, closed, infeasible}` for each
  nonbridge class;
- short witnesses for each nonbridge disposition.

So the remaining gap behind the front-end shape theorem is now narrower than
`136` originally had to assume.
It is no longer the finite class enumeration itself.
It is the disposition/witness layer for the four recovered nonbridge classes.

## Practical consequence

The old statement “the `032` artifact is missing” is no longer correct at the
level of class enumeration.
The repository now contains enough data to support the following sharpened
status claim:

> the front-end seed certificate has been recovered through unique
> bridge-class isolation, but the nonbridge disposition table still needs an
> exact witness package.
