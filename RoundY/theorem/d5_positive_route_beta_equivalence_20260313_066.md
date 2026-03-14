# D5 positive route: beta-controller equivalence and straightening lemma

This note pushes the positive route one step further.

It does **not** claim a full uniform proof of the phase-corner theorem or a full
local realizability proof for the beta-controller.  What it does prove is:

1. the phase-corner theorem and the beta-controller theorem are the same
   machine written in two gauges;
2. once an `alpha` carrier is transported, the straightening to `beta` is
   essentially automatic;
3. on the frozen `047` checked transition data, the whole beta normal form is
   exact with zero exceptions.

## 1. Setup

Work on the active best-seed branch for odd `m >= 5`.

Write
\[
B=(s,u,v,\lambda,f),
\qquad
J := 1_{\{\epsilon_4=\mathrm{carry\_jump}\}},
\qquad
\kappa := q+s+v+\lambda \pmod m.
\]

On the constructive side also write
\[
\alpha := \rho-u,
\qquad
\beta := \alpha-(s+v+\lambda)-J.
\]

From the checked constructive formula
\[
q \equiv -\alpha + J \pmod m,
\]
we get the exact algebraic identities
\[
\beta \equiv -\kappa \pmod m,
\qquad
q \equiv -\beta-s-v-\lambda \pmod m,
\qquad
c = 1_{\{\beta+s+v+\lambda=1\}}.
\]

So `beta` is not an unrelated constructive coordinate. It is exactly the
negative of the theorem-side phase.

## 2. Beta normal form of the phase-corner theorem

### Theorem A (phase-corner theorem => beta-controller normal form)
Assume the phase-corner theorem in the form:

1. `kappa' = kappa + 1 mod m`;
2. the current event scheduler is
   \[
   \kappa=0 \Rightarrow \mathrm{wrap},
   \qquad
   \kappa=1 \Rightarrow \mathrm{carry\_jump},
   \]
   \[
   \kappa=2 \Rightarrow
   \begin{cases}
   \mathrm{other}_{1000},& c=1,\\
   \mathrm{flat},& c=0,
   \end{cases}
   \qquad
   \kappa=3 \Rightarrow
   \begin{cases}
   \mathrm{other}_{0010},& (c=0\ \&\ s=2)\ \text{or}\ (c=1\ \&\ s\neq 2),\\
   \mathrm{flat},& \text{otherwise},
   \end{cases}
   \]
   and phases `4,...,m-1` are flat;
3. among flat states, the only short reset occurs at `(kappa,s)=(2,2)`.

Then with
\[
\beta := -\kappa \pmod m,
\]
the active machine is exactly:

#### Clock law
\[
\beta' = \beta-1 \pmod m.
\]

#### Current readouts
\[
q \equiv -\beta-s-v-\lambda \pmod m,
\qquad
c = 1_{\{\beta+s+v+\lambda=1\}}.
\]

#### Event scheduler in beta gauge
\[
\beta=0 \Rightarrow \mathrm{wrap},
\qquad
\beta=m-1 \Rightarrow \mathrm{carry\_jump},
\]
\[
\beta=m-2 \Rightarrow
\begin{cases}
\mathrm{other}_{1000},& c=1,\\
\mathrm{flat},& c=0,
\end{cases}
\]
\[
\beta=m-3 \Rightarrow
\begin{cases}
\mathrm{other}_{0010},& (c=0\ \&\ s=2)\ \text{or}\ (c=1\ \&\ s\neq 2),\\
\mathrm{flat},& \text{otherwise},
\end{cases}
\]
and every other `beta` fiber is flat.

#### Countdown readout
\[
\tau=0 \quad (\epsilon_4\neq \mathrm{flat}),
\]
and on the flat branch,
\[
\tau=
\begin{cases}
1,& (\beta,s,c)=(m-2,2,0),\\
\beta,& \text{otherwise}.
\end{cases}
\]

#### Reset/update readout
\[
\tau'=
\begin{cases}
\tau-1,& \epsilon_4=\mathrm{flat},\\
0,& \epsilon_4=\mathrm{wrap},\\
0,& \epsilon_4=\mathrm{carry\_jump}\ \&\ c=1,\\
1,& \epsilon_4=\mathrm{carry\_jump}\ \&\ c=0\ \&\ s=1,\\
m-2,& \epsilon_4=\mathrm{carry\_jump}\ \&\ c=0\ \&\ s\neq 1,\\
m-3,& \epsilon_4=\mathrm{other}_{1000}\ \&\ s=1,\\
0,& \epsilon_4=\mathrm{other}_{1000}\ \&\ s\neq 1,\\
m-4,& \epsilon_4=\mathrm{other}_{0010}.
\end{cases}
\]

#### Current-state next-B update
If `e_s,e_u,e_v,e_\lambda` are the standard basis increments on the first four
coordinates of `B`, then
\[
B'=
\begin{cases}
B,& \beta=0,\\
B+e_s+e_u,& \beta=m-1,\\
B+e_s,& \beta=m-2\ \&\ c=1,\\
B+e_v,& \beta=m-3\ \&\big((c=0\ \&\ s=2)\ \text{or}\ (c=1\ \&\ s\neq 2)\big),\\
B+e_\lambda,& \text{otherwise},
\end{cases}
\]
with all residues taken mod `m` and family unchanged.

#### Proof
Everything is a direct translation of the phase-corner theorem by the gauge
change `beta = -kappa`.

- `beta' = beta-1` is immediate from `kappa' = kappa+1`.
- The event scheduler is exactly the scheduler in `kappa`, rewritten using
  `kappa \equiv -beta`.
