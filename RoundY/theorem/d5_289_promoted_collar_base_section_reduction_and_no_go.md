# D5 289 Promoted-Collar Base-Section Reduction And No-Go

This note promotes the `2026-03-25` resonant base-section memo into the stable
RoundY layer.

The point is not to claim a new final repair.
The point is to record that the current promoted-collar pure color-`1` package
has now been reduced one step further, and that this reduction changes how the
next theorem target should be stated.

The saved checked summary is
[d5_289_promoted_collar_base_section_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_289_promoted_collar_base_section_summary.json).

## 1. Exact reduction now available

For the promoted-collar color-`1` section return

`R = R^{(u)}_{1,m} = h_1^m |_{\Sigma=0}`

on the package

`\widehat{\mathfrak N}_m^{(u)} = \widehat{\mathfrak N}_m(1) \cup \{A_{u,3}\}`,

the following picture is now available.

- Every lower defect line normalizes into a finite entrance slab.
- The high-band behavior consists only of the already audited finite
  side-top / `chi`-active episodes.
- Therefore the global promoted-collar color-`1` problem reduces to an exact
  induced map on the base section

  `H_m = {c = 0, d = 0}`.

So the old four-dimensional section dynamics is no longer the right object to
look at directly. The remaining problem has already been compressed to an
`m^2`-state map

`F_m : H_m -> H_m`.

## 2. Checked no-go status

On the checked resonant moduli

- `m = 21, 27, 33, 39, 51`,

the induced map `F_m` is not a single cycle.

The checked cycle lengths are:

- `m = 21`: `220, 126, 95`
- `m = 27`: `343, 342, 44`
- `m = 33`: `538, 423, 128`
- `m = 39`: `412, 356, 333, 309, 111`
- `m = 51`: `661, 547, 444, 227, 165, 165, 165, 165, 62`

So the promoted-collar package is **not** a final Hamilton breaker on the
checked resonant branch.

This is not just a failed search anecdote.
It means the current promoted-collar family should now be treated as an
explicit reduced no-go packet.

## 3. The base subset reduction

Inside `H_m`, define the base subset

`B_m = {c = 0, d = 0, e = 0}`.

In the checked moduli above, every cycle of `F_m` meets `B_m`.
So the cycle decomposition of `F_m` is already visible in the next-return
permutation

`P_m : B_m -> B_m`.

The checked cycle lengths of `P_m` are:

- `m = 21`: `11, 5, 5`
- `m = 27`: `13, 12, 2`
- `m = 33`: `17, 11, 5`
- `m = 39`: `10, 9, 9, 8, 3`
- `m = 51`: `12, 10, 9, 6, 4, 3, 3, 2, 2`

So after all the current local transducers are resolved, the checked promoted
collar branch behaves like a genuinely one-dimensional permutation obstruction.

## 4. Consequence for the current idea

This refines the earlier priority note
[d5_288_next_closable_piece_priority.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_288_next_closable_piece_priority.md).

The old wording

- “prove a uniform double-top breaker theorem”

is now too coarse as an immediate next step.

The present better split is:

1. first close a **base-section reduction / no-go theorem** for the current
   promoted-collar package;
2. then phrase the next positive repair target as a theorem about changing the
   induced base permutation on `B_m`.

So the next question is no longer:

- “is the promoted-collar package already the final breaker?”

It is now:

- “what new repair changes the base permutation `P_m` after the current
  promoted-collar family has been reduced to its exact no-go core?”

## 5. Updated priority read

This does **not** move the project back to broad search.

It sharpens it further.

The next useful mathematical fragment is now best read as one of two closely
stacked targets:

1. immediate target:
   a theorem-level promoted-collar base-section reduction / no-go statement;
2. next positive target after that:
   a new repair theorem that changes the induced base permutation on `B_m`.

That is a more accurate formulation of the current resonant pure color-`1`
frontier than the earlier direct “double-top breaker” wording.

## 6. Bottom line

The promoted-collar family is no longer just a plausible candidate breaker.

It is now better understood as:

> a fully local-audited package whose remaining obstruction has already been
> compressed to an exact induced map on `H_m`, and in checked moduli further to
> a one-dimensional permutation obstruction on `B_m`.

That is the right place from which the next repair theorem should be stated.
