# D5 116--118 Corrected Selector Frontier Summary

This note records how tmp notes `116`, `117`, and `118` change the current D5
graph-theoretic frontier.

Primary artifacts:

- [../../tmp/d5_116_slice4_transport_formula_note.tex](../../tmp/d5_116_slice4_transport_formula_note.tex)
- [../checks/d5_116_slice4_transport_formula_summary.json](../checks/d5_116_slice4_transport_formula_summary.json)
- [../../tmp/d5_117_M4_corrected_selector_theorem.tex](../../tmp/d5_117_M4_corrected_selector_theorem.tex)
- [../checks/d5_117_M4_corrected_selector_summary.json](../checks/d5_117_M4_corrected_selector_summary.json)
- [../../tmp/d5_118_M4_G4prime_M6_note.tex](../../tmp/d5_118_M4_G4prime_M6_note.tex)

## 1. What `116` does

`116` resolves the slice-4 transport/compression bottleneck isolated by `115`.

It proposes the explicit exact field

`F4sharp = (B2, B3, B4, Z, O, M)`,

with `O = {i : x_i = 1}`, and gives a direct local formula that reconstructs
the predecessor slice-3 field

`F3 = (B2, B3, Z, M)`

from `F4sharp(y)` and the predecessor generator `j`.

The accompanying check was rerun and matches the tmp summary exactly.

Main checked facts from
[d5_116_slice4_transport_formula_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_116_slice4_transport_formula_summary.json):

- exact formula verification for `m = 5,7,9,11,13`;
- state counts `621, 2112, 3882, 4661, 4746` on those moduli;
- dropping `O` fails already at `m = 5` and badly at `m = 9`;
- dropping `B4` also fails already at `m = 5`;
- dropping `B3` happens to pass at `m = 5` but fails by `m = 7`.

So the old slice-4 transport problem from `115` is no longer “search for an
intermediate field.” `116` proposes a concrete symbolic answer, with ablation
evidence that the added pieces are not accidental.

## 2. What `117` does

`117` replaces the old M4 target “compress the present raw selector row” by a
direct corrected selector theorem on the full torus.

Its structure is:

- on `Sigma = 2`, an explicit 32-subset correction rule depending only on
  `A2 = M - 1`;
- on `Sigma = 3`, an explicit two-bit correction rule depending only on the
  membership of `1,2` in `A3 = B2 triangle (M - 1)`;
- off slices `2,3`, the clean selector.

The rerun of the accompanying check also matches the tmp summary exactly.

Main checked facts from
[d5_117_M4_corrected_selector_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_117_M4_corrected_selector_summary.json):

- the slice-2 rule is a permutation on all `32` subsets;
- the slice-2 incoming color at generator `j` ignores the only predecessor bit
  that can vary at that generator;
- the slice-3 target-slice-4 equalities hold on checked moduli
  `m = 5,7,9,11,13`;
- type-level exactness holds on both defect slices for
  `m = 5,7,9,11,13,15,17,19`;
- the resulting global selector check is exact for `m = 5,7,9,11,13`.

So `117` is not just another compression experiment. It is a candidate direct
closure of M4 via a corrected selector package.

## 3. What `118` changes conceptually

`118` observes that if the corrected selector theorem of `117` is accepted,
then the old bridge-state wording of `(G4)` in note `103` was stronger than
needed.

The effective replacement is:

- `(G4')`: there exists some selector package on the full torus whose local
  selected arcs define the color maps under study.

With that weaker input, `118` argues:

- M4 is supplied directly by the corrected selector package from `117`;
- M6 is already an imported theorem from the odd-`m` globalization package;
- the remaining graph-level burden is therefore M5 for the corrected global
  color maps, together with any still-open upstream odd-`m` inputs.

This means `118` is mainly a packaging note. Its force depends on whether one
accepts `117` as the right theorem object.

## 4. Recommended reading and status

The practical reading order is now:

1. `115` for the old slice-4 bottleneck and the failed first search families;
2. `116` for the explicit symbolic replacement field `F4sharp`;
3. `117` for the corrected selector theorem candidate;
4. `118` for the repackaging “M4 and M6 are now closed, so M5 is next”.

Current status recommendation:

- treat `116` as a strong compute-backed symbolic closure of the slice-4
  transport step;
- treat `117` as the main new theorem candidate that should be reviewed and, if
  accepted, promoted;
- treat `118` as the correct downstream interpretation conditional on `117`.

In short: `116` appears to remove the old transport bottleneck, `117` proposes
to close M4 outright, and `118` explains why that would move the live graph
frontier from “selector construction” to “return-cycle lift for the corrected
maps”.
