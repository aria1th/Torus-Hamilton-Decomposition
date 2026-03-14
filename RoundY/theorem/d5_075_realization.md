# D5 075 — realization integration on the dynamic bridge

## Scope

This note is for the active **realization integration** branch.

I do **not** try to prove the dynamic bridge theorem itself. I take as input the
accepted theorem-side phase-corner package and ask only:

> once the final bridge object exists as a deterministic exact quotient for
> current `epsilon4`, what follows automatically, and what extra hypothesis is
> still needed to recover the canonical clock?

So this note is meant to separate cleanly:

1. the abstract realization theorem,
2. the hypotheses that must come from the bridge theorem, and
3. the consequences that are then automatic.

I also do **not** assume that the old static decorated bridge `(beta,a,b)` is
final. The statement is written for the dynamic bridge
`(beta,q,sigma)` / `(beta,delta)` or any equivalent splice-compatible exact
quotient.

---

## Executive answer

The realization integration is now conceptually clean.

Let `X` be the theorem-side exact accessible object, with successor `F`, current
`epsilon4`, phase `kappa`, and canonical clock

\[
\beta_X := -\kappa \in \mathbb Z/m\mathbb Z.
\]

Let

\[
\pi : X \to Q
\]

be the final deterministic global bridge, where `Q` is the dynamic bridge state
space on the accessible image.

Then the right final theorem is:

> **If `Q` is deterministic and current `epsilon4` is exact on `Q`, then the
> short-corner detector descends automatically.**
>
> **If, in addition, every accessible bridge state has a future hit to the
> descended short-corner set, then the canonical clock descends uniquely by
> corner-time modulo `m`.**

More explicitly, define the visible short-corner set

\[
S_Q := \{q \in Q : (\bar\epsilon_4(q),\bar\epsilon_4(Gq))
= (\mathrm{flat},\mathrm{other}_{0010})\},
\]

where `G` is the induced bridge successor and
`epsilon4 = bar_epsilon4 ∘ pi`.
If every accessible `q` has some future hit to `S_Q`, then all such hit times
have one common residue modulo `m`; write that residue as `T_Q(q)`. The
canonical clock on `Q` is then forced to be

\[
\beta_Q(q) := T_Q(q) - 2 \pmod m,
\]

and it satisfies

\[
\beta_Q \circ \pi = \beta_X.
\]

So the answer to the `075` subquestions is:

- the exactness really needed is only **current `epsilon4` exactness on a
  deterministic quotient**;
- the extra nontrivial input is **recurrence of the descended short-corner set**,
  not uniqueness of a single short-corner state;
- the normalization is always **modulo `m`**, even if the bridge component is
  much longer than one bare `m`-cycle;
- without singleton short-corner structure, one still gets the full set-valued
  theorem and unique clock descent by corner-time residue.

---

## 1. The theorem-side package used here

Let `X` be the theorem-side exact accessible object, with deterministic
successor `F` and current event map

\[
\epsilon_4 : X \to E.
\]

I use only the accepted phase-corner data in the following form.

### Accepted phase-corner package

There is a phase map

\[
\kappa : X \to \mathbb Z/m\mathbb Z
\]

such that:

1. \(\kappa(Fx) = \kappa(x)+1 \pmod m\), equivalently
   \(\beta_X(Fx)=\beta_X(x)-1 \pmod m\) for
   \(\beta_X:=-\kappa\);
2. the theorem-side short-corner set is the two-step event signature
   \[
   S_X := \{x \in X : (\epsilon_4(x),\epsilon_4(Fx))
   = (\mathrm{flat},\mathrm{other}_{0010})\};
   \]
3. every short-corner state lies at phase \(\kappa = 2\), equivalently
   \(\beta_X = m-2\).

I do **not** use any singleton hypothesis for short corners.
The point is only that every short-corner hit has the same phase residue.

---

## 2. Abstract realization theorem for an exact deterministic bridge

Let

\[
\pi : X \to Q
\]

be a deterministic quotient with induced successor `G`, so that

\[
\pi \circ F = G \circ \pi.
\]

Assume only that current `epsilon4` factors through `Q`:

\[
\epsilon_4 = \bar\epsilon_4 \circ \pi
\]

for some readout \(\bar\epsilon_4 : Q \to E\).

This is the exactness hypothesis that must come from the bridge theorem.
No prior exactness of short-corner, future words, or the canonical clock is
assumed.

### Definition 2.1 (visible short-corner set)

Define

