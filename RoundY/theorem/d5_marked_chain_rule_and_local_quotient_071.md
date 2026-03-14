# D5 Marked Chain Rule And Local Quotient 071

This note answers the `070` exact-reduction question on the frozen `045`
checked-range data only:

> what is the correct exact rule on the first marked chain, and what quotient of
> that rule is the current admissible catalog actually seeing?

## 1. Exact marked-chain rule

Fix a checked modulus `m` and a regular carry-jump slice at fixed
`(source_u, w)`. The extracted rows form a marked chain of length `m`
with normalized coordinate
\[
q \in \{0,1,\dots,m-1\}.
\]

Define the slice offset
\[
\sigma := source_u + w \pmod m.
\]

Then on every checked row
\[
s = q + \sigma \pmod m.
\]

So the same chain can be written in the affine local coordinate `s`.

The rule is exact on the frozen checked range:

- **interior states** `q < m-1`:
  \[
  q' = q+1,\qquad s' = s+1 \pmod m,
  \]
  with
  \[
  c=0,\qquad next\_dn = (0,0,0,1)\;\text{(flat)}.
  \]

- **endpoint state** `q = m-1`:
  \[
  s = \sigma - 1 \pmod m,
  \]
  with
  \[
  c=1,\qquad next\_dn = (1,0,0,0)\;\text{(other_1000)}.
  \]

So the first exact reduction object is:

- the standard marked length-`m` chain in `q`-gauge, or
- equivalently an affine `s`-gauge chain
  \[
  s \mapsto s+1
  \]
  with chain-dependent marked endpoint
  \[
  s = \sigma-1.
  \]

This is the *chain* object. The splice from the endpoint to the next `w`-slice
belongs to the later source-chain / cycle promotion step.

## 2. What the catalog is actually seeing

The best exact deterministic one-feature families from `070`
(`cur:antidiag_omit.tau_lo`, `cur:diag_omit.tau_lo`) are not mysterious on this
object. On the full frozen `045` data they are exactly

\[
cur:antidiag\_omit.tau\_lo = cur:diag\_omit.tau\_lo = s.
\]

Likewise their `nxt:` versions are exactly the next `s` value:
\[
nxt:antidiag\_omit.tau\_lo = nxt:diag\_omit.tau\_lo = s'.
\]

So the first exact deterministic quotient of size `m` is simply:

> **the affine chain coordinate `s` on each fixed marked chain.**

By contrast, the familiar 2-state exact-only families from `070`
(`next_dn`, `dn + next_dn`) are only seeing the endpoint/interior partition:

- interior: `next_dn = flat`
- endpoint: `next_dn = other_1000`

That reads the mark exactly, but loses deterministic successor.

## 3. Per-chain versus union-of-chains

The important nuance is:

- on each **fixed** marked chain, `s` gives an exact deterministic quotient of
  size `m`;
- on the **union** of all marked chains, `s` is not exact for carry and not
  deterministic for successor, because the marked endpoint sits at
  \[
  s = \sigma-1
  \]
  and the offset `\sigma = source_u + w` changes from chain to chain.

So the intended class is already seeing the correct first exact object, but only
in its **unnormalized affine gauge** on each chain separately.

## 4. Compute conclusion

The clearest current answer is:

1. the correct first exact rule is the marked length-`m` chain
   \[
   q \mapsto q+1
   \]
   with marked endpoint at `q=m-1`;
2. the current admissible catalog already sees this rule as the affine
   `s`-gauge chain
   \[
   s \mapsto s+1
   \]
   on each fixed slice chain;
3. `next_dn` contributes only the endpoint bit, not the full deterministic
   chain state;
4. the remaining normalization issue is exactly the hidden offset
   \[
   \sigma = source_u + w,
   \]
   which is why the union of all slice chains does not yet collapse to one
   exact deterministic quotient in the same small class.
