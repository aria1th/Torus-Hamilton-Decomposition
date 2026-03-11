# D5-TAIL-CUT-QUOTIENT-RERUN-001

## Executive summary

This artifact closes the loop on the Session 20 `delta`-partition scan.

I used the exact residual hypergraph extracted in Session 19/20 support work, computed the exact incidence-signature quotient on the pilot moduli `m=5,7,9`, exported the exact pilot lookup bit

- `m=5`: `tail_cut(delta)=1_{delta in {1,2}}`
- `m=7`: `tail_cut(delta)=1_{delta in {1,3,5}}`
- `m=9`: `tail_cut(delta)=1_{delta in {1,2,5,6}}`

and reran the free-anchor master-field search on the refined quotient

`Theta_AB + phase_align + tail_cut`.

Main result:

- The incidence-signature quotient is already **discrete** on the pilot range:
  every nonzero hidden phase `delta` is its own signature class for `m=5,7,9`.
- The exact pilot `tail_cut` bit is therefore a legitimate quotient bit, not an arithmetic guess.
- However, adding this exact pilot bit gives **no structural gain** in the current free-anchor search.
- The pilot search on the refined quotient is `OPTIMAL`, and the optimal field is exactly the lifted projection of the old strict-collapse representative:
  `changed_state_count_vs_lifted = 0`.
- The tail still freezes:
  layers `2,3,4+` remain constant with permutation `01234`, so the old collapse law persists on the pilot range.

Sharp handoff conclusion:

- the exact one-bit `tail_cut` refinement is **combinatorially correct but dynamically inert** inside the present free-anchor search model;
- the next credible branch is therefore a **two-bit tail grammar**, not another single-bit phase partition.

## What was computed

### 1. Incidence-signature quotient

For each pilot modulus and each nonzero hidden phase `delta in Z_m^*`, I computed the incidence signature

`I_m(delta) = (1_{delta in D_tau})_tau`

over the exact residual support table `tau -> D_tau`.

Result:

- `m=5`: `4` classes on `Z_5^*`, all singleton
- `m=7`: `6` classes on `Z_7^*`, all singleton
- `m=9`: `8` classes on `Z_9^*`, all singleton

So the coarsest exact hidden-phase quotient on the pilot range is already discrete.

### 2. Post-cut support histograms

Using the exact hypergraph-optimal subsets, the post-split excess/histograms are:

- `m=5`
  - cut states: `56`
  - post-split excess: `14`
  - residual fragments: `14` fragments of size `2`
- `m=7`
  - cut states: `1391`
  - post-split excess: `1282`
  - residual fragments: `150` of size `3`, `982` of size `2`
- `m=9`
  - cut states: `4557`
  - post-split excess: `8150`
  - residual fragments: `640` of size `4`, `1144` of size `3`, `3942` of size `2`

These are exact recomputations from the saved support table, not inferred from aggregate scan scores.

### 3. Refined quotient rerun

I added the lookup bit

`tail_cut_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m in A_m}`

to the schema helper and reran the free-anchor CP-SAT search on the pilot union `m=5,7,9`.

Important implementation detail:

- the exact search is on the pilot union only, where the refined quotient has `54,982` states;
- a full union `m=5,7,9,11,13` search would require `142,422` states and was not used as the exact search model;
- for `m=11,13`, I only computed a **projected extension** of the pilot solution by using the searched pilot anchors on seen states and the lifted old projection on stability-only states.

## Search outcome

Pilot search result:

- schema: `joined_anchor_five_atom_phase_align_tail_cut`
- solver status: `OPTIMAL`
- pilot state count: `54,982`
- full state count for projected extension: `142,422`
- optimal preference score: `32,176`
- lifted baseline preference score: `32,176`
- changed pilot states vs lifted baseline: `0`

So the refined search found no improvement at all over the lifted strict-collapse field.

## Validation outcome

On the pilot moduli `m=5,7,9`, both the lifted field and the optimal searched field are the same object, and they satisfy:

- `clean_frame = True`
- `strict_clock = True`
- `U_0` splits into `m^2` fixed points
- all monodromies are `0`
- the old collapse law still matches exactly

The layer palettes are also unchanged:

- layer `2`: constant permutation `01234`
- layer `3`: constant permutation `01234`
- layer `4+`: constant permutation `01234`

So the tail remains frozen exactly as before.

For the projected extension to `m=11,13`:

- `strict_clock = False`
- `U_cycle_count = 0`

This is only a post hoc extension check, not a searched stability theorem, but it gives no evidence of rescue at larger moduli.

## Interpretation

This is a stronger negative result than the earlier “best arithmetic bit drifts with `m`” diagnosis.

What is now ruled out:

- the next useful quotient bit is not hiding in a small phase-equivalence quotient;
- the exact pilot hypergraph bit itself is not enough to change the free-anchor dynamics;
- a single extra hidden-phase bit, even when chosen optimally from the exact support hypergraph, does not break the collapse mechanism.

What remains plausible:

- a **two-bit tail grammar**, with one bit for oriented tail-entry data and one bit for local frozen-tail context.

## Files

- Signature / quotient summary:
  - `data/signature_summary.json`
- Refined search / validation summary:
  - `data/rerun_summary.json`
- Refined quotient state table:
  - `data/quotient_state_table.json`
- Refined quotient orbit table:
  - `data/rotation_orbits.json`
- Raw logs:
  - `logs/signature_extract.log`
  - `logs/rerun.log`

New or modified code used for this artifact:

- `scripts/torus_nd_d5_tail_cut_signature_extract.py`
- `scripts/torus_nd_d5_tail_cut_lookup_rerun.py`
- `scripts/torus_nd_d5_master_field_quotient_family.py`

## Reproducibility

Commands used:

```bash
python -m py_compile \
  scripts/torus_nd_d5_master_field_quotient_family.py \
  scripts/torus_nd_d5_tail_cut_signature_extract.py \
  scripts/torus_nd_d5_tail_cut_lookup_rerun.py

python scripts/torus_nd_d5_tail_cut_signature_extract.py \
  --out artifacts/d5_tail_cut_quotient_rerun_001/data/signature_summary.json \
  --no-rich

python scripts/torus_nd_d5_tail_cut_lookup_rerun.py \
  --max-time-sec 120 \
  --workers 8 \
  --out artifacts/d5_tail_cut_quotient_rerun_001/data/rerun_summary.json \
  --state-table-out artifacts/d5_tail_cut_quotient_rerun_001/data/quotient_state_table.json \
  --orbit-table-out artifacts/d5_tail_cut_quotient_rerun_001/data/rotation_orbits.json \
  --no-rich
```

The artifact bundle also includes `SHA256SUMS.txt`.
