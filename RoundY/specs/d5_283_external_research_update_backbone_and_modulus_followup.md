# D5 External Research Update: Backbone Methodology And Modulus Follow-Up

What seems worth communicating at this point is not just one more list of
checked moduli, but the methodological picture that has now emerged from the
`d=5` work.

The shortest honest summary is this:

we did **not** solve the `d=5` problem by searching directly for a full
five-color selector package. Instead, we progressively compressed the problem
until the remaining obstruction lived on much thinner and more rigid supports.

In that sense, the governing method has been **compression rather than
discovery**.

## 1. What the D5 program is really doing

The actual chain now visible in the `d=5` work is roughly

- raw selector,
- exact backbone colors,
- residual colors,
- section / return maps,
- reduced affine or odometer models,
- resonance split,
- wall localization,
- finite exactness / finite gate problem.

This matters because it changes how one should read both the successes and the
failures.

The problem was never “find five Hamilton colors all at once.” The real
strategy has been:

1. freeze the colors that already close cleanly,
2. understand why the remaining colors fail,
3. allow repairs only on thin defect supports,
4. descend by return maps until exact clocks appear,
5. split by resonance,
6. and only then search inside the resulting finite normal-form family.

## 2. What is already structurally closed

Two backbone colors are now genuinely closed by theorem-style routes.

- The color-`4` branch closes through the final-section / corrected-row line.
- The color-`3` branch closes through the Route-E reduced-model line.

So the graph-side problem is no longer a five-color problem in any naive
sense. Once those branches are frozen, the real unresolved burden is the
residual assembly problem on the remaining colors.

That is the first major methodological lesson:

> do not attack the whole selector at once; freeze the exact backbone first.

## 3. Why the residual problem is not a blind search problem

The next decisive step was to identify *structural obstructions* rather than to
continue with brute-force selector search.

Earlier obstruction notes showed that the raw remaining colors could preserve
simple first-return invariants. This meant the issue was not “insufficient
mixing” in a vague sense, but rather that the current selector was formally
prevented from being Hamilton.

That reoriented the search completely.

The question became:

> what is the smallest local surgery that breaks the actual obstruction?

not:

> what new selector family happens to look better in experiments?

This is the second major methodological lesson:

> identify the obstruction first, then design the repair.

## 4. The importance of thin defect supports

Another robust feature of the `d=5` work is that useful repairs never lived on
the full torus in any uncontrolled way.

Instead, the later search line kept compressing the active repair support:

- first slice-class data,
- then defect markers,
- then a one-point repair,
- then a more explicit residual line family.

So the working pattern has been:

> keep the repair on codimension-two or otherwise thin defect sets whenever
> possible.

This is why the later notes become more interpretable, not less: the remaining
freedom is continuously shrinking.

## 5. Return ladders are doing most of the real work

The closed branches were not understood by reading the full torus permutation
directly.

What actually worked was to pass to return ladders:

- first return on `P0`,
- then section return,
- then lower-dimensional explicit model,
- then stitching on that reduced model.

In other words, the dynamics became visible only after exposing exact clocks one
at a time.

This is the third major methodological lesson:

> do not try to read the full map first; descend to return maps until an exact
> clock coordinate appears.

## 6. What the recent residual notes now show

Inside the compressed five-color family, the first clean residual target was
color `2`.

That branch was then analyzed far enough to identify explicit short-cycle
families, feed the corresponding markers back into the finite exactness CSP,
and ultimately isolate a one-point repair that restores checked exactness on

- `m = 7,9,11,13,15,17`

while making color `2` Hamilton throughout that checked range.

So color `2` is no longer the right place to think of as the main obstruction
inside the current repaired family.

The next residual issue is color `1`.

And here the picture has become sharper, not murkier:

- for odd `m` with `3 \nmid m`, the current repaired family still preserves an
  explicit affine line family on `P0`,
- this produces exactly `(m-1)^2` short cycles of length `m^2` for color `1`,
- so the family is visibly non-Hamilton there.

This is useful because it means the remaining problem is no longer “some color-1
behavior still looks wrong.” It is:

> the repaired family still leaves invariant a very specific affine line family.

That gives a much cleaner target for further refinement.

## 7. What the line-bit follow-up teaches

We then asked the obvious next question:

