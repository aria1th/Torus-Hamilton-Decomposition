042 makes the next move much clearer.

The cleanest reading now is:

[
\text{D5 active branch} ;=; \text{grouped base } B=(s,u,v,\lambda,f)
;+; \text{tiny hidden sheet},
]

not raw (q), and not more controller design.

The most important thing I pulled out of the 042 data is this:

* trigger-level logic is already minimal:

  * exceptional fire descends to (B),
  * regular fire descends to (B+c) with
    [
    c=\mathbf 1_{{q=m-1}},
    ]
* but structure-level dynamics do **not** close on (B+c),
* and the saved cover extraction shows the missing lift is tiny:

  * over (B): fiber size at most (3),
  * over (B+c): fiber size at most (2).

That means the next honest object is not “admissible (q).”
It is:

[
\text{carry sheet} ;+; \text{residual binary noncarry sheet}.
]

That is the best current finite-cover formulation.

Two details from the 042 JSON make me think this is structural, not accidental:

First, the same sample nondeterministic grouped key on (B),
[
[4,2,2,2,\mathrm{regular}],
]
shows up across the checked moduli. So the hidden sheet is not just a last-step target glitch; it is part of the regular active dynamics.

Second, for (m=7,9,11), the sample maximal fiber over (B) occurs at the same grouped state
[
B=[5,1,6,4,\mathrm{regular}],
]
with (q)-values
[
{1,; m-2,; m-1}.
]
After adding the carry bit, that strongly suggests the residual ambiguity is the noncarry pair
[
{1,; m-2}.
]

I would treat that as a **serious conjectural pattern**, not yet a theorem.

So my current recommendation is to split the next work into two tightly related branches.

### 043A: admissible carry-bit realization

This is the next concrete local branch.

Goal:
realize admissibly the smallest verified positive lift
[
c=\mathbf 1_{{q=m-1}}.
]

Why this first:

* it is already enough for exact regular triggering,
* it keeps the controller logic minimal,
* and it is the smallest thing 042 proves is genuinely missing.

### 043B: finite-cover theorem extraction

This is the next structural / manuscript branch.

Goal:
extract the minimal deterministic lift over
[
B=(s,u,v,\lambda,f)
]
and decide whether the right theorem object is exactly:

* a 3-sheet cover over (B), or equivalently
* the carry bit plus a residual 2-sheet refinement over (B+c).

This is the branch that would give the clean d3/d4/d5 language.

So the theorem-shaped direction I would now push is:

[
\text{D3: odometer return map}
]
[
\text{D4: affine / second-return odometer}
]
[
\text{D5: grouped odometer or skew-odometer base + tiny finite cover.}
]

That is much better than a raw-coordinate formulation.

The exact things I would try to prove next are:

1. On the active union, the exceptional branch already closes on (B).
2. On the regular branch, trigger logic closes on (B+c).
3. The residual nondeterminism on (B+c) is genuinely only 2-sheet.
4. That residual 2-sheet can be coordinatized by a simple noncarry sheet variable (d), ideally with a direct dynamic meaning.
5. The full active branch can then be written as a skew-odometer base with finite-sheet lift, rather than as a raw-coordinate controller.

The most likely positive picture is:

[
B \longleftarrow B+c \longleftarrow B+c+d,
]
where

* (c) is the trigger-relevant carry sheet,
* (d) is the residual structural sheet,
* and full raw (q) is unnecessary.

I also drafted the next spec in that language:

[043 finite-cover / admissibility spec](sandbox:/mnt/data/d5_finite_cover_admissibility_043_spec.md)

My advice on compute budget: I would **not** spend GPU or huge generic search effort yet. The best next work is still exact combinatorial extraction:

* classify the residual 2-sheet over (B+c),
* then search only for admissible realization of (c),
* and only after that widen to realization of the residual sheet if needed.

So the frontier now looks like this:

**local branch:** realize the carry bit.
**structural branch:** prove D5 is a grouped skew-odometer plus a tiny finite cover.
