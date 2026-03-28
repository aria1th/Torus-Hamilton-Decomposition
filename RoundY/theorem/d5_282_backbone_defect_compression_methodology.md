# D5 282 Backbone-Defect Compression Methodology

This note records the current high-level methodology suggested by the later
`d=5` work and translates it into the present RoundY language.

The point is not to add a new theorem. It is to state clearly what kind of
method actually worked in `d=5`, and what part of that method should be
exported to later dimensions.

## 1. One-line summary

The successful `d=5` approach is not:

- “search directly for all five Hamilton colors.”

It is:

- fix the exact backbone first,
- compress the remaining colors by return maps,
- isolate the residual defects on thinner and thinner supports,
- and only then search inside the resulting finite normal-form family.

So the right summary is:

> the core method is compression, not discovery.

## 2. The actual chain seen in the current D5 work

In current RoundY language, the live graph-side chain is best read as

- raw selector
- exact backbone colors
- residual colors
- section / return maps
- reduced affine models
- resonance split
- wall localization
- finite local exactness / gate problem

This is exactly how the recent notes behave.

### A. Exact backbone first

The key move was not to solve all five colors simultaneously.

Instead:

- the color-`4` branch was closed first by the `119–122` final-section route;
- the color-`3` branch was then closed by the `257–266` Route-E line.

So the real unresolved graph-side problem was no longer “five colors at once,”
but the residual colors left after freezing the already exact backbone.

### B. Obstructions before repairs

The next decisive step was to understand why the raw package fails.

The obstruction notes
[d5_269_selstar_color12_return_invariant_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_269_selstar_color12_return_invariant_obstruction.md)
and
[d5_280_one_point_repair_color1_line_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_280_one_point_repair_color1_line_obstruction.md)
show the right pattern:

- first find the preserved structure,
- only then ask what local surgery is needed to break it.

So the repair problem is not

- “find a nicer selector,”

but

- “break the precise obstruction with the smallest possible local change.”

### C. Defect-supported surgery

The actual refinement line

- `274 -> 279 -> 281`

does not search arbitrary five-color packages.

It keeps shrinking the active repair support:

- first slice-class data,
- then defect markers,
- then one-point repair,
- then line-family refinement.

This is the right `d=5` lesson:

> repairs should live on thin defect sets, not on the bulk torus.

### D. Return ladders and exact clocks

The decisive structural content in the closed color branches came from

- `P0` first returns,
- section maps,
- lower-dimensional explicit models,
- and exact clock coordinates.

This is visible in the color-`4` notes `119–122` and the color-`3` notes
`257–266`.

The working principle is:

> do not read the full permutation first; descend to the return ladder and
> expose one exact clock at a time.

### E. Resonance matters

The later residual notes also show that arithmetic branching is real.

Examples already visible in the current work:

- `280` splits the repaired color-`1` obstruction by `3 \nmid m` versus
  checked multiples of `3`;
- earlier casebook-style observations also suggest finer congruence behavior.

So the robust methodological point is not any one specific modulus law.
It is:

> classify resonance before expecting one global normal form.

### F. Final defects should become finite objects

The end of the chain is always supposed to be finite.

In the present `d=5` branch this appears in two related forms:

- finite exactness CSPs such as `274`, `277`, `281`,
- and explicit small obstruction families such as `276` and `280`.

The right target is therefore:

> localize the residual defect until the remaining problem is a finite exactness
> or finite graph problem.

## 3. What is genuinely `d=5`-specific and what is exportable

Some parts are casebook details:

- the exact closure order of colors `3,4`,
- the concrete slice labels and branch formulas,
- the specific affine laws now seen in `275`, `276`, `280`,
- the one-point repair source from `279`.

These should not be copied blindly to higher dimensions.

What should be exported is the method:

- freeze the backbone first,
- identify raw obstructions as invariants or explicit residual structures,
- restrict surgery to thin defect supports,
- descend by return maps,
- split by resonance,
- and compress the last defect to a finite exactness / gate problem.

## 4. Consequence for later dimensions

If this methodology is used for `d=7`, the first goal should **not** be

- a full seven-color search.

The first goal should be:

- find the exact outer/backbone colors,
- isolate the central residual block,
- build the return ladder there,
- and only then begin defect-supported search.

So the correct transfer is:

> reuse the compression program, not the `d=5` formulas.

## 5. Current honest status

This methodology is strongly supported by the present `d=5` work:

- exact backbone closure is real,
- return-map reduction is real,
- defect localization is real,
- finite exactness compression is real.

But some later arithmetic taxonomy remains partly empirical:

- the best refined family is still not the final five-color theorem,
- and the full resonance taxonomy is not yet a finished theorem package.

So this note should be read as a methodological distillation of the current
evidence, not as a completed general theorem.

## 6. Bottom line

The `d=5` branch now supports the following practical slogan:

> First freeze the exact spine. Then compress the residual dynamics by return
> maps until only thin defect supports remain. Only after that should one do
> exact search, and even then only inside the finite normal-form family forced
> by the defect geometry.

That is the main durable lesson of the current `d=5` program.
