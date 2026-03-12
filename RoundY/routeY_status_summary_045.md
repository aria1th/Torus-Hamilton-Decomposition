Yes — this is the right moment to freeze the map.

## Current north star

We are no longer trying to “find a controller” for the best-seed obstruction.

The controller is already known on raw coordinates.

The project has compressed to:

[
\text{admissible realization of the carry sheet } c
]

on top of the checked active normal form

[
B \leftarrow B+c \leftarrow B+c+d,
]

with

[
B=(s,u,v,\mathrm{layer},\mathrm{family}),\qquad
c=\mathbf 1_{{q=m-1}},\qquad
d=\mathbf 1_{{\text{next carry }u\ge m-3}}.
]

So the live question is no longer logic, phase, or routing. It is **exposure/admissibility of the first lifted sheet**.

---

## Where we are, in one line per branch

### Settled core

* `033`: the best-seed obstruction reduces to the single unresolved channel `R1 -> H_L1`.
* `035–037`: the long corridor already has visible raw odometer structure; phase is not hidden anymore.
* `038`: the exceptional family bit is cheap at birth; it is not the hard part.
* `039`: source and entry birth classes are exact on raw current coordinates.
* `040`: the reduced controller closes on raw current coordinates; simple 038-style richer rows still fail.
* `041`: first admissibility no-go — grouped-descending families through current grouped state are too small.
* `042`: regular trigger needs exactly the carry-slice bit (c); exceptional trigger already descends to (B).
* `043`: the structural lift over (B+c) is truly 2-sheet; the residual sheet is not a tiny obvious local bit.
* `044`: explicit normal form
  [
  B \leftarrow B+c \leftarrow B+c+d
  ]
  with canonical binary anticipation sheet
  [
  d=\mathbf 1_{{\text{next carry }u\ge m-3}}.
  ]

### Live branch

* `045`: search for an **admissible realization of (c)**.

### Parked for later proof

* finite-cover theorem writeup for `042–044`
* manuscript-level d3/d4/d5 odometer narrative

---

## The exact decomposition of the problem now

### 1. Local/search problem

Find an admissible observable, or smallest admissible lifted gadget, that realizes

[
c=\mathbf 1_{{q=m-1}}.
]

This is the only open local branch that matters right now.

### 2. Structural/theorem problem

Describe the active branch as a grouped odometer/skew-odometer base with tiny finite cover:

* base (B),
* carry sheet (c),
* binary anticipation sheet (d).

This is already the clean theorem language, even before admissibility is solved.

### 3. Integration problem

Once (c) is realized admissibly, combine it with the already checked raw control logic:

* birth on source/entry classes,
* family tagging,
* regular/exceptional firing,
* transport through the active corridor.

That will be the first real “end-to-end reduced mechanism” checkpoint.

---

## What is proved on checked moduli, versus what is still theorem-shaped

### Checked on (m=5,7,9,11)

* (w=s-u)
* exceptional fire is a function of (B)
* regular fire is not a function of (B), but is a function of (B+c)
* (c) is not a function of (B)
* (B+c) is not dynamically closed
* the minimal deterministic cover over (B+c) is 2-sheet
* the full checked active branch has normal form
  [
  B \leftarrow B+c \leftarrow B+c+d
  ]
* (d) has the canonical coordinatization
  [
  d=\mathbf 1_{{\text{next carry }u\ge m-3}}.
  ]

### Still theorem-shaped

* prove that this normal form holds uniformly in odd (m)
* prove that (d) is the natural binary anticipation sheet in general, not just on checked moduli
* prove that the active branch is best read as grouped skew-odometer base plus finite cover
* prove that the first admissible missing lift is exactly (c), not full raw (q)

---

## The clean status statement

Right now the project is:

[
\textbf{D5 = grouped base + carry sheet + binary anticipation sheet}
]

and the only live local obstruction is:

[
\textbf{admissible realization of the carry sheet } c.
]

That is the sharpest compact status line.

---

## Branches to keep separate

## A. Search/code branch — live now

This is your current work.

Goal:

* search admissible lifted families that do not descend to current (B)
* test whether they realize (c) exactly on the checked active union
* minimize the surviving family

Success criterion:

* exact realization of (c) on (m=5,7,9,11)
* preferably with a small, interpretable admissible family

Failure criterion:

* first genuinely lifted admissible families still cannot realize (c)

Meaning of failure:

* the obstruction is not just “one lifted coordinate beyond grouped state”
* it would mean the admissibility class being searched is still too small

## B. Structural/normal-form branch — already basically frozen

This branch is no longer exploratory.

Goal:

* package `042–044` into theorem language:

  * base (B)
  * carry sheet (c)
  * binary anticipation sheet (d)
* connect it to the d3/d4 odometer narrative

This does not need more search before it can be outlined.

## C. Proof branch — intentionally delayed

Goal:

* convert the checked `042–044` statements into lemma/proposition form
* only after the `045` search clarifies whether (c) is admissibly realizable

This is the right thing to delay until the search stabilizes.

---

## What not to reopen

These are no longer first-class branches.

* generic transducer search
* larger 038-style local row searches
* grouped-descending point-cocycle variants that still factor through current (B)
* full raw-(q) realization as the primary target
* local realization of (d) before (c) is settled

Those directions are now either dead or premature.

---

## The most useful waypoints from here

### Waypoint 1

A surviving admissible family for (c), or a solid no-go in the first lifted admissible class.

This is the next real fork.

### Waypoint 2

If (c) is realized:

* integrate it with the existing active controller
* verify exact birth / family / fire logic end-to-end on checked moduli
* then I switch to proof packaging immediately

### Waypoint 3

If (c) still fails in the next admissible family:

* promote the obstruction statement
* the next theorem becomes:
  “the grouped base needs a genuinely nontrivial admissible lift beyond the first natural carry sheet candidates”

---

## The manuscript-level story already visible

The clean d3/d4/d5 progression now looks like this:

* **d=3:** odometer return maps
* **d=4:** affine / second-return odometer
* **d=5:** grouped odometer or skew-odometer base plus tiny finite cover
  [
  B \leftarrow B+c \leftarrow B+c+d.
  ]

That is much better than a raw-coordinate story, and it is already stable enough to use as internal narrative.

---

## The one-sentence live project summary

We have already identified the active D5 normal form; the only live computational branch is to realize the carry sheet (c) admissibly.

When your current `045` run stabilizes, send the surviving observable family and the exact collision summary; that is the right handoff point for the proof branch.
