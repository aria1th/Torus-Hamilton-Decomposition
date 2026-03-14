The handoff makes the right shift: on the clock side, the job is no longer to invent a controller, but to expose the already existing lifted clock (\beta=-\Theta) on the intended local/admissible quotient. In the theorem gauge this is the same phase as (\kappa), with (\beta=-\kappa \pmod m) on the active branch. 

## 1. The clean object to build: the canonical clock realization

Fix odd (m). Let

[
(\widetilde X_m,\widetilde T)
]

be the exact lifted active corridor, and let

[
L_m:\widetilde X_m\to Y_m
]

be the projection to the intended local/admissible object, with deterministic quotient dynamics

[
L_m\circ \widetilde T = F_m\circ L_m.
]

Let the canonical lifted clock be

[
\widetilde\beta_m:\widetilde X_m\to \mathbb Z/m\mathbb Z,
\qquad
\widetilde\beta_m(\widetilde T x)=\widetilde\beta_m(x)-1.
]

This is the lifted (\beta=-\Theta) from the handoff. 

Now define the **clock realization over (Y_m)** by

[
\mathcal R_m
:=
{(y,b)\in Y_m\times \mathbb Z/m\mathbb Z:\exists x\in \widetilde X_m,\ L_m(x)=y,\ \widetilde\beta_m(x)=b}.
]

Equip it with the induced update

[
\widehat F_m(y,b):=(F_m(y),,b-1).
]

Then the map

[
\Pi_m:\widetilde X_m\to \mathcal R_m,
\qquad
\Pi_m(x):=(L_m(x),\widetilde\beta_m(x))
]

satisfies

[
\Pi_m\circ \widetilde T=\widehat F_m\circ \Pi_m.
]

So (\mathcal R_m) is always an exact realization of the canonical clock over the intended quotient.

That gives a very clean reformulation:

> **Descent** asks whether (\mathcal R_m\to Y_m) collapses to a graph.
> **Realization** is the object (\mathcal R_m) itself.

---

## 2. Necessary and sufficient condition for descent

Write

[
Y_m^*:=L_m(\widetilde X_m)
]

for the accessible part of the intended quotient, and for each (y\in Y_m^*) define the phase fiber

[
P_m(y):={b\in \mathbb Z/m\mathbb Z:(y,b)\in \mathcal R_m}.
]

Then the exact descent question is equivalent to asking whether every (P_m(y)) is a singleton.

### Theorem D1

The following are equivalent.

1. There exists a descended clock
   [
   \beta_m:Y_m^*\to \mathbb Z/m\mathbb Z
   ]
   such that
   [
   \beta_m\circ L_m=\widetilde\beta_m.
   ]

2. For every (y\in Y_m^*),
   [
   |P_m(y)|=1.
   ]

3. The projection
   [
   \rho_m:\mathcal R_m\to Y_m^*,\qquad \rho_m(y,b)=y
   ]
   is bijective.

4. (\mathcal R_m) is the graph of a function (Y_m^*\to \mathbb Z/m\mathbb Z).

### Proof

If (\beta_m) exists, then every lift of the same (y) has the same phase, so (P_m(y)={\beta_m(y)}). That gives (1\Rightarrow 2).

If every (P_m(y)) is a singleton, define (\beta_m(y)) to be its unique element. Then by construction (\beta_m\circ L_m=\widetilde\beta_m). So (2\Rightarrow 1).

Statements (2,3,4) are just different ways of saying the same thing. ∎

So the positive branch has been reduced to a crisp test:

[
\text{Does each accessible local state }y\text{ support exactly one lifted phase?}
]

---

## 3. The universal property of the realization

This is the other important theorem.

### Theorem D2

(\mathcal R_m) is the coarsest accessible realization of the canonical clock over (Y_m).

More precisely, suppose (Z_m) is any system with:

* update (G_m:Z_m\to Z_m),
* visible projection (v_m:Z_m\to Y_m),
* clock (\beta_{Z,m}:Z_m\to \mathbb Z/m\mathbb Z),
* accessible map (j_m:\widetilde X_m\to Z_m),

such that

[
j_m\circ \widetilde T = G_m\circ j_m,
\qquad
v_m\circ j_m=L_m,
\qquad
\beta_{Z,m}\circ j_m=\widetilde\beta_m.
]

Then on the accessible exact part (Z_m^*:=j_m(\widetilde X_m)), the map

[
\Phi_m:Z_m^*\to \mathcal R_m,
\qquad
\Phi_m(z):=(v_m(z),\beta_{Z,m}(z))
]

is a surjective factor map commuting with dynamics.

### Proof

Take (z=j_m(x)). Then

[
\Phi_m(z)
=========

# (v_m(j_m(x)),\beta_{Z,m}(j_m(x)))

(L_m(x),\widetilde\beta_m(x))
\in \mathcal R_m.
]

So (\Phi_m) is well-defined on (Z_m^*). It is surjective because every ((y,b)\in \mathcal R_m) has the form ((L_m(x),\widetilde\beta_m(x))), hence equals (\Phi_m(j_m(x))). And

