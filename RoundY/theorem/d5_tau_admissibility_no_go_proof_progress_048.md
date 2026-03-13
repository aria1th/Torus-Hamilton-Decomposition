# D5 tau / carry-sheet proof progress after 044–047

## Status line

The conceptual theorem should now be centered on `046`, not `047`.

- `044` gives the checked finite-sheet normal form
  \[
  B \leftarrow B+c \leftarrow B+c+d,
  \qquad
  B=(s,u,v,\lambda,\mathrm{family}),
  \qquad
  c=\mathbf 1_{\{q=m-1\}},
  \qquad
  d=\mathbf 1_{\{U^+\ge m-3\}}.
  \]
- `045` is the first carry-specific admissibility no-go in the current-edge / short-transition / low-cardinality gauge catalogs.
- `046` is the conceptual theorem: the carry sheet is already an exact one-sided future transition event on the grouped base.
- `047` is a boundary sharpening: once the anticipation coordinate is recognized, the only extra current datum needed is the `tau=0` boundary class.

So the live proof fork is now exactly:

1. prove an admissible/local coding theorem for `tau`, or
2. prove a no-go theorem for the intended local mechanism class.

---

## Conceptual theorem (`046`)

Define on the checked active best-seed branch
\[
B(x)=(s,u,v,\lambda,\mathrm{family}),
\qquad
\Delta_n(x)=B(Tx)-B(x),
\qquad
\Delta_{\mathrm{flat}}=(0,0,0,1),
\]
where `T` is the active grouped return map.

Define the anticipation time
\[
\tau(x)=\min\{t\ge 0: \Delta_n(T^t x)\ne \Delta_{\mathrm{flat}}\}.
\]
Let
\[
\eta(x)=\Delta_n(T^{\tau(x)}x)
\]
be the first nonflat grouped-delta event.

### Checked theorem (`046`)
On `m=5,7,9,11`, the carry sheet satisfies
\[
c(x)=\mathbf 1_{\{q(x)=m-1\}} = F\bigl(B(x),\tau(x),\eta(x)\bigr)
\]
for an exact function `F` on the checked active branch.

Moreover:

- the minimal exact grouped-delta horizon is `m-3`,
- the minimal exact grouped-state horizon is `m-2`.

This is the correct manuscript-level theorem: **the carry sheet is an anticipation datum over the grouped base**.

---

## Boundary sharpening (`047`)

