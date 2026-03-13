# D5 proof progress 059: uniform active phase-event scheduler from the mixed witness rule

This note upgrades the `058` phase-event law from a checked scheduler to a genuine proof reduction.
The theorem object remains the minimal future-side object
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]
The auxiliary proof coordinate is
\[
\Theta := q+s+v+\lambda \pmod m.
\]
Here \(\lambda\) is the first torus coordinate, so
\[
\Theta = q+w+u+v+\lambda = x_0+x_1+x_2+x_3+x_4 \pmod m
\]
is exactly the mixed-witness layer bucket of the current state.

The key point is that, on the active nonterminal best-seed branch, every current state is still `B`-labeled, so the current outgoing direction is governed by the underlying mixed witness rule `mixed_008` without any endpoint override.  Thus the scheduler in `058` is not an empirical coincidence: it is just the witness rule written in the coordinate \(\Theta\).

## 1. Mixed witness rule on the active branch

For color `0`, the mixed witness `mixed_008` uses the following anchor table by layer bucket:

- layer bucket `0`: anchor `1`
- layer bucket `1`: anchor `4`
- layer bucket `2`: orientation `0/2`, with old bit `q=-1`, i.e.
  \[
  c:=\mathbf 1_{\{q=m-1\}}
  \]
  selects anchor `0` if `c=0` and anchor `2` if `c=1`
- layer bucket `3`: predecessor-flag mode switch with
  - `p_0=(0,3)`
  - `p_1=(3,0)`
  - predecessor flag `pred_sig1_wu2`
- layer buckets `4+`: anchor `0`.

Because
\[
\Theta = x_0+x_1+x_2+x_3+x_4 \pmod m,
\]
these layer buckets are exactly the residue classes of \(\Theta\).

## 2. The predecessor flag on the active branch

At layer bucket `3`, the only nontrivial local bit in the rule is `pred_sig1_wu2`.
For color `0`, predecessor direction `1` decrements the `q` coordinate and leaves `w,u` unchanged.  Therefore
\[
\texttt{pred\_sig1\_wu2}=1
\iff (w+u)\equiv 2 \pmod m
\iff s=2.
\]
So on the active branch the layer-`3` switch depends only on the pair `(c,s)`:

- if `c=0` and `s=2`, choose anchor `3`
- if `c=1` and `s\neq 2`, choose anchor `3`
- otherwise choose anchor `0`.

This is exactly the conditional in `(P3)` from `058`.

## 3. Anchor-to-event dictionary

On the active branch, anchor directions translate to grouped-delta events as follows.

- anchor `0`: increment `\lambda`, so
  \[
  dn=(0,0,0,1),\qquad \epsilon_4=\mathrm{flat}
  \]
- anchor `1`: increment `q`, so
  \[
  dn=(0,0,0,0),\qquad \epsilon_4=\mathrm{wrap}
  \]
- anchor `2`: increment `w`, hence `s=w+u` increases by `1`, so
  \[
  dn=(1,0,0,0),\qquad \epsilon_4=\mathrm{other}
  \]
- anchor `3`: increment `v`, so
  \[
  dn=(0,0,1,0),\qquad \epsilon_4=\mathrm{other}
  \]
- anchor `4`: increment `u`, hence also `s=w+u` increases by `1`, so
  \[
  dn=(1,1,0,0),\qquad \epsilon_4=\mathrm{carry\_jump}.
  \]

Thus once the witness anchor at a current state is known, the grouped event class is known.

## 4. Uniform phase-event scheduler theorem

### Theorem S (active phase-event scheduler, proof form)
Fix odd `m` and the best-seed active nonterminal branch of the `R1 -> H_L1` channel.  At every current state on that branch, let
\[
\Theta=q+s+v+\lambda \pmod m,
\qquad c=\mathbf 1_{\{q=m-1\}}.
\]
Then the current grouped event is determined by `(\Theta,s,c)` as follows:

\[
\Theta=0 \Longrightarrow \epsilon_4=\mathrm{wrap},\quad dn=(0,0,0,0),
\]
\[
\Theta=1 \Longrightarrow \epsilon_4=\mathrm{carry\_jump},\quad dn=(1,1,0,0),
\]
\[
\Theta=2 \Longrightarrow
\begin{cases}
\epsilon_4=\mathrm{other},\ dn=(1,0,0,0),& c=1,\\
\epsilon_4=\mathrm{flat},\ dn=(0,0,0,1),& c=0,
\end{cases}
\]
\[
\Theta=3 \Longrightarrow
\begin{cases}
\epsilon_4=\mathrm{other},\ dn=(0,0,1,0),& (c=0\ \&\ s=2)\ \text{or}\ (c=1\ \&\ s\neq 2),\\
\epsilon_4=\mathrm{flat},\ dn=(0,0,0,1),& \text{otherwise},
\end{cases}
\]
and for every
\[
4\le \Theta\le m-1,
\]
one has
\[
\epsilon_4=\mathrm{flat},\qquad dn=(0,0,0,1).
\]