[
\Phi_m(G_m z)
=============

# (v_m(G_m z),\beta_{Z,m}(G_m z))

# (F_m(v_m z),\beta_{Z,m}(z)-1)

\widehat F_m(\Phi_m(z)).
]

So (\Phi_m) is a factor map. ∎

This is the right realization statement: even if descent fails, there is still a canonical exact object carrying the clock, namely (\mathcal R_m).

---

## 4. Phase-set propagation

Now for the part that makes descent practical.

### Lemma D3

For accessible (y\in Y_m^*),

[
P_m(F_m y)\supseteq P_m(y)-1.
]

If every accessible lift of (F_m y) has an accessible predecessor lift of (y) — in particular on an interior point of a chain, or everywhere on a cycle — then in fact

[
P_m(F_m y)=P_m(y)-1.
]

### Proof

If (b\in P_m(y)), pick (x) with (L_m(x)=y) and (\widetilde\beta_m(x)=b). Then

[
L_m(\widetilde T x)=F_m(y),
\qquad
\widetilde\beta_m(\widetilde T x)=b-1,
]

so (b-1\in P_m(F_m y)). That gives the inclusion.

For the reverse inclusion, take (b'\in P_m(F_m y)) with witness (x'). If (x') has a predecessor (x) with (\widetilde T x=x') and (L_m(x)=y), then (b'+1\in P_m(y)). ∎

So along the accessible chain/cycle, the phase fibers just shift by (-1). Their size is constant wherever predecessor/successor transport is available.

That yields the key constructive corollary.

### Corollary D4

Assume the accessible quotient (Y_m^*) is a single chain or cycle under (F_m). If there is one anchor state (y_{\mathrm{anc}}\in Y_m^*) with

[
|P_m(y_{\mathrm{anc}})|=1,
]

then

[
|P_m(y)|=1
\quad\text{for every }y\in Y_m^*.
]

Hence the canonical clock descends on all of (Y_m^*).

So to prove descent, it is enough to expose the lifted phase at one anchor on the accessible orbit.

---

## 5. Explicit anchor formula

This gives the constructive realization of the descended clock.

Assume (A\subseteq Y_m^*) is an anchor set such that every accessible orbit segment hits (A) in a unique time, and on (A) the phase is already known exactly by a local function

[
b_A:A\to \mathbb Z/m\mathbb Z.
]

If (n(y)) is the first time with (F_m^{n(y)}y\in A), then define

[
\beta_m(y):=b_A(F_m^{n(y)}y)+n(y)\pmod m.
]

Because the clock decreases by (1) each step, this is exactly the unique descended phase.

Indeed,

[
\beta_m(F_m^{n(y)}y)=\beta_m(y)-n(y)=b_A(F_m^{n(y)}y).
]

So the positive route can be stated very sharply:

> Find one local anchor where the lifted phase is visible, and show every accessible local state reaches it in a unique time.

That is the constructive descent theorem.

---

## 6. Once (\beta) descends, the whole theorem package descends

The handoff says compute should validate exact readout of

[
q,\ c,\ \epsilon_4,\ \tau,\ \text{next}_\tau
]

from ((B,\beta)), and where available also (\text{next}_B). 

So suppose on the lifted corridor each theorem-side quantity (g) has the form

[
g(x)=G(B(x),\widetilde\beta_m(x)).
]

Then:

* on the realization (\mathcal R_m), define
  [
  \widehat g(y,b):=G(B(y),b);
  ]
* if descent holds, define on (Y_m^*)
  [
  g_Y(y):=G(B(y),\beta_m(y)).
  ]

Thus **realizing the clock is enough to realize the entire exact controller**.

That is why the handoff is right to treat the clock route as the remaining live frontier. 

---

## 7. What this means for D5 specifically

The clean D5 program for descent/realization is now:

1. Fix the intended local/admissible quotient
   [
   L_m:\widetilde X_m\to Y_m.
   ]

2. Build the canonical realization
   [
   \mathcal R_m={(L_m(x),\widetilde\beta_m(x))}.
   ]

3. Compute or prove the phase fibers
   [
   P_m(y).
   ]

4. Show one anchor fiber is singleton.

Then Corollary D4 gives descent on the full accessible chain/cycle.

The natural candidate anchors are exactly the theorem-side marked places: the carry/corner/short-reset markers from the phase-corner package. The handoff already puts those structures in the theorem package, and it also says compute should validate cycle-vs-chain and ((B,\beta)) exactness/drift rather than reopen generic search. 

So the practical target is no longer “search for a controller.” It is:

[
\text{compute }\mathcal R_m\text{ and prove }|P_m(y)|=1\text{ on one anchor.}
]

---

## 8. The unified picture

This also clarifies how descent and rigidity fit together:

* **Descent/realization:** the canonical realized object is (\mathcal R_m); descent means (\mathcal R_m) is a graph over (Y_m).
* **Rigidity/necessity:** any exact realization must already carry the same canonical clock, hence factor through the corresponding realized object on its accessible exact part.

So both sides are really about the same object.

Scope: I used only the `067` concentrated handoff. What remains unverified from that handoff alone is which exact intended quotient (Y_m) you want, and which anchor in that quotient exposes the phase as a singleton.