\[
S_Q := \{q \in Q : (\bar\epsilon_4(q),\bar\epsilon_4(Gq))
= (\mathrm{flat},\mathrm{other}_{0010})\}.
\]

### Lemma 2.2 (short-corner descends automatically)

Under determinism and current `epsilon4` exactness,

\[
S_X = \pi^{-1}(S_Q).
\]

#### Proof

For any `x \in X`, determinism gives \(\pi(Fx)=G\pi(x)\). Hence

\[
(\epsilon_4(x),\epsilon_4(Fx))
= (\bar\epsilon_4(\pi(x)),\bar\epsilon_4(G\pi(x))).
\]

So `x` is short-corner exactly when `pi(x)` satisfies the defining condition
for `S_Q`. ∎

### Theorem 2.3 (corner-time realization on the bridge)

Define also the theorem-side hit set

\[
H_X(x) := \{r \ge 0 : F^r x \in S_X\}.
\]

Assume, in addition, that every accessible state of `Q` has a future hit to
`S_Q`:

\[
H_Q(q) := \{r \ge 0 : G^r q \in S_Q\} \neq \varnothing
\qquad\text{for every accessible } q \in Q.
\]

Then:

1. every two elements of \(H_Q(q)\) are congruent modulo `m`;
2. therefore the residue
   \[
   T_Q(q) := [r]_m \in \mathbb Z/m\mathbb Z
   \qquad (r \in H_Q(q))
   \]
   is well defined;
3. `T_Q` satisfies
   \[
   T_Q(Gq) = T_Q(q)-1 \pmod m;
   \]
4. the canonical clock descends uniquely by
   \[
   \beta_Q(q) := T_Q(q)-2 \pmod m;
   \]
5. this descended clock satisfies
   \[
   \beta_Q \circ \pi = \beta_X,
   \qquad
   \beta_Q(Gq)=\beta_Q(q)-1 \pmod m.
   \]

#### Proof

Fix accessible `q = pi(x)`. By Lemma 2.2,

\[
H_Q(q)=H_X(x),
\]

so `H_Q(q)` is nonempty by hypothesis.

If \(r \in H_Q(q)\), then \(F^r x \in S_X\). By the phase-corner package,
short-corner states have \(\beta_X = m-2\), so

\[
\beta_X(F^r x) = m-2.
\]

But \(\beta_X\) drifts by `-1`, hence

\[
\beta_X(F^r x) = \beta_X(x) - r \pmod m.
\]

Therefore

\[
r \equiv \beta_X(x)+2 \pmod m.
\]

So all elements of `H_Q(q)` have the same residue modulo `m`, which proves the
well-definedness of `T_Q`.

The drift identity for `T_Q` is immediate from

\[
r \in H_Q(Gq) \iff r+1 \in H_Q(q).
\]

Now define \(\beta_Q := T_Q-2\). For `q = pi(x)` and any `r \in H_Q(q)`,

\[
\beta_X(x) \equiv r-2 \equiv T_Q(q)-2 = \beta_Q(q) \pmod m,
\]

so \(\beta_Q \circ \pi = \beta_X\). The drift law follows from that for `T_Q`.
Uniqueness on the accessible image is immediate from the identity
\(\beta_Q \circ \pi = \beta_X\). ∎

### Corollary 2.4 (what exactness is truly needed)

For the full realization theorem, the only bridge exactness needed is:

- deterministic successor on `Q`, and
- exactness of current `epsilon4` on `Q`.

No additional hypothesis is needed for:

- short-corner exactness,
- two-step event exactness,
- future `epsilon4`-word exactness,
- prior exactness of the canonical clock.

Those are automatic once current `epsilon4` is exact on a deterministic bridge.

---

## 3. Specialization to the dynamic bridge

The bridge theorem is expected to produce a dynamic bridge of the form

\[
Q_A = (\mathbb Z/m\mathbb Z) \times A,
\]

where `A` is the accessible boundary state space, parameterized for example by
`delta` or equivalently by `(q,sigma)`.

The deterministic successor has the bridge form

\[
G(\beta,\delta)
=
\begin{cases}
(\beta-1,\delta), & \beta \neq 0,\\
(m-1,T\delta), & \beta = 0,
\end{cases}
\]

for some boundary return map `T : A -> A`.

The bridge theorem is also expected to provide an exact current-event readout
\(\bar\epsilon_4\) on `Q_A`.

### 3.1 What the realization theorem uses from the dynamic bridge theorem

Only the following are needed.

#### Bridge inputs

1. **Deterministic bridge:**
   a quotient map \(\pi : X \to Q_A\) with \(\pi \circ F = G \circ \pi\).
