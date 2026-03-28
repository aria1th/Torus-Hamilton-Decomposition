# D5 299 Resonant Late First Exact Promotions

This note records the outcome of the first two full exact `B_m` promotions
selected by the late mod-`30` routing note
[d5_298_resonant_late_mod30_routing_note.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_298_resonant_late_mod30_routing_note.md).

The promoted pair was:

- `183`, central pair
- `201`, flank pair

The replay used the same exact runner and helper stack as the late atlas:

- [torus_nd_d5_resonant_late_campaign_297.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_resonant_late_campaign_297.py)
- [d5_299_resonant_late_first_exact_promotions_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_first_exact_promotions_summary.json)
- [per_case.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_first_exact_promotions/per_case.json)

The raw per-run outputs are also saved under:

- [d5_299_resonant_late_promotions_183_central_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_promotions_183_central_summary.json)
- [full_b_selected.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_promotions_183_central/full_b_selected.json)
- [d5_299_resonant_late_promotions_201_flank_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_promotions_201_flank_summary.json)
- [full_b_selected.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_299_resonant_late_promotions_201_flank/full_b_selected.json)

## 1. `183`, central pair

At `m = 183`, the central late family is a full exact `B_m` win.

The induced base permutation on `B_183` is:

- a genuine permutation of the `183` base states;
- one single cycle of length `183`;
- with zero-state data `0 -> 138` after `3,683,909` section blocks;
- and with maximum first-return depth `24,580,835` over all starting states.

So the `3 mod 30` central-first lane is no longer supported only by zero-state
atlas data and older medium-range wins.  It now has a new late exact
branch-defining promotion at `183`.

## 2. `201`, flank pair

At `m = 201`, the flank late family is **not** Hamilton on `B_201`.

The induced base permutation on `B_201` is still a genuine permutation, but it
splits into three cycles:

- `103`
- `57`
- `41`

with short-cycle witnesses starting at:

- `a = 0` for the `103`-cycle,
- `a = 10` for the `57`-cycle,
- `a = 3` for the `41`-cycle.

The zero-state data are still the atlas-favored ones:

- `0 -> 80` after `3,272,300` section blocks;
- maximum first-return depth `14,665,604`.

So the atlas-favored family at `201` is genuinely the right family to promote
first, but it is not yet the final winner.

## 3. What this changes

This sharpens the interpretation of
[d5_298_resonant_late_mod30_routing_note.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_298_resonant_late_mod30_routing_note.md).

The mod-`30` routing picture should now be read as:

- a law for **which family to promote first**;
- not a law saying that the first promoted family is already Hamilton.

Concretely:

- `3 mod 30` central-first is materially strengthened by a new exact late win
  at `183`;
- `21 mod 30` flank-first remains the right first promotion rule, but the
  first promoted family at `201` still fails and the drift lane remains
  unresolved.

So the late branch now has a noticeably asymmetric shape:

- the central lane has moved one step closer to theorem-level stability;
- the drift/flank lane still needs a second exact step after the first
  promotion.

## 4. Operational consequence

The next exact late jobs should no longer be read as a blind continuation of
the old promotion list.

The current best read is:

1. keep `213`, central, as the next clean central-lane confirmation;
2. treat `201` as a genuine drift-lane comparison modulus, not as “already
   settled by flank-first routing”;
3. compare that with `207`, flank, as the next flank-lane promotion.

So `299` does not close the late resonant theorem.
But it does move the late campaign from “first-family routing” to
“winner-versus-routing separation”, which is a more informative frontier.
