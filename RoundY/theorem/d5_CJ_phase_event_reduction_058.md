# D5 CJ proof progress 058: phase-event reduction of the flat corner

This note keeps the theorem object fixed at
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\},
\]
and pushes the carry-jump proof one step further.

The new point is that the `057` flat-corner lemma can itself be recast as a corollary of a smaller **phase-event law**.  This law is still only checked on the frozen active branch, but it is cleaner than the earlier `delta` formulation and looks like the right next theorem target.

## 1. Phase variable

Define the current active-branch phase
\[
\Theta := q+s+v+\lambda \pmod m.
\tag{Theta}
\]
Using `s=w+u`, this is equivalently
\[
\Theta = q+w+u+v+\lambda.
\]
So `\Theta` is the total raw-coordinate sum on the active branch.

On flat states, since
\[
q\equiv u-\rho \pmod m,
\]
we have
\[
\Theta \equiv -\delta \pmod m,
\qquad
\delta:=\rho-(s+u+v+\lambda).
\tag{Theta-delta-flat}
\]
Thus the `057` flat-corner parameter `\delta` is exactly the negative of the current phase on the flat strand.

## 2. Checked phase-event law on the frozen `047` range

From the frozen `047` dataset, the current grouped event is an exact function of
\[
(\Theta,s,c),\qquad c=\mathbf 1_{\{q=m-1\}},
\]
on `m=5,7,9,11`; see `d5_CJ_theta_event_law_058.json`.

The law is:

\[
\Theta=0 \Longrightarrow \epsilon_4=\mathrm{wrap},\ dn=(0,0,0,0),
\tag{P0}
\]
\[
\Theta=1 \Longrightarrow \epsilon_4=\mathrm{carry\_jump},\ dn=(1,1,0,0),
\tag{P1}
\]
\[
\Theta=2 \Longrightarrow
\begin{cases}
\epsilon_4=\mathrm{other},\ dn=(1,0,0,0),& c=1,\\
\epsilon_4=\mathrm{flat},\ dn=(0,0,0,1),& c=0,
\end{cases}
\tag{P2}
\]
\[
\Theta=3 \Longrightarrow
\begin{cases}
\epsilon_4=\mathrm{other},\ dn=(0,0,1,0),& (c=1\ \text{and}\ s\neq 2)\ \text{or}\ (c=0\ \text{and}\ s=2),\\
\epsilon_4=\mathrm{flat},\ dn=(0,0,0,1),& (c=1\ \text{and}\ s=2)\ \text{or}\ (c=0\ \text{and}\ s\neq 2),
\end{cases}
\tag{P3}
\]
and for every
\[
4\le \Theta\le m-1,
\]
one has
\[
\epsilon_4=\mathrm{flat},\qquad dn=(0,0,0,1).
\tag{P4+}
\]

This is stronger and cleaner than the earlier `delta`-corner phrasing.

## 3. Why this is the right reformulation

The raw branch increments exactly one of the coordinates
\[
q,w,u,v,\lambda
\]
at each step:

- `wrap` increments `q`,
- `other=(1,0,0,0)` increments `w`,
- `carry_jump` increments `u`,
- `other=(0,0,1,0)` increments `v`,
- `flat` increments `\lambda`.

So, on the checked active branch, the phase `\Theta` advances by `+1` on every step.  In other words, the event law above is a cyclic schedule telling us **which coordinate gets the next unit increment**.

This makes the D5 branch look even more odometer-like than before: not only is there a grouped base with carry sheet and anticipation sheet, but the boundary mechanism is governed by a one-step phase scheduler on the active branch.

## 4. Flat-corner law from the phase-event law

Now take a current flat state `x`.
Then
\[
\epsilon_4(x)=\mathrm{flat},\qquad dn(x)=(0,0,0,1),
\]
so `x` lies in the flat part of the schedule.

### 4.1 The case `\delta=1`
By `(Theta-delta-flat)`,
\[
\Theta(x)=m-1.
\]
After one flat step, the successor `y=F(x)` has
\[
\Theta(y)=0.
\]
By `(P0)`, `y` is `wrap`.  So
\[
\delta=1 \Longrightarrow \text{next event is wrap}.
\tag{FC1}
\]

### 4.2 The case `2\le \delta\le m-3`
Again by `(Theta-delta-flat)`,
\[
\Theta(x)=m-\delta.
\]
After one flat step,
\[
\Theta(y)=m-\delta+1.
\]
If `2\le \delta\le m-3`, then
\[
4\le \Theta(y)\le m-1.
\]
So by `(P4+)`, `y` is flat.  Hence
\[
2\le \delta\le m-3 \Longrightarrow \text{next event is flat}.
\tag{FC2}
\]

### 4.3 The case `\delta=m-2`
Then
\[
\Theta(x)=2.
\]
Because `x` itself is flat, `(P2)` forces
\[
c(x)=0.
\]
After one flat step,
\[
\Theta(y)=3,
\qquad s(y)=s(x),
\qquad c(y)=c(x)=0.
\]
Applying `(P3)` with `c=0`,
\[
\epsilon_4(y)=\mathrm{other}
\iff s(y)=2
\iff s(x)=2.
\]
Otherwise `y` is flat.  Therefore
\[
\delta=m-2 \Longrightarrow
\begin{cases}
\text{next event is other},& s=2,\\
\text{next event is flat},& s\neq 2.
\end{cases}
\tag{FC3}
\]

Combining `(FC1)`, `(FC2)`, and `(FC3)` yields the whole `057/057a` flat-corner law.

## 5. CJ as a corollary

This recovers the carry-jump reduction immediately.

For a noncarry carry-jump state `x`, the `057` reduction already shows that the successor `y=F(x)` is flat with
\[
\delta(y)=m-2,
\qquad s(y)=s(x)+1.
\]
Applying `(FC3)` to `y`,
\[
\tau(y)=
\begin{cases}
1,& s(y)=2,\\
m-2,& s(y)\neq 2,
\end{cases}
\]
that is,
\[
R_{\mathrm{cj}}(x)=
\begin{cases}
1,& s(x)=1,\\
m-2,& s(x)\neq 1.
\end{cases}
\]
Together with the zero-reset fiber, this is exactly the noncarry part of `CJ`.

So:

> **CJ is now a corollary of the phase-event law `(P0)–(P4+)`.**

## 6. Honest status

What is now genuinely improved:

- the theorem object is unchanged: `(B,\tau,\epsilon_4)`;
- `046` remains the conceptual center;
- `057` is no longer best viewed as a standalone `delta` lemma;
- the checked flat-corner law is now compressed to a smaller scheduler statement in `\Theta`;
- `CJ` follows formally from that scheduler statement.

What is **not** yet proved uniformly in odd `m`:

- the phase-event law `(P0)–(P4+)` itself.

So the next proof target is even sharper than before:

> prove the uniform active-branch phase-event law in `\Theta=q+s+v+\lambda`,
> or at minimum prove the restricted pieces `(P0)`, `(P3)` with `c=0`, and `(P4+)`,
> since those already imply the flat-corner lemma and hence `CJ`.

That is the honest frontier after `057a`.
