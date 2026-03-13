I read only `d5_063_route_organization.md`, and I think the negative branch can be sharpened to one clean theorem: not merely “bounded horizon fails,” but “any bounded quotient of the active odometer section already needs at least (m) states to recover carry.” That is exactly the bounded-quotient / odometer-factor direction the note is pointing at.  

## The right negative theorem

The note says the theorem side should look like “an odometer with one corner,” while the no-go side should aim for a bounded-quotient collapse rather than a vague impossibility result.

The clean form is this.

### Proposition (cyclic section lower bound)

Assume that for each odd (m) there is a return section
[
\Sigma_m={x_0,\dots,x_{m-1}}
]
on the active branch such that the first-return map is
[
R_m(x_q)=x_{q+1}\qquad(\bmod m),
]
and the carry label on that section is
[
c_m(x_q)=\mathbf 1_{{q=m-1}}.
]

Suppose a candidate local/admissible mechanism induces a finite quotient
[
\pi_m:\Sigma_m\to Q
]
with an induced return map (\widehat R_m:Q\to Q) and readout (\chi:Q\to{0,1}) such that
[
\pi_m\circ R_m=\widehat R_m\circ \pi_m,
\qquad
c_m=\chi\circ \pi_m.
]
Then
[
|Q|\ge m.
]

### Proof

Assume (\pi_m(x_i)=\pi_m(x_j)) with (0\le i<j\le m-1).
Let
[
n:=m-1-j.
]
Then by semiconjugacy,
[
\pi_m(R_m^n x_i)=\widehat R_m^n\pi_m(x_i)=\widehat R_m^n\pi_m(x_j)=\pi_m(R_m^n x_j).
]
But
[
R_m^n x_j=x_{m-1},
\qquad
R_m^n x_i=x_{m-1-(j-i)}\neq x_{m-1}.
]
Applying (\chi),
[
c_m(x_{m-1-(j-i)})=\chi(\pi_m(R_m^n x_i))
=\chi(\pi_m(R_m^n x_j))
=c_m(x_{m-1})=1.
]
This is impossible because (m-1-(j-i)\neq m-1), so the left-hand side is (0). Hence all
[
\pi_m(x_0),\dots,\pi_m(x_{m-1})
]
are distinct, and therefore (|Q|\ge m). ∎

---

## Why this is the right no-go statement

This proposition is the exact odometer-factor obstruction suggested in the note. The note’s negative branch says:

* define the intended local/admissible class,
* show it collapses to bounded grouped transition/reset data or a finite quotient of the active odometer word,
* then use the persistent witness family to kill that quotient. 

The proposition above gives the “kill that quotient” step in a much cleaner form than a bounded-horizon argument. It says:

> once you really have a cyclic (q)-section with carry equal to one distinguished residue, any factor that still computes carry must have at least (m) states.

So a bounded quotient independent of (m) is impossible.

---

## What this buys you for the intended local class

Now define the intended admissible/local mechanism as something with:

* a controller state set (S) of size bounded independently of (m),
* deterministic update along the active branch from bounded grouped transition/reset data,
* a current readout of (c).

Then on any section (\Sigma_m), the controller state induces exactly such a quotient:
[
\pi_m(x)=\text{controller state at }x.
]
The induced first-return map on controller states is (\widehat R_m), and the controller’s readout is (\chi).

So the proposition immediately yields:

### Corollary

Any admissible/local mechanism whose effective state space is bounded independently of (m) cannot recover the carry sheet (c) on all odd (m), provided the active branch contains the cyclic section above.

This is the bounded-quotient collapse theorem in the form I would now target.

---

## What still has to be proved in D5

The remaining work is very specific.

### 1. Prove the section exists

You need one explicit active-branch section (\Sigma_m) on which the hidden residue runs through an (m)-cycle. Under the note’s “odometer with one corner” picture, this is exactly the natural thing to extract from the structural branch.

### 2. Put carry on that section

You need
[
c_m(x_q)=\mathbf 1_{{q=m-1}}
]
on that section. That is the single marked residue.

### 3. Formalize the local class

You need one precise definition that guarantees every mechanism in the class induces a bounded quotient of the section dynamics. That is the real reduction lemma the note asks for. 

Once those three pieces are written, the no-go branch is basically done.

---

## How this fits the witness family

The earlier witness family is still useful, but now as a shadow of the stronger theorem.

What the witness pair already shows is:

* same grouped base,
* same current event class,
* very long identical future flat/nonflat prefix,
* opposite carry.

That kills bounded future-horizon codings.

The section proposition upgrades that from:

> “you cannot do this with bounded lookahead”

to:

> “you cannot do this with any bounded quotient at all.”

So the witness pair is the first visible symptom; the cyclic-section lower bound is the real theorem.

---

## The conceptual payoff

This also clarifies the positive branch.

If the constructive route through transported (\rho) or (\alpha=\rho-u) is the real solution, then it cannot live inside a bounded-state quotient class. It must genuinely carry an (m)-valued residue. That matches the note’s split very well:

* positive branch: transport source residue,
* negative branch: rule out any bounded quotient that tries to fake that transport.

So my recommendation is:

**Write the negative branch as a conditional theorem with exactly two inputs:**

1. a cyclic active section (R_m:x_q\mapsto x_{q+1}),
2. a bounded-quotient reduction for the intended local class.

Then the proof is the one-page proposition above.

