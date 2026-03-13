# D5 Constructive Route Through Source Residue 063

This note switches from the theorem-side object `(B, tau, epsilon4)` to the
**stronger constructive refinement**
\[
\rho := u_{\mathrm{source}}+1 \pmod m,
\]
while keeping clear that `rho` is **not** a replacement theorem coordinate.
It is a current-memory refinement for the constructive branch.

The point is:

> once `rho` is transported, the hidden anticipation datum is no longer a
> future window. It becomes an explicit current-state quantity.

This is the positive constructive route suggested by `049`, now sharpened using
`058–062`.

---

## 1. Scope

What is theorem-side minimal:
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4.
\]

What is constructive-side stronger:
\[
(B,\rho),\qquad \rho=u_{\mathrm{source}}+1.
\]

Checked support:
- `049`: through `m = 5,7,9,11,13,15,17,19`,
  - `tau` is exact on `(s,u,v,layer,rho)`
  - `next_tau` is exact on `(s,u,layer,rho,epsilon4)`
  - `c` is exact on `(u,rho,epsilon4)`
  - `q \equiv u-rho+1_{epsilon4=cj} (mod m)`
- `058–062`: the active branch is governed by the mixed-witness phase machine
  in the auxiliary phase
  \[
  \Theta = q+s+v+\lambda \pmod m.
  \]

This note does **not** claim a uniform proof of the `rho`-route yet.  It gives
an explicit constructive normal form on the checked range and isolates the one
remaining constructive gap: **local birth/transport of `rho`**.

---

## 2. Auxiliary current-state residues

Let
\[
\rho = u_{\mathrm{source}}+1,
\qquad
\delta := \rho-(s+u+v+\lambda) \pmod m.
\]

Also write
\[
a := 1_{\{\rho=u+1\}}.
\]

On non-`carry_jump` states, `a` is exactly the current carry bit `c`, because
there
\[
q \equiv u-\rho \pmod m.
\]

On `carry_jump` states,
\[
q \equiv u-\rho+1 \pmod m,
\]
so the carry bit is
\[
c = 1_{\{\rho=u+2\}}.
\]

Thus the checked `049` current-state formula for the carry sheet can be written
compactly as
\[
c = 1_{\{\rho = u + 1 + 1_{\{\epsilon_4=\mathrm{carry\_jump}\}}\}}.
\tag{C1}
\]

Likewise,
\[
q \equiv u-\rho+1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
\tag{C2}
\]

So once `rho` is present, the hidden raw phase coordinate `q` is already a
current-state quantity.

---

## 3. Explicit constructive formula for tau

The strongest positive consequence is that `tau` itself admits a closed current
formula on `(s,u,v,layer,rho)`.

### Proposition C (checked constructive formula)
On the checked active best-seed branch, define
\[
\delta = \rho-(s+u+v+\lambda) \pmod m,
\qquad
 a = 1_{\{\rho=u+1\}}.
\]
Then
\[
\tau =
\begin{cases}
0, & \delta=0,\\[1mm]
\delta, & 1\le \delta \le m-4,\\[1mm]
0, & \delta=m-3 \text{ and } \big((a=0\ \&\ s=2)\ \text{or}\ (a=1\ \&\ s\neq 2)\big),\\[1mm]
m-3, & \delta=m-3 \text{ and } \big((a=0\ \&\ s\neq 2)\ \text{or}\ (a=1\ \&\ s=2)\big),\\[1mm]
0, & \delta=m-2 \text{ and } a=1,\\[1mm]
1, & \delta=m-2,\ a=0,\ s=2,\\[1mm]
m-2, & \delta=m-2,\ a=0,\ s\neq 2.
\end{cases}
\tag{C3}
\]

Equivalently, if the current event class `epsilon4` is also available, then the
formula becomes much cleaner:
\[
\tau = 0 \quad (\epsilon_4\neq \mathrm{flat}),
\]
and on the flat branch,
\[
\tau =
\begin{cases}
1,& (s,\delta)=(2,m-2),\\
\delta,& \text{otherwise.}
\end{cases}
\tag{C3'}
\]

So the hidden anticipation datum is not “future” anymore once `rho` is
transported.  It is an explicit current function.

### Why this formula is natural
- `delta=0` is exactly the wrap/carry_jump boundary, so `tau=0`.
- `1\le delta\le m-4` is the long flat zone, so the countdown is just `delta`.
- `delta=m-3,m-2` are the only corner phases where the mixed-witness scheduler
  can switch from `flat` to `other` depending on `s` and carry.

This is exactly the same corner structure that appears in the theorem-side
proof, but here it is written as a current-state formula through `rho`.

---

## 4. Explicit constructive formula for next_tau

The same refinement gives a full checked branchwise reset/update law.

### Proposition D (checked current-state update law)
With `delta`, `rho`, and current event class `epsilon4` as above,
\[
\tau'=
\begin{cases}
\tau-1, & \epsilon_4=\mathrm{flat},\\[1mm]
0, & \epsilon_4=\mathrm{wrap},\\[1mm]
0, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \rho=u+2,\\[1mm]
1, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \rho\neq u+2\ \&\ s=1,\\[1mm]
m-2, & \epsilon_4=\mathrm{carry\_jump}\ \&\ \rho\neq u+2\ \&\ s\neq 1,\\[1mm]
m-3, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-2\ \&\ s=1,\\[1mm]
0, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-2\ \&\ s\neq 1,\\[1mm]
m-4, & \epsilon_4=\mathrm{other}\ \&\ \delta=m-3.
\end{cases}
\tag{D1}
\]

This is exactly consistent with:
- the theorem-side countdown law for `tau>0`,
- the boundary reset formulas `CJ` and `OTH`,
- and the `049` statement that `next_tau` is exact on
  `(s,u,layer,rho,epsilon4)`.

---

## 5. Constructive interpretation

The constructive route is now much cleaner than “code tau locally somehow.”

Once `rho` is available:

1. `q` is explicit from `(u,rho,epsilon4)` by `(C2)`.
2. `c` is explicit from `(u,rho,epsilon4)` by `(C1)`.
3. `tau` is explicit from `(s,u,v,layer,rho)` by `(C3)`.
4. `tau'` is explicit from `(s,u,layer,rho,epsilon4)` by `(D1)`.

So the hidden theorem-side carrier has become a **current-memory carrier**.
The constructive problem is therefore no longer “predict the future.”
It is:

> **initialize and transport `rho`, then read out `q`, `c`, `tau`, and
> `next_tau` by explicit current formulas.**

That is the strongest positive constructive route currently visible.

---

## 6. Honest boundary

This note does **not** prove that `rho` is locally/admissibly realizable.
It only shows that if a local mechanism can initialize and transport `rho`,
then the hidden anticipation datum ceases to be hidden.

So the constructive fork is now sharp:

- theorem side stays minimal at `(B,tau,epsilon4)`;
- constructive side can aggressively use the stronger transported residue `rho`.

The remaining constructive gap is not the countdown itself. It is:

> **source-residue birth and transport.**

---

## 7. Recommended next constructive target

The smallest positive constructive theorem one could now hope for is:

> There exists a local/admissible mechanism that initializes a source-residue
> carrier `rho = u_source+1` at the `R1` birth event and transports it through
> the active branch.

If that were achieved, the rest of the active best-seed controller would be
explicit by `(C1)`, `(C2)`, `(C3)`, and `(D1)`.

So the constructive side has compressed to a very small question:

\[
\textbf{Can we realize the transported source residue }\rho\textbf{?}
\]