2. **Current-event exactness:**
   \(\epsilon_4 = \bar\epsilon_4 \circ \pi\).
3. **Visible short-corner recurrence:**
   every accessible `q \in Q_A` has some future hit to `S_{Q_A}`.

That is enough for Theorem 2.3.

### 3.2 What is automatic once those hold

Once those three inputs are available, the following require no further bridge
work.

#### Automatic consequences

1. the short-corner detector descends:
   \(S_X = \pi^{-1}(S_{Q_A})\);
2. all future short-corner hits from one bridge state have a single residue
   modulo `m`;
3. the canonical clock descends uniquely by
   \[
   \beta_{Q_A}(q) = T_{Q_A}(q)-2 \pmod m;
   \]
4. any bridge-supplied coarse clock `beta` with the right drift and
   short-corner normalization must equal that descended canonical clock.

Indeed, if `beta_br` satisfies

\[
\beta_{br}(Gq)=\beta_{br}(q)-1 \pmod m
\]

and \(\beta_{br}=m-2\) on `S_{Q_A}`, then for any accessible `q` and any
future short-corner hit time

\[
r \in H_{Q_A}(q) := \{n \ge 0 : G^n q \in S_{Q_A}\},
\]

one has

\[
\beta_{br}(q) \equiv \beta_{br}(G^r q)+r \equiv (m-2)+r
\equiv T_{Q_A}(q)-2 = \beta_{Q_A}(q) \pmod m.
\]

So after the dynamic bridge theorem, the realization route does **not** need a
separate guessed clock.

---

## 4. Bridge-native form of the recurrence hypothesis

The only extra hypothesis in Theorem 2.3 is that each accessible bridge state
has a future short-corner hit.

For the dynamic bridge, this can be stated more intrinsically on the boundary
return system.

Assume the bridge theorem identifies a subset \(C \subseteq A\) such that

\[
S_{Q_A} = \{(m-2,\delta) : \delta \in C\}.
\]

Then recurrence on `Q_A` is equivalent to a boundary condition:

### Proposition 4.1 (boundary criterion for recurrence)

Under the dynamic bridge form above, the following are equivalent.

1. every accessible bridge state has a future hit to `S_{Q_A}`;
2. every forward `T`-orbit in `A` meets `C`.

#### Proof

Along any forward orbit in `Q_A`, the phase `beta = m-2` is encountered once
per `m`-step block. Between successive such encounters, the `delta` coordinate
advances by one application of `T`. Therefore the sequence of `delta`-values
seen at the `beta = m-2` cross-section is exactly a forward `T`-orbit. A future
short-corner hit occurs exactly when one of those `delta`-values lies in `C`.
∎

### Practical sufficient forms

Any of the following is enough to discharge recurrence.

1. each accessible `T`-cycle meets `C`;
2. each accessible bridge component contains at least one short-corner state;
3. in the full symbolic odometer case, `T` is a single cycle and `C` is
   nonempty.

So the realization theorem itself needs only recurrence, but the bridge theorem
can package that recurrence in whatever boundary form is most natural.

---

## 5. Concrete dynamic-bridge corollary

Suppose the dynamic bridge theorem is proved in the concrete readout form
suggested by the current checked picture:

\[
\bar\epsilon_4(\beta,\delta)=
\begin{cases}
\mathrm{carry\_jump}, & \beta=m-1,\\
\mathrm{wrap}, & \beta=0,\\
\mathrm{other}_{1000}, & \beta=m-2 \text{ and } a(\delta)=1,\\
\mathrm{other}_{0010}, & \beta=m-3 \text{ and } b(\delta)=1,\\
\mathrm{flat}, & \text{otherwise.}
\end{cases}
\]

Then the visible short-corner set is

\[
S_{Q_A}
= \{(m-2,\delta) : a(\delta)=0,\ b(\delta)=1\}.
\]

In the `(q,sigma)` parameterization supported by the checked bridge work, this
becomes

\[
S_{Q_A}
= \{(m-2,q,\sigma) : q \neq m-1,\ q+\sigma \equiv 1 \pmod m\}.
\]

So in the concrete dynamic bridge, the realization hypothesis reduces to:

> every accessible boundary orbit of `delta` meets the bridge short-corner set
> \(\{\delta : a(\delta)=0,\ b(\delta)=1\}\).

Once that is known, the canonical clock descends uniquely and equals the bridge
`beta` coordinate.

This is the clean point at which the realization branch meets the bridge
branch.

---

## 6. Normalization when the bridge is longer than one bare `m`-cycle

