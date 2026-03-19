# D5 119 Selector-Star First-Return Factor Probe

This note records the first stable compute response to the request in
[../../tmp/d5_119_next_compute_request_selector_star.md](../../tmp/d5_119_next_compute_request_selector_star.md).

Primary artifacts:

- [../../tmp/d5_119_M5_return_probe_and_surgery_note.tex](../../tmp/d5_119_M5_return_probe_and_surgery_note.tex)
- [../../tmp/d5_119_next_compute_request_selector_star.md](../../tmp/d5_119_next_compute_request_selector_star.md)
- [../../scripts/torus_nd_d5_selector_star_factor_probe_119.py](../../scripts/torus_nd_d5_selector_star_factor_probe_119.py)
- [../checks/d5_119_selector_star_factor_probe_summary.json](../checks/d5_119_selector_star_factor_probe_summary.json)

## 1. Setup

Use the explicit selector surgery `Sel*` from the tmp-119 package and keep the
note-117 slice-3 rule unchanged. For colors `c = 3,4`, study the first return

`R_c^* = (F_c^*)^m | P0`, with `P0 = {Sigma = 0}`.

The checked moduli are `m = 9,11,13`.

The script probes exactly the low-complexity families requested by `119`:

- 3-coordinate projections on `P0`;
- 3 chosen pair sums;
- 3 chosen pair sums plus one `Z/O/M` bit;
- 4 chosen pair sums;
- `disp4`, `ZM`, `B23ZM`, `B234ZOM`, and the full 5-tuple of pair sums;
- cyclic and dihedral orbit quotients of the ambient 5-tuple and of the pair
  sums.

## 2. Exact factors that were found

Among the tested families, the only exact first-return factors on all checked
moduli are:

- `pairs4:0123`, `pairs4:0124`, `pairs4:0134`, `pairs4:0234`, `pairs4:1234`;
- `pairs_full`.

For both colors `3` and `4`, each of these candidates has:

- state counts `9^4 = 6561`, `11^4 = 14641`, `13^4 = 28561`;
- `0` nondeterministic states on all checked moduli;
- maximal multiplicity `1`.

So the checked exact factors are not compressions to the `m^3` scale suggested
by the preferred Route A. They are exact only because they retain full `m^4`
information on `P0`.

## 3. Low-complexity families ruled out by the probe

No exact candidate of size `m^3`, `2m^3`, or any smaller orbit quotient was
found among the tested families.

In particular, none of the following produced an exact factor on
`m = 9,11,13`:

- any 3-coordinate projection;
- any 3 pair sums;
- any 3 pair sums plus one `Z/O/M` bit;
- `disp4`;
- `ZM`;
- `B23ZM`;
- `B234ZOM`;
- cyclic or dihedral orbit quotients of the ambient 5-tuple;
- cyclic or dihedral orbit quotients of the pair-sum 5-tuple.

The best compressed near-factors are:

- color `3`: `pairs3+bit:012+M0`, with state count `2m^3` and nondeterministic
  state counts `16,20,24` on `m = 9,11,13`;
- color `4`: `coords:023` and the equivalent pair-sum family `pairs3:123`
  (together with the same one-bit variants), with state count `m^3` and
  nondeterministic state counts `72,110,156` on `m = 9,11,13`.

So color `3` exhibits a plausible near-factor at `2m^3`, but color `4` still
shows a larger residual ambiguity even at the natural `m^3` scale.

## 4. M5 consequence

This probe does not close Route A from note `119`.

What it does show is sharper:

- the Hamilton colors of `Sel*` do carry exact first-return structure;
- the easiest exact structure currently visible is still `m^4`, not `m^3`;
- the most obvious linear, pair-sum, transported, displacement, and
  symmetry-quotient families do not explain the observed Hamiltonicity.

So the next M5 step should not be another blind small-family scan. The two
natural continuations are:

- identify a structured nonlinear surgery that compresses one of the exact
  `pairs4` factors to an actual `m^3` quotient; or
- abandon Route A at this level and build the nested-return tower from note
  `119`, using the `pairs4` exactness only as a bookkeeping lift.

In short: the first-return probe finds exact `m^4` factors and rules out the
standard low-complexity `m^3` candidates, so the live M5 problem is now a
genuine compression or nested-return problem rather than a missing small-field
guess.
