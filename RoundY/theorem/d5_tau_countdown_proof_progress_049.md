# D5 Tau Countdown / Anticipation Proof Progress after 048

## Scope

This note consolidates the checked theorem chain from `044` through `048` and recasts the open problem in proof form.
The manuscript emphasis should be:

- `046` as the conceptual theorem,
- `047` as the boundary sharpening,
- `048` as the internal-dynamics theorem turning the hidden future datum into a countdown carrier.

The guiding point is now clean:

> the carry sheet is not a current grouped-state observable; it is a one-sided anticipation datum carried by an exact countdown/reset mechanism on the checked active best-seed branch.

Throughout,
\[
B=(s,u,v,\lambda,f),\qquad \lambda=\text{layer},\qquad f\in\{\mathrm{regular},\mathrm{exceptional}\}.
\]
Also
\[
c=\mathbf 1_{\{q=m-1\}},\qquad d=\mathbf 1_{\{U^+\ge m-3\}}.
\]

The checked moduli are
\[
m\in\{5,7,9,11\}.
\]

---

## I. Frozen checked theorem chain

### Theorem A (finite-cover normal form; `044` with `043` input)
On the checked active best-seed branch, the carry mechanism factors through the finite-sheet normal form
\[
B \leftarrow B+c \leftarrow B+c+d.
\]
More precisely:

1. exceptional fire already descends to `B`;
2. regular fire descends to `B+c`;
3. deterministic active evolution closes on `B+c+d`;
4. `d` is canonically coordinatized by the binary anticipation sheet
   \[
   d=\mathbf 1_{\{U^+\ge m-3\}}.
   \]

Interpretation: D5 is already best read as grouped skew-odometer base plus a tiny finite cover.

### Theorem B (first carry no-go; `045`)
No observable from the first admissible current-edge / short-transition / low-cardinality gauge catalogs realizes the carry sheet `c` exactly on the checked active branch. In particular the tested catalogs factoring through
\[
B,\qquad B\to B_{\mathrm{next}},\qquad B\to B_{\mathrm{next}}\to B_{\mathrm{next2}}
\]
all fail.

Interpretation: the missing datum is not another current grouped-state feature of the first natural kind.

### Theorem C (carry as future grouped-transition event; `046`)
The carry sheet `c` is already an exact future grouped-transition event on the checked active branch.

The checked minimal horizons are:
\[
H_{dn}=m-3,
\qquad
H_B=m-2.
\]
Equivalently, there is an exact future signature of the form
\[
B+\tau+\eta,
\]
where:

- `tau` is the initial flat-run length for the grouped-delta event
  \[
  dn=(0,0,0,1),
  \]
- `eta` is the first nonflat grouped-delta event.

This is the conceptual theorem: the carry sheet is already an anticipation datum on the grouped base.

