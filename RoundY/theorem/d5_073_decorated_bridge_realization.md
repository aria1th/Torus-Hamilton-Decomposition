# D5 073 — decorated exact bridge realization

## Scope actually used

This note continues **Researcher 3** after the `072` sync.

Inputs used here:

- the `072` frontier update supplied in the session:
  the coarse bridge is now treated as essentially settled, the bare `m`-state
  bridge is too coarse for current `epsilon4`, and a small decorated bridge of
  the form `(beta,a,b)` is supported on the checked range;
- the theorem-side phase/corner package from `069`;
- the conditional corner-time descent argument from `070`;
- the checked per-chain decorated rule from `071`.

What this note does **not** do:

- it does not prove existence of the global decorated bridge;
- it does not derive the carry-step update rule for `(a,b)` across chains;
- it does not prove that the uniform `(beta,a,b)` model is globally minimal
  among all possible exact quotients.

So the scope is: sharpen the realization theorem so it matches the new
**decorated exact bridge** target, and isolate exactly what extra exactness is
forced and exactly what still remains open.

## 1. Frontier after `072`

After the `072` sync, the realization question should be phrased in the
following order.

1. The coarse carry / distance-to-endpoint bridge is no longer the live issue.
2. The bare `beta` bridge is known to be too coarse for current `epsilon4`.
3. The checked-range support points to a refined bridge carrying the two early
   post-carry decorations.
4. Once that refined bridge is deterministic and exact for current `epsilon4`,
   the canonical clock should descend by corner-time.

So the live Researcher-3 problem is no longer:

> can *some* bridge realize the clock?

It is now:

> on the refined decorated bridge, what exactness is sufficient, what extra
> exactness is forced, and what part of the clock descent is already automatic?

## 2. The checked local decorated rule

The `071` chain note isolates a very small local rule on each checked regular
marked chain.

Write the local chain coordinate as
\[
\beta \in \{m-1,m-2,\dots,1,0\}
\]
with successor
\[
\beta \mapsto \beta-1.
\]

The checked current-event pattern is determined by two binary decorations
\[
(a,b) \in \{0,1\}^2,
\]
where:

- `a=1` means the state at `beta=m-2` is `other_1000`;
- `a=0` means the state at `beta=m-2` is `flat`;
- `b=1` means the state at `beta=m-3` is `other_0010`;
- `b=0` means the state at `beta=m-3` is `flat`.

So the checked local readout is:
\[
\bar\epsilon_4(\beta,a,b)=
\begin{cases}
\mathrm{carry\_jump}, & \beta=m-1,\\
\mathrm{other}_{1000}, & \beta=m-2\text{ and }a=1,\\
\mathrm{flat}, & \beta=m-2\text{ and }a=0,\\
\mathrm{other}_{0010}, & \beta=m-3\text{ and }b=1,\\
\mathrm{flat}, & \beta=m-3\text{ and }b=0,\\
\mathrm{flat}, & 1\le \beta\le m-4,\\
\mathrm{wrap}, & \beta=0.
\end{cases}
\]

On the checked range `m=5,7,9,11`, all four local types occur:

- `m=5`: `(0,0):19`, `(0,1):5`, `(1,0):1`, `(1,1):2`;
- `m=7`: `(0,0):103`, `(0,1):17`, `(1,0):3`, `(1,1):12`;
- `m=9`: `(0,0):299`, `(0,1):37`, `(1,0):5`, `(1,1):30`;
- `m=11`: `(0,0):655`, `(0,1):65`, `(1,0):7`, `(1,1):56`.

This gives two immediate consequences.

First, the bare `beta` chain is not exact for current `epsilon4`: it merges
`flat / other_1000` at `beta=m-2` and `flat / other_0010` at `beta=m-3`.

Second, the local obstruction is now very narrow: the missing exactness lives at
exactly the two early post-carry sites.

## 3. The right abstract decorated bridge target

The checked local rule suggests the following abstract global target.

A **decorated exact bridge** is a deterministic quotient `Q^dec` with successor
`G` and coordinate functions
\[
\beta:Q^{dec}\to \mathbb Z/m\mathbb Z,
\qquad
 a,b:Q^{dec}\to \{0,1\},
\]
with the following properties.

1. **Clock drift.**
   \[
   \beta(Gq)=\beta(q)-1 \pmod m.
   \]
