041 is the first clean wall.

My read now is:

**the controller is solved, the first admissible quotient is too small, and the next honest object is a minimal lifted cover over the grouped model.**

That is more precise than “search another observable.”

What 041 really settled:

* `040` gave exact raw control.
* `041` proved that every first `025`-style **grouped-state-descending** surrogate still factors through current grouped state `(s,u,v)`, so none of them can express the needed trigger logic.
* So the missing state is not more controller logic. It is one **lifted** coordinate beyond the current grouped quotient.

I then did one follow-on check on the traced active union, because 041 still leaves one ambiguity: whether the missing lift should be thought of as “full q-like phase” or something smaller.

That check strongly suggests it is smaller.

## What I think the next direction is

Let
[
B=(s,u,v,\lambda,f),
]
where (\lambda=\text{layer}) and (f\in{\mathrm{regular},\mathrm{exceptional}}) is the carried family tag.

On the checked active union (`m=5,7,9,11`), I found:

1. (w) is already exact from grouped data:
   [
   w=s-u \pmod m.
   ]

2. Once (\lambda) is treated as already visible, the **exceptional** fire predicate is already a function of (B).

3. The **regular** fire predicate is not a function of (B), but it becomes exact after adding just the carry-slice bit
   [
   c=\mathbf 1_{{q=m-1}}.
   ]

So the trigger logic does **not** seem to need full raw (q). It seems to need only:

* visible layer,
* grouped state,
* family tag,
* and one extra carry-slice bit.

That is a real sharpening of 041.

## But there is one more split

That carry bit is enough for **triggering**.
It is not obviously enough for a **closed reduced dynamics**.

I checked that too.

If you use base
[
B=(s,u,v,\lambda,f),
]
then on the checked active union the fiber over (B) contains at most **3** raw (q)-values. In other words, the active raw model over grouped-plus-layer is not an (m)-sheet mystery anymore; it looks like a very small cover.

More importantly:

* adding only the carry bit (c=\mathbf 1_{{q=m-1}}) makes the fire predicates exact,
* but it does **not** make the active transition law closed/deterministic on the grouped model.

So the next branch depends on what kind of realization you want.

## The right split now

### If pointwise current observables are allowed

Then the next problem is:

**expose the carry-slice bit admissibly.**

That is the smallest positive target.

Because then:

* birth is already exact from `039`,
* family is already cheap,
* fire is exact from (B+c),
* and no full q-like lift is needed.

### If you want a self-contained reduced return-map model

Then the next problem is:

**extract the minimal lifted cover over ((s,u,v,\lambda,f)).**

My current guess is that this cover is genuinely **3-sheet** on the active regular branch.

That would be the d5 analogue of the d4 “second-return odometer” move:
not full raw coordinates, but a tiny lifted sheet coordinate.

## So the next thing to prove is not “admissible q”

It is one of these two sharper statements.

### Main structural target

Prove that, on the checked active union, the grouped-plus-layer model lifts to a finite cover
[
\pi:\widetilde B \to (s,u,v,\lambda,f)
]
with fiber size at most (3), and that:

* exceptional fire already descends to the base,
* regular fire descends to the base plus the carry sheet,
* the current `025`-style grouped-descending families cannot see that sheet.

### Stronger positive target

Find an admissible observable realizing either:

* the carry bit (c=\mathbf 1_{{q=m-1}}), if current evaluation is enough,
* or the full minimal 3-sheet coordinate, if you want closed reduced dynamics.

## What I would make the next branch

I would make `042`:

### D5-CARRY-SLICE-COVER-042

Question:
For the unresolved best-seed active corridor, is the exact missing admissible state just the carry-slice bit
[
c=\mathbf 1_{{q=m-1}},
]
or is the true minimal lifted object the smallest finite cover over
[
(s,u,v,\lambda,f)
]
that closes the active dynamics?

Purpose:
`041` kills grouped-state-descending surrogates.
`037–040` already solve the raw control logic.
So the next honest step is to identify the **smallest lifted coordinate** that remains.

Success criteria:

1. Prove on checked moduli that (w=s-u).
2. Prove exceptional fire is a function of ((s,u,v,\lambda,f)).
3. Prove regular fire is a function of ((s,u,v,\lambda,f,c)) with (c=\mathbf 1_{{q=m-1}}).
4. Prove (c) is not a function of ((s,u,v,\lambda,f)).
5. Extract the minimal cover of the active grouped model; determine whether its maximal fiber size is exactly (3).
6. Search admissible lifted observables only for:

   * the carry bit, or
   * that minimal cover coordinate.

Failure mode:
If neither the carry bit nor the 3-sheet cover can be exposed in the next admissible family, then the obstruction is no longer “missing coordinate” in the small sense; it is the admissibility class itself.

## What not to do now

I would stop doing:

* generic transducer search,
* larger versions of the 038-style local row,
* more grouped-descending point cocycle variants.

041 already told us those are too low.

## My best current belief

The most likely positive path is:

1. keep layer as visible,
2. treat family as already cheap,
3. identify the carry slice (q=m-1),
4. if needed, refine that to the minimal 3-sheet cover,
5. only then try to realize that lift admissibly.

So the frontier is no longer “find a controller.”

It is:

**find the smallest admissible lifted sheet over the grouped model.**

And I think the first exact thing to look for is not full (q), but the **carry slice**.
