# D5-TWIST-GEOMETRY-ANALYSIS-010

## Executive summary

This artifact turns Sessions `008` and `009` into one clean diagnostic statement.

Main result:

- Session `008` already had exactly one mixed cycle profile:
  - `m=5`: `5` cycles of length `5`
  - `m=7`: `7` cycles of length `7`
  - `m=9`: `9` cycles of length `9`
- the only thing that changed across mixed survivors was the monodromy law, and that law depended only on the ordered layer-3 slice pair.

The new fact from this analysis is stronger:

- in Session `009`, Stage `1`, **every** clean strict survivor has exactly the same cycle signature;
- in Session `009`, Stage `2`, **every** clean strict survivor still has exactly the same cycle signature;
- the Stage `2` stability spot-checks on `m=11,13` also share one cycle signature.

So the best-supported diagnosis is:

**within the current twist-graft family, cycle geometry rigidifies to the universal `m`-cycle profile, while the ordered layer-3 slice pair controls the nonzero holonomy.**

That is stronger than the earlier informal reading “layer 2 chooses geometry, layer 3 adds twist.” The saved data say the current graft family does not preserve the stronger layer-2 cycle geometry at all; it collapses everything to the same simple base regime and only varies the holonomy.

## What was checked

Using the saved exact outputs from:

- Session `008`
  - `artifacts/d5_layer3_mode_switch_008/data/validation_summary.json`
- Session `009`
  - `artifacts/d5_strong_cycle_mix_009/data/search_summary.json`
  - `artifacts/d5_strong_cycle_mix_009/data/validation_summary.json`
- earlier cycle-only baseline
  - `artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json`

the script computed:

- exact `U_0` cycle signatures on each tested modulus;
- exact monodromy signatures on each tested modulus;
- ordered-pair monodromy laws;
- per-seed cycle-signature summaries;
- the Stage `2` “alt-4 rescue” table by layer-3 old bit.

## Exact conclusions

### 1. Session `008`

- mixed survivor count: `24`
- unique mixed cycle signature count: `1`
- ordered pairs
  - `(0/3,3/0)`
  - `(0/3,3/3)`
  - `(3/0,0/3)`
  - `(3/0,3/3)`
  - `(3/3,0/3)`
  - `(3/3,3/0)`
  each have exactly one monodromy signature
- that law is independent of predecessor flag and layer-2 orientation on the saved pilot data

So Session `008` is already a clean holonomy law over one fixed base cycle structure.

### 2. Session `009`, Stage `1`

- clean strict survivor count: `240`
- unique clean strict cycle signature count: `1`
- mixed improvement count over the Session `008` baseline: `0`
- ordered-pair monodromy law is exact and pair-only again

### 3. Session `009`, Stage `2`

- clean strict survivor count: `960`
- unique clean strict cycle signature count: `1`
- mixed improvement count over the Session `008` baseline: `0`
- ordered-pair monodromy law is still exact and pair-only

### 4. Alt-`4` seeds in Stage `2`

Stage `2` does restore mixed behavior on the strongest layer-2 seeds, but only by turning holonomy on:

- for `q=-1` alt `4` and `w+u=2` alt `4`
  - layer-3 bit `q=-1` gives only cycle-only rows
  - layer-3 bits `q+u=1`, `q+u=-1`, `u=-1` give only mixed rows

But their cycle signature stays the same in every case.

So even the “rescued” strong cycle seeds do not carry their old compression into the twist-graft family.

### 5. Stability spot-checks

For the top `12` mixed Stage `009` survivors:

- unique cycle signature count on `m=11,13`: `1`
- unique monodromy signature count on `m=11,13`: `1`
- all checked rows remain mixed

This does not prove a theorem, but it supports the same diagnosis beyond the pilot range.

## Clean explanation

The clean explanation to hand over is:

- the current predecessor gadget is a **holonomy gadget**;
- it changes the monodromy class carried by a cycle;
- but in the present graft family it does **not** change the cycle partition.

Equivalently:

- this family behaves like a cocycle over a fixed universal base map,
- not like a genuinely coupled geometry-changing perturbation.

## Why this matters

This tells us what the next successful branch probably must do.

The remaining problem is not “find more one-bit twist flags.”

Those already work very well at changing holonomy.

The remaining problem is:

**how to make the twist interact with geometry instead of merely decorating it.**

So the next serious branches are:

1. a theorem-level classification of the current twist-graft family as universally `m`-cycle;
2. a genuinely interactive layer-2/layer-3 gadget that can perturb the base geometry itself.

## Files

Primary output:

- `data/analysis_summary.json`

Log:

- `logs/analysis.log`

Code:

- `code/torus_nd_d5_twist_geometry_analysis.py`

Inputs copied into the bundle:

- `inputs/d5_twist_graft_explanation.md`
- `inputs/note_s26.md`
- `inputs/codex_work_s26.md`
- `inputs/note_s27.md`
- `inputs/codex_work_s27.md`

## Reproducibility

Command used:

```bash
python -m py_compile scripts/torus_nd_d5_twist_geometry_analysis.py

python scripts/torus_nd_d5_twist_geometry_analysis.py \
  --out artifacts/d5_twist_geometry_analysis_010/data/analysis_summary.json \
  --no-rich
```

Runtime in this run:

- `0.309s`

The bundle also includes `SHA256SUMS.txt`.