2. **Within-block stationarity.**
   On a regular block, the decorations `(a,b)` are fixed until the wrap/carry
   splice. In particular, along the step `beta=m-2 -> m-3`, the same block
   decoration is still being read.
3. **Current-event exactness.**
   The checked local formula above really gives the current `epsilon4` readout
   on `Q^dec`.
4. **Carry-step update left open.**
   When `beta=0` returns to the next carry-jump state, the new block may have a
   new pair `(a^+,b^+)`; this note does not specify that update law.

This is exactly the right level for the current frontier. Researcher 3 does not
need the carry-step update law in order to prove clock descent *once* the global
refined bridge exists and is exact for current `epsilon4`.

## 4. Local short-corner visibility on the decorated bridge

The theorem-side short corner is the unique state with two-step event signature
\[
(\epsilon_4,\epsilon_4\circ F)=(\mathrm{flat},\mathrm{other}_{0010}).
\]

On the decorated bridge, that detector becomes explicit.

### Proposition 4.1 (local short-corner detector)

Assume `Q^dec` satisfies the four conditions above. Then on every regular block,
\[
(\bar\epsilon_4(q),\bar\epsilon_4(Gq))=(\mathrm{flat},\mathrm{other}_{0010})
\iff
(\beta(q),a(q),b(q))=(m-2,0,1).
\]

So the short corner is visible on the decorated bridge as the current-state
subset
\[
S_\star := \{q\in Q^{dec}: (\beta(q),a(q),b(q))=(m-2,0,1)\}.
\]

#### Proof

At `beta=m-2`, the current event is `flat` exactly when `a=0`. By within-block
stationarity, the next state `Gq` is still in the same block and has
`beta=m-3` with the same block decoration `b`. At `beta=m-3`, the event is
`other_0010` exactly when `b=1`. No other `beta` value can produce the pair
`(flat, other_0010)`, because `other_0010` appears only at `beta=m-3`. ∎

This is the first clean payoff of the decorated bridge: the short corner is no
longer hidden in a future word. It is a visible state subset.

## 5. Global corner-time realization: componentwise form

The `070` note already gave the conditional realization theorem in a form well
suited to an exact `m`-cycle. For the decorated bridge, the correct statement is
slightly more global: the time to the next short corner may be longer than one
`m`-block, because not every regular block is of type `(a,b)=(0,1)`.

So the realization theorem should be stated componentwise.

### Theorem 5.1 (global corner-time realization)

Let `X` be the theorem-side exact accessible object with deterministic successor
`F`, phase
\[
\kappa:X\to \mathbb Z/m\mathbb Z,
\qquad
\beta:=-\kappa.
\]
Assume:

1. \(\kappa(Fx)=\kappa(x)+1\pmod m\);
2. on each accessible component of `X`, there is a unique short-corner state
   `x_\star`, and it is characterized by
   \[
   (\epsilon_4(x),\epsilon_4(Fx))=(\mathrm{flat},\mathrm{other}_{0010});
   \]
3. \(\pi:X\to Q\) is a deterministic quotient with induced successor `G` and
   current-event exactness
   \[
   \epsilon_4 = \bar\epsilon_4\circ \pi.
   \]

Then on each accessible component `C` of `Q`:

- there is a unique state `q_\star\in C` such that
  \[
  (\bar\epsilon_4(q),\bar\epsilon_4(Gq))=(\mathrm{flat},\mathrm{other}_{0010});
  \]
- if `C` is cyclic of length `\ell_C`, the hitting time
  \[
  T_C(q):=\min\{0\le r<\ell_C : G^r q = q_\star\}
  \]
  is well defined and satisfies
  \[
  T_C(Gq)=T_C(q)-1 \pmod{\ell_C};
  \]
- the canonical clock descends as
  \[
  \beta_Q(q):=T_C(q)-2 \pmod m,
  \]
  and obeys
  \[
  \beta_Q\circ \pi = \beta.
  \]

#### Proof

The short-corner detector descends because the two-step event word descends on
any deterministic quotient exact for current `epsilon4`.

