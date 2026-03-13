# D5 positive route: alpha-gauge sharpening

Starting from the `063` route organization, the positive constructive route can be sharpened substantially.

## 1. Main sharpening

The route organization says the constructive branch should transport
\[
\rho = u_{\mathrm{source}}+1 \pmod m,
\]
and suggests the gauge
\[
\alpha := \rho-u
\]
as the better transport variable.

The key extra observation is that after passing to `alpha`, the current-state readout formulas no longer need `u` at all.

Indeed, substituting `rho = alpha + u` into the checked constructive formulas gives:

\[
q \equiv -\alpha + 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
\]

Hence
\[
c=1_{\{q=m-1\}} = 1_{\{\alpha = 1 + 1_{\{\epsilon_4=\mathrm{carry\_jump}\}}\}}.
\]

Also
\[
\delta = \rho-(s+u+v+\lambda)=\alpha-(s+v+\lambda) \pmod m.
\]

So on the checked branch:

- `q` is exact on `(alpha, epsilon4)`;
- `c` is exact on `(alpha, epsilon4)`;
- `tau` is exact on `(s,v,layer,alpha,epsilon4)`;
- `next_tau` is exact on `(s,v,layer,alpha,epsilon4)`.

This is strictly cleaner than the raw `rho` formulation, where `u` still appears in the coordinate list.

## 2. Exact alpha-gauge readout formulas

Write
\[
\delta := \alpha-(s+v+\lambda) \pmod m.
\]

Then:

### Carry / raw phase
\[
q \equiv -\alpha + 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m,
\]
\[
c = 1_{\{\alpha = 1 + 1_{\{\epsilon_4=\mathrm{carry\_jump}\}}\}}.
\]

Equivalently:
- off `carry_jump`, `c=1` iff `alpha=1`;
- on `carry_jump`, `c=1` iff `alpha=2`.

### Countdown
\[
\tau=0 \qquad (\epsilon_4\neq \mathrm{flat}),
\]
and on the flat branch,
\[
\tau=
\begin{cases}
1,& (s,\delta)=(2,m-2),\\
\delta,& \text{otherwise.}
\end{cases}
\]

### One-step update
\[
\tau'=
\begin{cases}
\tau-1, & \epsilon_4=\mathrm{flat},\\
0, & \epsilon_4=\mathrm{wrap},\\
0, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \alpha=2,\\
1, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \alpha\neq 2\ \&\ s=1,\\
m-2, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \alpha\neq 2\ \&\ s\neq 1,\\
m-3, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-2\ \&\ s=1,\\
0, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-2\ \&\ s\neq 1,\\
m-4, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-3.
\end{cases}
\]

Again, `u` has disappeared.

## 3. What transporting alpha really means

Since
\[
\alpha = \rho-u,
\]
transporting `alpha` is equivalent to preserving the invariant
\[
\alpha+u=\rho.
\]

So the positive route can be reformulated as:

> build a local carrier `alpha` so that `alpha+u` is invariant and initially equals `u_source+1`.

At the post-entry active state we have `u=u_source`, so the natural birth value is
\[
\alpha=1.
\]

Thus the carrier does **not** need to be born as an arbitrary residue. It can be born as the constant value `1`, and then updated so that `alpha+u` stays fixed.

## 4. Why alpha is easier than raw rho

The candidate active orbit from the structural branch has updates
\[
(q,w,u,0)\mapsto(q+1,w,u,1),
\]
\[
(q,w,u,1)\mapsto(q,w,u+1,2),
\]
\[
(q,w,u,2)\mapsto(q,w+1_{\{q=m-1\}},u,3),
\]
with only the phase-1 step changing `u`.

Therefore, on the active odometer corridor,
\[
\alpha' = \alpha-1
\]
exactly when the current step is the unique `u`-increment step, and otherwise
\[
\alpha' = \alpha.
\]

So the constructive burden is smaller than “store an arbitrary mod-`m` source label forever.” It is:

> detect the unique `u`-increment phase and decrement `alpha` there.

That is a one-phase update problem, not a general memory problem.

## 5. Recommended positive theorem target

A clean constructive target is the following.

### Alpha-transport theorem (proposed)
There exists a local/admissible carrier `alpha` on the active best-seed branch such that:

1. **Birth:** at the `R1` post-entry state, `alpha=1`.
2. **Transport:**
   \[
   \alpha'+u' \equiv \alpha+u \pmod m.
   \]
   Equivalently,
   \[
   \alpha' = \alpha-(u'-u) \pmod m.
   \]
3. **Readout:** `q`, `c`, `tau`, and `next_tau` are given by the alpha-gauge formulas above.

If this theorem is proved, then the whole positive route closes.

## 6. Best lemma chain

The most efficient positive program now looks like:

1. **Birth lemma:** at active entry, `alpha=1`.
2. **u-step detector lemma:** the active branch admits a current-state test for whether the next step increments `u`.
3. **Alpha invariance lemma:** update `alpha` by subtracting that indicator, so `alpha+u` is invariant.
4. **Readout lemma:** substitute `rho=alpha+u` into the checked formulas.
5. **Controller corollary:** recover `q`, `c`, `tau`, and `next_tau` current-state exactly.

This isolates the real constructive gap more sharply than the raw `rho` wording:

> not “transport source residue” in the abstract,
> but “realize a one-phase decrement carrier whose sum with `u` is invariant.”

## 7. Honest status

This does not prove local realizability.
It does sharpen the positive route materially:

- the transport variable should be `alpha`, not raw `rho`;
- `u` disappears from the readout formulas once that change is made;
- the local task becomes a one-phase decrement mechanism.