- The flat countdown law
  \[
  \tau = 1 \text{ at } (\kappa,s)=(2,2),
  \qquad
  \tau = m-\kappa \text{ otherwise,}
  \]
  becomes
  \[
  \tau = 1 \text{ at } (\beta,s,c)=(m-2,2,0),
  \qquad
  \tau = \beta \text{ on all other flat states.}
  \]
- The branchwise reset values are just the same `wrap`, `carry_jump`,
  `other_1000`, `other_0010` formulas viewed in the beta gauge.
- The `B`-update rule is the event scheduler plus the defining increments of the
  event types.

So the phase-corner theorem is already a beta-controller theorem in disguise.

### Theorem B (beta-controller normal form => phase-corner theorem)
Conversely, assume there is a controller variable `beta` with the properties
listed in Theorem A. Define
\[
\kappa := -\beta \pmod m.
\]
Then the full phase-corner theorem follows.

#### Proof
Again this is immediate translation.  The beta clock law gives
\[
\kappa' = \kappa+1,
\]
and the beta scheduler translates back to the `kappa` scheduler.  The beta
countdown/readout formulas translate back to the phase-corner countdown law and
therefore to the usual reset formulas.

### Consequence
The theorem route and the positive beta-controller route are **not two different
machines**.  They are the same active branch written in the gauges
\[
\kappa 
\qquad\text{and}\qquad
\beta=-\kappa.
\]

So any proof of one automatically yields the other.

## 3. Straightening lemma: alpha transport is enough

The previous theorem still uses the theorem-side phase machine.  The next
question is: if one could transport `alpha`, how much work remains to obtain the
unit-drift `beta` clock?

The answer is: very little.

### Theorem C (alpha-to-beta straightening lemma)
Assume on the active branch that:

1. `alpha` is transported by
   \[
   \alpha' = \alpha - J \pmod m,
   \qquad J=1_{\{\epsilon_4=\mathrm{carry\_jump}\}};
   \]
2. the event types have the standard `B`-increments
   \[
   \mathrm{wrap}: (\Delta s,\Delta u,\Delta v,\Delta\lambda)=(0,0,0,0),
   \]
   \[
   \mathrm{carry\_jump}: (1,1,0,0),
   \qquad
   \mathrm{other}_{1000}: (1,0,0,0),
   \qquad
   \mathrm{other}_{0010}: (0,0,1,0),
   \qquad
   \mathrm{flat}: (0,0,0,1);
   \]
3. carry-jump occurs exactly one step after wrap and nowhere else:
   \[
   J' = 1_{\{\epsilon_4=\mathrm{wrap}\}}.
   \]

Then the straightened carrier
\[
\beta := \alpha-(s+v+\lambda)-J
\]
satisfies the unit-drift law
\[
\beta' = \beta-1 \pmod m.
\]

#### Proof
By definition,
\[
\beta'-\beta
= (\alpha'-\alpha) - \big((s'+v'+\lambda')-(s+v+\lambda)\big) - (J'-J).
\]
From (1),
\[
\alpha'-\alpha = -J.
\]
From the event increments in (2),
\[
(s'+v'+\lambda')-(s+v+\lambda)=
\begin{cases}
0,& \epsilon_4=\mathrm{wrap},\\
1,& \epsilon_4\neq \mathrm{wrap}.
\end{cases}
\]
From (3),
\[
J'=
\begin{cases}
1,& \epsilon_4=\mathrm{wrap},\\
0,& \epsilon_4\neq \mathrm{wrap}.
\end{cases}
\]
Therefore in the wrap case,
\[
\beta'-\beta = 0-0-(1-0)=-1,
\]
and in every non-wrap case,
\[
\beta'-\beta = -J-1-(0-J)=-1.
\]
So in all cases,
\[
\beta' = \beta-1 \pmod m.
\]

### Interpretation
This means the genuinely constructive burden is **not** the straightening from
`alpha` to `beta`.  Once `alpha` has the correct one-phase decrement law, the
beta clock follows automatically from the event semantics.

So the positive route can be phrased more sharply as:

> build `alpha` with universal birth and the one-phase decrement law; then
> `beta` is automatic.

## 4. Checked support on the frozen 047 data

I rechecked the frozen transition data for `m=5,7,9,11`.

The one-step transition scope contains:

- `216` transitions for `m=5`,
- `1212` transitions for `m=7`,
- `3952` transitions for `m=9`,
- `9780` transitions for `m=11`,

for a total of **15,160 checked transitions**.

On that scope there were **zero exceptions** to all of the following:

1. `alpha' = alpha - J`, with `alpha` reconstructed from
   `q \equiv -alpha + J`;
2. `u'-u = J`;
3. `J' = 1_{wrap}`;
4. the standard event increments of `B` listed in Theorem C;
5. `beta' = beta - 1`;
6. exact current-state readout of `q`, `c`, `epsilon4`, `tau`, and `next_tau`
   from `(B,beta)`;
7. exact next-state update of `B` from `(B,beta)` by the table in Theorem A.

So, on checked data, the active branch really does admit the exact normal form
\[
(B_n,\beta_n) \mapsto (T(B_n,\beta_n),\beta_n-1),
\]
with all other controller quantities read out from `(B,beta)`.

## 5. Honest status

What is now genuinely proved in this note:

- the phase-corner theorem and the beta-controller theorem are formally
  equivalent;
- beta straightening from alpha transport is formal under the standard event
  semantics;
- the resulting beta normal form is exactly consistent with the checked frozen
  `047` transition data.

What is **not** yet proved uniformly here:

- the full phase-corner theorem from first principles;
- the local/admissible realization of `alpha` or `beta` in the intended class.

So the positive-route frontier has sharpened further.

It is no longer:

> can we somehow realize a complicated beta controller?

It is now:

> can we realize the one-phase `alpha` transport law locally?

If yes, the beta-controller is essentially forced.