### Theorem D (boundary sharpening; `047`)
All ambiguity in `B+tau` lies at the boundary `tau=0`.
On the checked range, the boundary class is genuinely 3-class minimal:
\[
\{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]
The first exact checked-range quotient is
\[
B+\min(\tau,8)+\epsilon_4,
\]
with `epsilon4` the current grouped-delta event class.
Equivalently, the first exact checked-range transition-sheet coding is
current `B`, current `epsilon4`, and the next seven future flat/nonflat bits after the current step.

Manuscript role: this is a sharpening of Theorem C, not the final conceptual form.

### Theorem E (countdown carrier law; `048`)
On the checked active nonterminal branch, `tau` has exact internal dynamics as a countdown carrier.

1. Whenever `tau>0`,
   \[
   \tau' = \tau-1.
   \]
2. All nontrivial dynamics are confined to the boundary `tau=0`.
3. On the boundary:
   - `wrap` resets to `0`;
   - `carry_jump` resets exactly as a function of `(s,v,\lambda)`;
   - `other` resets exactly as a function of `(s,u,\lambda)`.
4. Equivalently, the full next-`tau` map is exact on
   \[
   (\tau,\epsilon_4,s,u,v,\lambda).
   \]
5. No smaller current `B`-subset with `epsilon4` is exact on the boundary.

Checked minimality on the boundary:

- globally with `epsilon4`, the minimal exact current quotient is
  \[
  (s,u,v,\lambda),
  \]
- on the `carry_jump` branch, the minimal exact quotient is
  \[
  (s,v,\lambda),
  \]
- on the `other` branch, the minimal exact quotient is either
  \[
  (s,u,v)
  \]
  or
  \[
  (s,u,\lambda).
  \]

Interpretation: the hidden datum from `046` is not an opaque future window anymore. It is an exact countdown/reset carrier.

---

## II. Conceptual corollary to emphasize in the manuscript

### Corollary F (carry sheet as anticipation datum)
On the checked active best-seed branch, the carry sheet is a one-sided anticipation datum over the grouped base.
More precisely, it is mediated by a countdown carrier `tau` with piecewise reset micro-law:

- free propagation by decrement while `tau>0`;
- reset on the boundary `tau=0` by the current-event class `epsilon4` together with a tiny current grouped-state quotient.

This is the right conceptual bridge between `044` and the local/admissibility problem.

The recommended manuscript hierarchy is therefore:

1. finite-cover normal form (`044`),
2. carry-as-anticipation theorem (`046`),
3. boundary sharpening (`047`),
4. countdown carrier law (`048`).

---

## III. What is now actually missing

The remaining gap is no longer controller design.
The remaining gap is one of the following two statements.

### Open Theorem P (positive route)
There exists an admissible/local coding of the countdown carrier `tau` on the active branch, equivalently an admissible/local coding of its boundary reset law together with internal decrement.

### Open Theorem N (negative route)
The intended admissible/local mechanism class cannot code `tau`.
Equivalently, no mechanism in that class can realize the carry sheet `c`, because any such mechanism would have to support the exact countdown/reset structure from Theorem E.

So the proof problem is now well-posed.

---

## IV. Strongest proof reduction now available

Theorem E gives a much sharper reduction than we had before.

### Reduction principle
To realize `tau`, it is not necessary to realize a whole future window from scratch.
It is enough to realize:

1. an internal counter state ranging over the checked countdown values, and
2. the boundary reset map
   \[
   R(\epsilon_4,s,u,v,\lambda)
   \]
   defined at `tau=0` by
   \[
   R(\mathrm{wrap},\cdot)=0,
   \]
   \[
   R(\mathrm{carry\_jump},s,u,v,\lambda)=R_{cj}(s,v,\lambda),
   \]
   \[
   R(\mathrm{other},s,u,v,\lambda)=R_{oth}(s,u,\lambda)
   \quad\text{(or equivalently via }(s,u,v)\text{ on the checked data).}
   \]

After that, propagation is exact by the deterministic update
\[
\tau' = \begin{cases}
\tau-1,&\tau>0,\\
R(\epsilon_4,s,u,v,\lambda),&\tau=0.
\end{cases}
\]

This is the cleanest proof-side recoding of the local problem.

### Consequence
The next positive theorem need not construct an admissible coding of the full future signature from `046`.
It only needs to construct an admissible coding of the boundary reset micro-law plus an internal countdown carrier.

Conversely, the next negative theorem can focus on the impossibility of coding the reset map in the intended local class.

---

## V. Suggested theorem / lemma sequence for a paper draft

### Proposition 1 (checked finite-cover normal form)
State Theorem A.

### Proposition 2 (checked carry anticipation theorem)
State Theorem C.
This is the conceptual proposition.

### Proposition 3 (checked boundary sharpening)
State Theorem D as a refinement of Proposition 2.
Make clear that the checked-range quotient `min(tau,8)` is evidence, not the canonical final form.

### Proposition 4 (checked countdown carrier law)
State Theorem E.

### Corollary 5 (reduction to boundary reset coding)
On the checked branch, coding the carry sheet is equivalent to coding the countdown carrier with exact piecewise reset law.

This is the proposition that should drive the next local/admissibility section.

---

## VI. Proof route from here

### Positive route
Try to prove an admissible coding theorem for the boundary reset map.
If successful, the rest of the carrier is internal and deterministic.
That would turn the local branch into:

- an admissible boundary reset observable,
- a countdown carrier state,
- exact reconstruction of `tau`,
- exact reconstruction of `c`.

### Negative route
Try to prove a reduction lemma of the form:

> every intended admissible/local coding of the carry mechanism factors through a bounded-depth grouped transition sheet or a bounded current-edge reset catalog.

Combined with `045` and the 046/047/048 witness families, that would yield a real no-go theorem.

At present this reduction lemma is the main proof gap on the negative side.

---

## VII. Exact status labels

- `[C]` checked on `m=5,7,9,11`:
  - finite-cover normal form `B <- B+c <- B+c+d`
  - first carry no-go for the initial admissible catalogs
  - carry as exact future grouped-transition event
  - boundary 3-class sharpening
  - countdown carrier law and minimal current reset quotients

- `[H]` theorem-shaped but not yet proved uniformly:
  - the active branch admits a canonical anticipation-carrier formulation for all odd `m`
  - the local problem reduces canonically to admissible coding of the reset micro-law

- `[O]` open:
  - admissible/local coding of `tau`
  - or an impossibility theorem for the intended local mechanism class.

---

## VIII. Recommended immediate proof emphasis

If the manuscript has to choose one conceptual theorem right now, it should be `046`.
If it has to choose one structural sharpening, it should be `048`.

`047` should be presented as the boundary refinement that first exposes the role of `epsilon4`, but not as the final canonical form.

The shortest honest summary is:

> On the checked active D5 best-seed branch, the carry sheet is a one-sided anticipation datum on the grouped base; the hidden future parameter is an exact countdown carrier with a tiny current-state reset law.