#### Proof
Because the active nonterminal branch stays in `B`, the outgoing direction is given by the unmodified `mixed_008` rule.  The current layer bucket of that rule is exactly `\Theta`.

- If `\Theta=0`, the layer-`0` anchor is `1`, hence the current step increments `q`; this is `wrap`.
- If `\Theta=1`, the layer-`1` anchor is `4`, hence the current step increments `u`; this is `carry_jump`.
- If `\Theta=2`, the layer-`2` rule is the old-bit orientation `0/2` with old bit `c=1_{q=m-1}`.  Thus anchor `2` is chosen iff `c=1`, and otherwise anchor `0` is chosen.  This gives exactly the `\Theta=2` line.
- If `\Theta=3`, the layer-`3` rule is the predecessor-flag mode switch described above.  Since `pred_sig1_wu2 \iff s=2`, the switch chooses anchor `3` exactly in the two cases `(c=0,s=2)` and `(c=1,s\neq 2)`, and anchor `0` otherwise.  This gives exactly the `\Theta=3` line.
- If `\Theta\ge 4`, the witness uses anchor `0`, hence the current event is flat.

Translating anchors to grouped deltas via the dictionary of §3 gives the stated event labels and `dn` values. ∎

## 5. Immediate corollaries

### Corollary S1 (flat-corner law)
Let `x` be a current flat state and define the auxiliary residue
\[
\delta:=\rho-(s+u+v+\lambda) \pmod m,
\]
where `\rho=u_{source}+1` is used only as a proof aid.  On flat states one has
\[
\Theta \equiv -\delta \pmod m.
\]
Hence:

- `\delta=1` implies the next event is `wrap`
- `2\le \delta\le m-3` implies the next event is `flat`
- `\delta=m-2` implies the next event is `other` iff `s=2`, and otherwise `flat`.

This is exactly the `057` flat-corner law.

### Corollary S2 (CJ reset formula)
On a carry-jump state `x`, one has `\Theta=1`, hence
\[
q\equiv 1-s-v-\lambda \pmod m.
\]
If `q=m-1`, equivalently `s+v+\lambda\equiv 2`, then the reset is `0`.  If `q\neq m-1`, then the successor is flat at phase `\Theta=2`; the flat-corner law then yields
\[
R_{\mathrm{cj}}(x)=
\begin{cases}
1,& s=1,\\
m-2,& s\neq 1.
\end{cases}
\]
This is the full checked CJ formula.

### Corollary S3 (OTH reset formula)
For `other=(1,0,0,0)` one is at phase `\Theta=2` with `c=1`.  The successor has phase `\Theta=3`, still `c=1`, and new `s'=s+1`.  By Theorem S, the successor is `flat` iff `s'=2`, i.e. iff `s=1`; otherwise it is the second `other` subtype.  Therefore
\[
(1,0,0,0)\mapsto
\begin{cases}
m-3,& s=1,\\
0,& s\neq 1.
\end{cases}
\]
For `other=(0,0,1,0)` one is at phase `\Theta=3`; the successor has phase `\Theta=4`, hence is always flat.  Therefore
\[
(0,0,1,0)\mapsto m-4.
\]
This is exactly the checked OTH reset law.

## 6. Honest status

What is now proved modulo the witness-rule facts already established earlier in the project:

- the active phase-event law is a direct consequence of the mixed witness rule,
- the `057` flat-corner law is a corollary,
- `CJ` is a corollary,
- `OTH` is also a corollary.

So the proof burden has compressed all the way to the one statement that the active nonterminal best-seed branch stays in the unmodified `B`-region of the mixed witness.  Once that corridor fact is admitted, the branch reset formulas are no longer separate mysteries; they are just the mixed witness phase machine.

In particular, the theorem-side object remains minimal: `(B,\tau,\epsilon_4)`.  The auxiliary phase `\Theta` is only a proof coordinate, and `\rho` is used only to restate the flat-corner corollary.