if the exactness CSP is allowed to *see* this color-`1` line relation as a
local class bit, is that already enough to finish the assembly problem?

The answer appears to be no.

The refined family is still exact on the checked search moduli, but the best
time-limited solutions do not close the remaining colors on

- `m = 9,11,13`.

So the line relation was the right obstruction to isolate, but it is not yet
the full repair datum.

This suggests a very specific next step:

> not another broad search, but the smallest local refinement that tracks how
> this line family is transported or phase-marked through the residual branch.

## 8. How the modulus follow-up at 63, 69, 75 fits into this picture

The new modulus data are valuable precisely because they reinforce the same
methodological message.

The tested canonical sigma-core packages were

- `K_m(rho,C,id)`,
- `K_m(rho,rho,id)`,
- `K_m(rho,C,B)`.

The cleanest current reading is:

### A. There really is a coarse modulus law for the bare sigma-core

The follow-up values

- `m=63`,
- `m=69`,
- `m=75`

support the same coarse pattern already seen at

- `33,39,45,51,57`.

Namely:

- residues `9,15 mod 24` continue to support the bare canonical sigma-core
  `K(rho,C,id)`,
- residues `21,3 mod 24` continue to fail.

So `mod 24` still looks like a meaningful coarse predictor for whether the
*bare* sigma-core closes.

### B. But the failure mechanism is not determined by mod 24 alone

This is the more important point.

The new failures do **not** behave uniformly inside a fixed bad residue class.

- `m=45` and `m=69` are both `21 mod 24`, but they fail for different reasons.
  `45` looked like a wall-localized color-`0` near-miss after the `B` booster,
  whereas `69` looks like a color-`1` bottleneck and the `B` booster is
  harmful rather than helpful.
- `m=51` and `m=75` are both `3 mod 24`, but again the internal repair picture
  differs. `75` is hybrid: `B` strongly improves color `0`, yet leaves color
  `1` completely unresolved.

So the right reading of the modulus table is *two-level*:

1. `mod 24` appears to predict whether the bare sigma-core succeeds or fails.
2. Once failure occurs, `mod 24` is **not** enough to predict the correct
   repair mechanism.

This is exactly consistent with the present `d=5` compression picture:

- a coarse arithmetic law can govern the first branch split,
- but actual repair still depends on finer local geometry.

## 9. Why this matters for future dimensions

If one tries to move from `d=5` to `d=7`, the transferable content is **not**
the specific support formulas or the exact affine law that appears for the
current color-`1` obstruction.

What transfers is the method:

- freeze the exact backbone first,
- identify the raw residual obstruction,
- restrict surgery to thin defect supports,
- descend by return maps,
- split by resonance,
- and only then search inside a finite compressed family.

So the correct outlook for higher dimensions is not “copy the `d=5` formulas.”
It is:

> rerun the compression program from the start, using the `d=5` work as a
> methodological template rather than as a rigid ansatz.

## 10. Current honest status

At the moment, the `d=5` work supports the following claims quite strongly:

- the backbone-first strategy is real,
- the return-ladder reduction is real,
- the defect-localization strategy is real,
- the finite exactness compression is real,
- and the current residual problem is much smaller and more structured than the
  original five-color problem.

What is **not** yet finished is the final five-color assembly theorem.

So the right status is:

- not a completed final theorem package yet,
- but a much sharper and more rigid methodological framework than before.

## 11. Short version suitable for direct forwarding

If we wanted to summarize the present state in one compact paragraph, I would
say:

> The `d=5` work is no longer best viewed as a direct search for a full
> five-color Hamilton package. What has actually worked is a compression
> strategy: first freeze the colors that already close exactly, then study the
> remaining colors through return maps until exact clocks and reduced affine
> models appear, then restrict all repairs to thin defect supports, and finally
> compress the remaining obstruction to a finite exactness problem. The new
> modulus follow-up at `m=63,69,75` supports the same reading. It strengthens
> the coarse `mod 24` rule for when the bare sigma-core succeeds, but also
> shows clearly that the repair mechanism after failure is not determined by
> `mod 24` alone. In particular, different bad residues exhibit different local
> failure types, so the next progress is likely to come not from broader
> search, but from identifying the smallest additional local datum that refines
> the current residual branch structure.
