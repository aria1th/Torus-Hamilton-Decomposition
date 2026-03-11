# D5-ACTIVE-TAIL-GRAMMAR-002

## Executive summary

I split the Session 21 note into:

- `tmp/note_s21.md`
- `tmp/codex_work_s21.md`

and then executed the immediate Codex-side branch instead of stopping at the prose template.

Main result:

- The passive refined quotient `Theta_AB + phase_align + tail_cut` is **not** exhausted.
- There exists a **same-preference nonlifted pilot witness** on `m=5,7,9`.
- The solver proves this at the same preference score as the lifted strict-collapse field:
  `pref = 32176`, `changed_state_count = 22806`, `status = OPTIMAL`.
- So the strongest previous reading
  “passive one-bit tail refinement is inert”
  was too strong.

What the new witness does:

- it keeps Latin on the pilot range;
- it breaks the old collapse law on `m=5,7,9`;
- in the strongest same-preference variant it also breaks `strict_clock`;
- in the best lexicographic divergent variant it keeps `strict_clock=True` but still breaks the old collapse law and leaves `U_0` split into fixed points.

Second result:

- I extracted a concrete recursive second bit `b2` from the residual post-`tail_cut` fragments.
- Exact recursive max-cut gives:
  - `m=5`: `b2 = {1,3}`, residual excess `0`
  - `m=7`: `b2 = {1,2,4}`, residual excess `420`
  - `m=9`: `b2 = {1,3,5,7}`, residual excess `3354`

So the sharp handoff conclusion is:

- the passive branch admits nonlifted same-preference witnesses;
- `b2` is now concrete and exact;
- the next constructive step should use these two facts together, rather than trying to prove a passive no-go that is now false.

## 1. Passive divergence search

I ran two exact pilot searches on the current passive refined quotient:

1. `same_preference`
   - constraint: same preference score as the lifted field
   - objective: maximize the number of changed states
2. `best_divergent`
   - constraint: differ from the lifted field
   - objective: lexicographically maximize preference, then maximize changed states

### Same-preference witness

Status:

- `OPTIMAL`
- changed pilot states: `22806`
- preference score: `32176`

Pilot validation:

- `m=5`: Latin `True`, old collapse law `False`, clean frame `True`, strict clock `False`
- `m=7`: Latin `True`, old collapse law `False`, clean frame `True`, strict clock `False`
- `m=9`: Latin `True`, old collapse law `False`, clean frame `True`, strict clock `False`

Layer palettes:

- layer `2`: constant permutation `12340`
- layer `3`: constant permutation `12340`
- layer `4+`: constant permutation `01234`

Interpretation:

- This is already a decisive counterexample to the claim that the passive refined quotient only contains the lifted collapse field at optimal preference.

### Best divergent witness

Status:

- `OPTIMAL`
- changed pilot states: `22806`
- preference score: `32176`

Pilot validation:

- `m=5,7,9`: Latin `True`, old collapse law `False`, clean frame `True`, strict clock `True`
- `U_0` still splits into `m^2` fixed points
- all monodromies remain `0`

Layer palettes:

- layer `2`: constant permutation `23401`
- layer `3`: constant permutation `34012`
- layer `4+`: constant permutation `01234`

Interpretation:

- This field shows that even within the passive refined quotient, one can break the old collapse law while preserving clean-frame + strict-clock structure.
- So the real obstruction now sits deeper than the earlier strict-collapse law.

## 2. Exact `b2` extraction

I conditioned the exact residual support table on the first bit

`b1 = tail_cut`

and formed the residual fragment hypergraph consisting of the post-`b1` fragments of size `> 1`.

Then I solved the exact recursive max-cut on that residual hypergraph.

Results:

- `m=5`
  - `b1 = {1,2}`
  - `b2 = {1,3}`
  - residual fragment excess after `b2`: `0`
- `m=7`
  - `b1 = {1,3,5}`
  - `b2 = {1,2,4}`
  - residual fragment excess after `b2`: `420`
- `m=9`
  - `b1 = {1,2,5,6}`
  - `b2 = {1,3,5,7}`
  - residual fragment excess after `b2`: `3354`

This gives an exact, data-derived second bit. It is not guessed from arithmetic.

## 3. Strongest conclusion supported

The Session 21 branch changes the picture in two ways.

First:

- the passive refined quotient already contains nonlifted same-preference pilot witnesses.

Second:

- the recursive second bit `b2` is now explicit.

So the next constructive branch should be:

1. use the discovered divergent pilot witnesses as grammar seeds,
2. use the exact `b2` tables as the second tail bit,
3. search a small active layer-2/3 grammar around these discovered palettes.

What is no longer credible:

- treating the passive refined quotient as if it had already been proved inert.

## 4. Files

- Session note split:
  - `tmp/note_s21.md`
  - `tmp/codex_work_s21.md`
- Passive divergence search:
  - `data/passive_divergence_summary.json`
- Recursive `b2` extraction:
  - `data/b2_summary.json`
- Derived palette summary:
  - `data/discovered_grammar_tables.json`
- Raw logs:
  - `logs/passive_divergence.log`
  - `logs/b2_extract.log`

New code:

- `scripts/torus_nd_d5_tail_cut_passive_divergence.py`
- `scripts/torus_nd_d5_tail_cut_b2_extract.py`

Code reused directly:

- `scripts/torus_nd_d5_tail_cut_lookup_rerun.py`
- `scripts/torus_nd_d5_master_field_quotient_family.py`

## 5. Reproducibility

Commands used:

```bash
python -m py_compile \
  scripts/torus_nd_d5_tail_cut_passive_divergence.py \
  scripts/torus_nd_d5_tail_cut_b2_extract.py

python scripts/torus_nd_d5_tail_cut_b2_extract.py \
  --out artifacts/d5_active_tail_grammar_002/data/b2_summary.json \
  --no-rich

python scripts/torus_nd_d5_tail_cut_passive_divergence.py \
  --max-time-sec 60 \
  --out artifacts/d5_active_tail_grammar_002/data/passive_divergence_summary.json \
  --no-rich
```

The bundle also includes `SHA256SUMS.txt`.