Let `epsilon4` be the current grouped-delta event class
\[
\epsilon_4 \in \{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]

### Checked theorem (`047`)
On `m=5,7,9,11`:

1. all ambiguity of `B+tau` lies at `tau=0`;
2. the `tau=0` boundary class is genuinely `3`-class minimal:
   \[
   \{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\};
   \]
3. therefore
   \[
   c = G(B,\tau,\epsilon_4)
   \]
   is exact on the checked active branch.

This should be presented as a sharpening of `046`, not as the conceptual endpoint.

---

## Stronger per-modulus pattern extracted from the 047 dataset

The checked-range statement `B + min(\tau,8) + \epsilon_4` is not the cleanest canonical form.

A cleaner per-modulus pattern is already visible in the frozen `047` data.

### Proposition A (checked per modulus)
For each checked modulus `m in {5,7,9,11}`:

1. the quotient
   \[
   B + \min(\tau,m-3) + \epsilon_4
   \]
   is exact for `c`;
2. no smaller truncation horizon survives;
3. equivalently, the first exact transition-sheet coding is
   \[
   B + \epsilon_4(\text{current}) + \beta_{m-4},
   \]
   where `beta_h` is the next `h` future flat/nonflat indicators **after** the current step.

On the checked moduli, the minimal exact horizons are:

| coding family | minimal exact horizon |
|---|---:|
| current `epsilon4` + future binary after current | `m-4` |
| full `epsilon4` event window | `m-3` |
| pure binary flat/nonflat window | `m-1` |

This is supported by
[`d5_047_per_modulus_horizon_pattern.json`](../checks/d5_047_per_modulus_horizon_pattern.json).

### Proof sketch
For each fixed checked `m`, the frozen `047` dataset shows exactness/nonexactness of these quotient families. The first exact horizon for
\[
(B,\epsilon_4,\beta_h)
\]
appears at `h=m-4`, and the first exact truncation of `tau` appears at `m-3`. Since `tau` takes values in `{0,1,\dots,m-2}`, this is equivalent to exactness of
\[
B+\min(\tau,m-3)+\epsilon_4.
\]

---

## Explicit witness family for the lower bound

The most useful new proof ingredient is an explicit witness pair already visible across all checked moduli.

### Proposition B (checked witness pair)
For each `m in {5,7,9,11}`, the active branch contains two regular states with the same grouped base
\[
B_*=(3,1,2,0,\mathrm{regular})
\]
and the same current boundary class
\[
\epsilon_4=\mathrm{flat},
\]
but opposite carry labels:
\[
x^-_m=(q,w,u,v,\lambda)=(m-2,2,1,2,0), \qquad c(x^-_m)=0,
\]
\[
x^+_m=(q,w,u,v,\lambda)=(m-1,2,1,2,0), \qquad c(x^+_m)=1.
\]
Their anticipation times satisfy
\[
\tau(x^-_m)=m-3,
\qquad
\tau(x^+_m)=m-4.
\]
Hence for every `h < m-4`, the states `x^-_m` and `x^+_m` have identical data
\[
(B,\epsilon_4,\beta_h)
\]
but different carry labels.

### Consequence
No coding family that depends only on current `B`, current `epsilon4`, and the next `h` future flat/nonflat bits after the current step can realize `c` on that modulus when `h < m-4`.

### Proof sketch
For both witness states the current event is flat. The future binary-after-current sequence for `x^+_m` has exactly `m-5` leading `1`s and then a `0`; for `x^-_m` it has exactly `m-4` leading `1`s. Therefore the two states agree on every prefix of length `< m-4` and disagree at length `m-4`. Since their carry labels differ, every shorter horizon fails.

This is precisely the observed lower bound in
[`d5_047_per_modulus_horizon_pattern.json`](../checks/d5_047_per_modulus_horizon_pattern.json).

---

## What this proves now, and what it does not yet prove

### Proved on checked moduli
- `046` gives the conceptual theorem: `c` is a one-sided anticipation datum over the grouped base.
- `047` gives the boundary sharpening: `epsilon4` is only needed at `tau=0`.
- The per-modulus canonical pattern is cleaner than the checked-range summary:
  \[
  c \text{ is exact on } B+\min(\tau,m-3)+\epsilon_4,
  \]
  equivalently on
  \[
  B+\epsilon_4+\beta_{m-4}.
  \]
- There is a genuine lower-bound witness family forcing the `m-4` horizon in the `B+epsilon4+future-binary` class.

### Not yet proved
We do **not** yet have a theorem saying that every admissible/local mechanism in the intended `025`-style class factors through one of these bounded-horizon transition-sheet families.

That reduction lemma is now the exact missing step if the goal is a full no-go theorem for the intended local class.

---

## The right next proof target

The cleanest theorem target is now:

### Theorem target
Either:

1. **Admissible coding theorem for `tau`:**
   show that the intended admissible/local class can express the anticipation coordinate `tau` (or an equivalent coding such as `min(tau,m-3)` together with the `tau=0` boundary class);

or:

2. **Bounded-horizon reduction + no-go theorem:**
   prove that every intended local mechanism factors through a bounded-horizon grouped transition sheet, then combine that reduction with Proposition B to rule out exact coding of `c` and hence `tau`.

### Best current proof split
- `046` should be written as the conceptual theorem.
- `047` should be written as the boundary sharpening theorem.
- the new horizon lemma above should be inserted as the first serious no-go direction:
  **no fixed bounded future-binary horizon can code the carry sheet uniformly in `m`, and the checked minimal horizon is exactly `m-4`.**

That is real proof progress, not just another search summary.
