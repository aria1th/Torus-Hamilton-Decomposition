# D5-TAIL-AUTOMATON-BIT-EXTRACTION-001

## 1. Executive summary

Starting from the saved strict-collapse field on `Theta_AB + phase_align`, I extracted the exact residual nonzero-phase hypergraph on `\Delta_m = {1,\dots,m-1}` for `m = 5,7,9,11,13`, solved the exact one-bit optimization problem, and searched for a common quotient-level one-bit factor on natural automaton-context families.

Main outcome:

- The residual one-bit problem is exactly a weighted hypergraph max-cut.
- The unique optimal subsets modulo complement are:
  - `m=5`: `{1,2}`
  - `m=7`: `{1,3,5}`
  - `m=9`: `{1,2,5,6}`
  - `m=11`: `{1,2,6,7,8}`
  - `m=13`: `{1,4,5,7,8,10}`
- The pair graph and antisymmetric restriction agree through `m=11` and both fail first at `m=13`.
- No tested common one-bit automaton factor works. I tested `45` families built from current/predecessor/successor and entry-window states; `0` fit globally on `m=5,7,9,11,13`.
- The best tested family was `entry0__entry1__prev__state__next`, but it is exact only at `m=5` and already fails inside `m=7`.

Recommendation:

- Treat the one-bit branch as negative on the tested local automaton families.
- The next credible quotient should add **two tail bits**:
  - an **oriented entry-class bit** learned from the early return window;
  - a **local frozen-tail context bit** learned from predecessor/current/successor tail states.

## 2. Exact residual automaton / hypergraph definition

For each modulus `m`, I replayed the saved strict-collapse field under color `0` on all `m^4` start states `(q,w,v,u)` in `P_0`, collected every visited phase-align state with nonzero instantaneous hidden phase

`\delta = (x_3 - x_1) mod m in Delta_m`,

and grouped occurrences by exact quotient state.

For each residual state `s`, its support is

`S_s = { delta in Delta_m : s is visited at some occurrence with hidden phase delta }`.

The exact one-bit problem is then:

- vertices: `Delta_m`
- weighted hyperedges: one edge `S_s` for each residual state `s` with `|S_s| >= 2`
- identical supports are merged with multiplicity weight
- a proposed bit `chi : Delta_m -> {0,1}` cuts state `s` iff `chi` is nonconstant on `S_s`

Therefore minimizing residual excess is exactly weighted hypergraph max-cut.

Extracted support counts:

- `m=5`: `58` residual states, `8` unique supports
- `m=7`: `1829` residual states, `57` unique supports
- `m=9`: `5509` residual states, `235` unique supports
- `m=11`: `7387` residual states, `796` unique supports
- `m=13`: `8172` residual states, `1921` unique supports

Support-size histograms are saved in `data/hypergraph_extract.json`.

## 3. Optimal partition data

Exact hypergraph optima:

- `m=5`: best subset `{1,2}`, runner-up gap `12`
- `m=7`: best subset `{1,3,5}`, runner-up gap `14`
- `m=9`: best subset `{1,2,5,6}`, runner-up gap `28`
- `m=11`: best subset `{1,2,6,7,8}`, runner-up gap `13`
- `m=13`: best subset `{1,4,5,7,8,10}`, runner-up gap `1`

Comparators:

- Pair graph max-cut matches the hypergraph optimum for `m=5,7,9,11`.
- Pair graph first fails at `m=13`, where it selects `{1,2,5,6,9,10}`.
- Best antisymmetric partition also matches through `m=11`.
- Antisymmetry first fails at `m=13`, where the best antisymmetric subset is `{1,3,5,6,9,11}`.

These results are in `data/hypergraph_optimize.json`.

## 4. Learned quotient factor(s), or one-bit obstruction

No exact common one-bit factor was found in the tested automaton families.

Tested family universe:

- `45` families
- tokens drawn from `{state, prev_state, next_state, entry0_state, entry1_state, entry2_state}`
- included the richest local family `entry0__entry1__prev__state__next`

Negative result:

- `exact_fit_family_count = 0` globally on `m=5,7,9,11,13`
- `17` families happen to fit `m=5` alone
- `0` tested families fit `m=7`, and therefore none fit any larger tested modulus either

Best families by global conflict count:

- `entry0__entry1__prev__state__next`: mixed occurrences `328282`
- `entry0__entry1__state__next`: mixed occurrences `366898`
- `entry0__entry1__prev__state`: mixed occurrences `374904`
- best local-only family `state__prev__next`: mixed occurrences `459525`

Concrete obstruction inside `m=7` for the best family:

- Feature value
  `['L=0|sig=[4,0,4,0,4]', 'L=1|sig=[4,0,0,0,0]', '<START>', 'L=0|sig=[4,0,4,0,4]', 'L=1|sig=[4,0,0,0,0]']`
  occurs with both:
  - `delta=2`, which lies outside the exact optimum `{1,3,5}`
  - `delta=5`, which lies inside the exact optimum

So even the strongest tested entry-augmented one-bit context already mixes both target sides within a single modulus.

All tested families and example conflicts are in `data/factor_search_summary.json`.

## 5. Suggested next quotient schema

The next credible quotient refinement is a **two-bit tail grammar**:

- `tail_entry_orientation`
  - source: early return window `(entry0, entry1, entry2)`
  - role: break the symmetry that first becomes visible at `m=13`, where the optimum is no longer antisymmetric
- `local_tail_context`
  - source: predecessor/current/successor state on the frozen tail
  - role: split the residual mixed supports that remain even after entry information is included

This is a recommendation, not a proof of sufficiency. The present artifact is a one-bit obstruction plus a data-backed direction for the next branch.

## 6. Negative results for ruled-out factor families

Ruled out on the tested range:

- pure current-state factor
- predecessor/current factor
- predecessor/current/successor factor
- entry-window only factors
- entry-window plus current-state factors
- the richest tested local family `entry0__entry1__prev__state__next`

Also ruled out as exact surrogates for the one-bit optimization:

- pairwise co-occurrence graph alone
- pure antisymmetric `delta <-> -delta` orientation class alone

Both surrogates fail first at `m=13`.

## 7. Reproducibility notes

Scripts:

- `scripts/torus_nd_d5_tail_hypergraph_common.py`
- `scripts/torus_nd_d5_tail_hypergraph_extract.py`
- `scripts/torus_nd_d5_tail_hypergraph_optimize.py`
- `scripts/torus_nd_d5_tail_automaton_factor_search.py`

Commands used:

```bash
python -m py_compile \
  scripts/torus_nd_d5_tail_hypergraph_common.py \
  scripts/torus_nd_d5_tail_hypergraph_extract.py \
  scripts/torus_nd_d5_tail_hypergraph_optimize.py \
  scripts/torus_nd_d5_tail_automaton_factor_search.py

python scripts/torus_nd_d5_tail_hypergraph_extract.py \
  --out artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_extract.json \
  --no-rich

python scripts/torus_nd_d5_tail_hypergraph_optimize.py \
  --extract-json artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_extract.json \
  --out artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_optimize.json \
  --no-rich

python scripts/torus_nd_d5_tail_automaton_factor_search.py \
  --optimize-json artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_optimize.json \
  --out artifacts/d5_tail_automaton_bit_extraction_001/data/factor_search_summary.json \
  --no-rich
```

Raw logs are in `logs/`.
