# D5 261 SelStar Color-3 Explicit Section Model All-m

This note records the current strongest theorem candidate on the live `Sel*`
color-`3` route.

Primary artifacts:

- [d5_258_selstar_color3_section_stitch.md](./d5_258_selstar_color3_section_stitch.md)
- [d5_260_selstar_color3_row_model_all_m.md](./d5_260_selstar_color3_row_model_all_m.md)
- [torus_nd_d5_selstar_color3_section_model_261.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_section_model_261.py)
- [d5_261_selstar_color3_section_model_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_261_selstar_color3_section_model_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_261_selstar_color3_section_model/per_modulus.json)

## 1. The model

Take the explicit three-dimensional section law from `258` on coordinates
`(a,b,e)`, with

- `c = 2 - a - b - e (mod m)`,

and update rules:

- `A`: if `a = m-1`, `c != m-1`, and `(b != m-1 or e = m-3)`,
  then `(a,b,e) -> (a,b,e+1)`;
- `B`: if `b = m-2`, `e != m-2`, and `(a != m-1 or e = 6)`,
  then `(a,b,e) -> (a+1,b+1,e)`;
- `C`: if `e = m-2` and `c = m-1`,
  then `(a,b,e) -> (a+1,b,e)`;
- `D`: if `a = m-1`, `b = m-1`, and `e notin {5,m-3}`,
  then `(a,b,e) -> (a+1,b,e+1)`;
- otherwise `G`: `(a,b,e) -> (a,b+1,e)`.

Write this explicit map as `T_m^sharp`.

## 2. Candidate theorem

For every `m > 2`, the explicit section model `T_m^sharp` is one `m^3`-cycle.

## 3. What is already closed inside that candidate

The `261` checker verifies, for every checked `m = 3,4,...,101`:

- `T_m^sharp` is a single `m^3`-cycle;
- the row section
  `B0 = {(a,b,e) : b = 0}`
  has first-return map that is a single `m^2`-cycle;
- the half-open first-return segments from `B0` are pairwise disjoint;
- those half-open segments cover all `m^3` states;
- for every checked `m >= 9`, the first return on `B0` agrees exactly with the
  explicit row model `W_m` from `260`.

So the structural picture is now very tight:

- the full three-dimensional section model is already globally Hamilton in a
  broad checked range;
- its `B0` return is already identified with the all-`m` row model from `260`
  in the checked range;
- and the `B0`-segment decomposition behaves exactly like a stitching theorem.

## 4. What still needs symbolic proof

There are now two different symbolic tasks, and they should not be confused.

### A. Model-internal closure

Inside the pure model `T_m^sharp`, one still wants a manuscript proof of:

- the exact `B0` first-return formula `T_m^sharp|_{B0} = W_m` for `m >= 9`;
- the fact that every point of the model hits `B0`;
- hence the model-internal stitching theorem
  `T_m^sharp` is one `m^3`-cycle.

The checked data strongly suggest that this should be short and fully
combinatorial.

### B. Actual D5 closure

Even after the model-internal theorem is proved, the actual graph-side D5 route
still needs the identification theorem:

- the true `Sel*` color-`3` section return equals the explicit model from `258`.

That is the real remaining live gap on the actual D5 side.

## 5. Consequence for the proof program

This changes the shape of the remaining work.

The old transport route from `G1/G2` is gone after `256`. The new endgame is:

1. close the explicit section model `T_m^sharp` as an all-`m` theorem;
2. prove that the actual color-`3` section map is exactly that model;
3. lift from the section model to the full torus map.

So the live color-`3` route is now much closer to the `120 -> 121 -> 122`
pattern than to the old transport pattern:

- first extract an explicit reduced model,
- then prove that reduced model stitches globally,
- then identify the actual return with that reduced model.