Now fix one component and pull everything back to `X`. The theorem-side short
corner has phase `kappa=2`, hence
\[
\beta(x_\star)=m-2.
\]
If `F^r x = x_\star`, then unit drift gives
\[
\beta(x)-r \equiv m-2 \pmod m,
\]
so
\[
\beta(x) \equiv r-2 \pmod m.
\]
Taking `r=T_C(\pi(x))` gives
\[
\beta(x)=T_C(\pi(x))-2 \pmod m.
\]
So `beta` factors through `Q` by the displayed formula. The drift identity for
`T_C` is immediate from first-hit time on a deterministic cycle. ∎

### Remark 5.2

The earlier `070` formulation used “the next short corner within the next `m`
steps.” That is enough when the exact quotient itself is the relevant `m`-cycle.
For the decorated bridge, the more natural object can be a longer deterministic
component, and the right clock formula is still
\[
\beta_Q = T_{corner}-2 \pmod m,
\]
but now `T_{corner}` means **componentwise first-hit time to the next short
corner**, not necessarily time within one `m`-block.

This is the key realization refinement after `072`.

## 6. Decorated-bridge realization theorem

Combining Proposition 4.1 with Theorem 5.1 gives the Researcher-3 target in the
form now appropriate for the refined bridge.

### Corollary 6.1 (realization on the decorated exact bridge)

Assume a deterministic global decorated bridge `Q^dec` exists, exact for current
`epsilon4`, and assume each accessible component of `Q^dec` contains a unique
state of type
\[
(\beta,a,b)=(m-2,0,1).
\]
Then:

1. the short-corner detector on `Q^dec` is exactly the visible subset
   \[
   S_\star=\{(\beta,a,b)=(m-2,0,1)\};
   \]
2. the corner-time function
   \[
   T_{S_\star}(q)=\text{first hit time from }q\text{ to }S_\star
   \]
   is well defined componentwise;
3. the canonical clock descends by the fixed normalization
   \[
   \beta_Q(q)=T_{S_\star}(q)-2 \pmod m.
   \]

So the decorated bridge is already exact enough for realization. The remaining
burden is bridge existence and component structure, not a separate clock
construction.

## 7. What exactness is forced, and what is still open

The checked family already proves a sharp lower-bound statement on exactness.

### Proposition 7.1 (forced refinements of the bare bridge)

Any quotient that is exact for current `epsilon4` on the checked local decorated
family must distinguish at least:

- the two states at `beta=m-2` with `a=0` and `a=1`;
- the two states at `beta=m-3` with `b=0` and `b=1`.

#### Proof

At `beta=m-2`, current `epsilon4` is `flat` when `a=0` and `other_1000` when
`a=1`, and both cases occur on the checked range. So they cannot be merged in
an exact current-event quotient.

Likewise, at `beta=m-3`, current `epsilon4` is `flat` when `b=0` and
`other_0010` when `b=1`, and both cases occur on the checked range. So those
states cannot be merged either. ∎

This proves exactly where extra exactness beyond the bare `beta` bridge must
live.

What it does **not** yet prove is that the uniform `(beta,a,b)` state space is
minimal among all exact deterministic quotients. A smaller nonuniform quotient
might still exist, for example one that only refines `beta` near the two early
post-carry sites. So the right conclusion is:

- the bare bridge is definitely too coarse;
- exactness must refine it at the two early post-carry sites;
- the checked uniform decorated bridge is a sufficient realization target;
- true minimality is still open.

That is the precise form of the “smallest exact bridge” question after `072`.

## 8. Researcher-3 handoff after this note

The responsibilities now split cleanly.

### What is now settled on the Researcher-3 side

- the refined bridge makes the short corner visible as a current-state subset;
- once the refined bridge is deterministic and exact for current `epsilon4`,
  the canonical clock descends automatically by componentwise corner-time;
- the bare `beta` bridge fails for a completely localized reason: it loses the
  two early post-carry distinctions.

### What still has to be supplied by the other frontier branches

- **Researcher 1 / 2:** prove existence of the deterministic global decorated
  bridge and identify the carry-step update law for `(a,b)` across chains;
- **Researcher 4:** validate the refined bridge and check the component
  structure, especially uniqueness of the short-corner state per accessible
  component.

So the current realization theorem can now be stated cleanly as:

> **If the deterministic decorated exact bridge exists and is exact for current
> `epsilon4`, then the canonical clock descends uniquely as corner-time to the
> visible short-corner subset `S_\star={(m-2,0,1)}` with the fixed
> normalization `beta = T_{S_\star}-2 mod m`.**

That is the right Researcher-3 success criterion relative to the `072` frontier.