This is the place where the old wording needed correction.

If the accessible bridge component has length `m * L` with `L > 1`, the
canonical clock is **still only a mod-`m` object**.

It is **not** normalized by the full component length. The correct quantity is
always the residue modulo `m` of the future hitting times to the visible
short-corner set.

So the normalization is always

\[
\beta_Q(q)=T_Q(q)-2 \pmod m,
\]

not a clock modulo `mL`.

The extra bridge memory carried by `delta` changes which future short-corner hit
occurs, but it does not change the mod-`m` phase relation forced by the
phase-corner theorem.

---

## 7. What can be stated without uniqueness of a single short-corner state?

Everything needed for realization can be stated with the event-defined set
`S_Q`; one does **not** need a distinguished singleton short-corner state.

Without singleton structure, one still gets:

1. exact descent of the short-corner detector;
2. well-defined future-hit residue modulo `m` from each state;
3. unique descent of the canonical clock by corner-time;
4. identification of any bridge-supplied `beta` coordinate with that clock.

What singleton structure would give is only a more concrete presentation, for
example a unique next-hit time to one named state. That is a convenience, not a
logical requirement.

---

## 8. Final integrated theorem statement for the active branch

The clean final theorem statement to target is therefore the following.

### Theorem 8.1 (dynamic bridge + current-event exactness + short-corner recurrence)

Let `X` be the theorem-side exact accessible object with deterministic
successor `F`, current event `epsilon4`, and canonical clock
\(\beta_X=-\kappa \in \mathbb Z/m\mathbb Z\) from the phase-corner package.
Let

\[
\pi : X \to Q_A
\]

be a deterministic dynamic bridge quotient on the accessible image, where
`Q_A` is any splice-compatible bridge equivalent to `(beta,q,sigma)` or
`(beta,delta)`.

Assume:

1. **bridge determinism:** \(\pi \circ F = G \circ \pi\);
2. **current-event exactness:** \(\epsilon_4 = \bar\epsilon_4 \circ \pi\);
3. **short-corner recurrence:** every accessible state of `Q_A` has a future hit
   to
   \[
   S_{Q_A} = \{q : (\bar\epsilon_4(q),\bar\epsilon_4(Gq))
   = (\mathrm{flat},\mathrm{other}_{0010})\}.
   \]

Then:

1. the short-corner set descends exactly:
   \(S_X = \pi^{-1}(S_{Q_A})\);
2. for each accessible `q \in Q_A`, the set of future hit times to `S_{Q_A}`
   has a unique residue modulo `m`;
3. the canonical clock descends uniquely by
   \[
   \beta_{Q_A}(q)=T_{Q_A}(q)-2 \pmod m;
   \]
4. this descended clock satisfies
   \[
   \beta_{Q_A} \circ \pi = \beta_X;
   \]
5. if `Q_A` already carries a bridge coordinate `beta` with drift
   `beta -> beta-1` and short-corner normalization `beta = m-2` on
   `S_{Q_A}`, then that bridge coordinate is exactly the descended canonical
   clock.

### Interpretation

This theorem cleanly separates the remaining work.

- **What the bridge theorem must still supply:** a deterministic dynamic bridge,
  exactness of current `epsilon4`, and a recurrence statement for the visible
  short-corner set.
- **What becomes automatic once that is supplied:** short-corner descent,
  canonical-clock descent, uniqueness, and the identification of the bridge
  `beta` with the theorem-side canonical clock.

So the live realization question is no longer “invent a clock.”
It is only:

> does the final dynamic bridge theorem supply the exact current-event quotient
> and the needed visible short-corner recurrence?

If yes, realization is done.

---

## 9. What remains open after this integration

This note does **not** close the bridge branch itself.
The remaining open items are exactly bridge-side.

1. prove the dynamic bridge theorem uniformly from the D5 structure;
2. package the correct accessible boundary state space `A`;
3. prove the concrete short-corner recurrence criterion on `A`;
4. optionally show that in the final bridge, recurrence is automatic because the
   accessible boundary return system is one cycle or because each accessible
   cycle meets the bridge short-corner subset.

Those are no longer realization-theorem gaps. They are bridge-theorem gaps.

## Bottom line

The realization integration problem is now reduced to one clean statement:

> **deterministic dynamic bridge + current `epsilon4` exactness + visible
> short-corner recurrence**
>
> implies
>
> **exact short-corner descent and unique canonical-clock descent by corner-time
> modulo `m`.**

That is the right final interface between the theorem-side phase-corner package
and the dynamic boundary-odometer bridge.
