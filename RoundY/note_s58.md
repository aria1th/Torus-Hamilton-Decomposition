043 clarifies the frontier a lot.

The cleanest reading now is not “find a better observable for raw (q).” It is:

[
B ;\leftarrow; B+c ;\leftarrow; B+c+d,
]

with

[
B=(s,u,v,\mathrm{layer},\mathrm{family}),\qquad
c=\mathbf 1_{{q=m-1}},\qquad
d\in{0,1}.
]

And the roles are now sharply separated:

* **control / trigger level:** (c) is the live missing lift;
* **structural / theorem level:** (d) is the residual binary noncarry sheet.

That is the right d5 language now.

I also wrote the next-spec draft here:

[044 carry + finite-cover spec](sandbox:/mnt/data/d5_carry_and_finite_cover_044_spec.md)

## What 043 really changed

The decisive point is that (d) is no longer a vague hidden state.

It is now a very specific object:

* binary,
* supported only on the **regular noncarry** branch,
* unnecessary for exceptional trigger logic,
* unnecessary for regular trigger logic once (c) is known,
* needed only to make the lifted active dynamics deterministic.

So (d) is a **structural sheet**, not the next local controller target.

That means the right split is:

* **local branch:** realize (c);
* **theorem branch:** understand (d).

Not the other way around.

## What I think should be proved next

There are really two theorems to aim at.

### 1. Finite-cover theorem for the active branch

Prove, first on the checked moduli and then in a theorem-shaped way, that the best-seed active branch factors as:

* grouped base (B),
* carry lift (c),
* residual binary sheet (d),

with:

* exceptional fire descending to (B),
* regular fire descending to (B+c),
* and deterministic active evolution closing on (B+c+d).

This is the manuscript-level statement.

The important extra statement to prove is that the support of (d) lies entirely on the regular noncarry region. That makes the whole picture much cleaner: (d) is a transient refinement of the noncarry dynamics, not a global extra coordinate.

### 2. Carry-realization theorem

Separately, search for the smallest admissible realization of

[
c=\mathbf 1_{{q=m-1}}.
]

This is the next concrete branch because (c) is already enough for exact trigger logic.

That makes it much smaller than “realize the whole cover.”

## The key strategic consequence

I would **not** try to realize (d) locally yet.

The future-carry-window lengths (6,29,55,89) are a strong warning that (d) is not a tiny current observable on the first natural families. So trying to make (d) local before settling (c) is likely to waste effort.

By contrast, (c) is already the smallest verified positive lift, and it is the one that matters for the actual firing logic.

So the next exact question is not:

> can we expose the whole structural lift?

It is:

> can we expose the carry slice admissibly?

## The theorem-friendly formulation I would push

The nicest d5 formulation now is:

* base grouped skew-odometer state (B),
* a carry sheet (c),
* a residual binary anticipation sheet (d) on regular noncarry states.

I would probably start calling (d) something like the **residual noncarry sheet** or **binary anticipation sheet**.

The fact that “time to next carry” coordinatizes (d) is very important. It means the object is not arbitrary; it is tied to the return structure of the odometer skeleton. So d5 is looking less like a controller search and more like:

**odometer/skew base + finite cover induced by carry anticipation.**

That fits the d3/d4/d5 story much better.

## My best next branch split

I would separate the work like this.

### 044A — local / admissibility branch

Target:
[
c=\mathbf 1_{{q=m-1}}.
]

Goal:
find the smallest admissible observable or lifted admissible gadget that realizes the carry slice.

Success here is already meaningful even if (d) remains nonlocal.

### 044B — structural / theorem branch

Target:
extract (d) intrinsically.

Goal:
turn “time to next carry” into a theorem-friendly coordinatization of the residual 2-sheet and prove that the active branch is a grouped base with a transient binary noncarry lift.

This branch should try to prove:

* (d) is irrelevant on carry and exceptional states,
* (d) is only needed on regular noncarry states,
* carry events reset or merge the (d)-fibers.

That last point would be especially good for the manuscript, because then (d) becomes a temporary sheet between carries, not a permanent hidden coordinate.

## What I would not do now

I would stop:

* broad lifted-observable search for full raw (q),
* generic transducer search,
* direct local search for (d),
* more grouped-state-descending families that still collapse to current (B).

043 already tells us the interesting object is above that level.

## My current best manuscript-level picture

The clean theorem narrative now looks like this:

* **d=3:** odometer return map;
* **d=4:** affine / second-return odometer;
* **d=5:** grouped skew-odometer base plus carry sheet plus residual binary noncarry cover.

That is a real progression, and it is cleaner than a raw-coordinate controller story.

The strongest thing to prove next is not “D5 needs raw coordinates.” It is:

**D5 needs only a tiny finite cover over the grouped odometer base, with the carry slice as the first genuinely local missing lift.**

If you want, I can turn this into a tighter theorem note with candidate lemma labels and a manuscript-style “D5 finite-cover normal form” statement.
