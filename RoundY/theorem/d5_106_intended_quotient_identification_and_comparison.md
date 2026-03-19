# D5 106 Intended Quotient Identification And Comparison

This note answers the live M3 bookkeeping question after `105`:

- what the downstream intended quotient should mean,
- whether it is literally the same as the dynamic bridge `(beta,q0,sigma)` /
  `(beta,delta)`,
- and what comparison theorem should actually be proved next.

## Scope actually used

- theorem-side context from `068`, `074`, `076`, `099`, and `105`
- the regenerated comparison check
  [../checks/d5_106_intended_quotient_compare_summary.json](../checks/d5_106_intended_quotient_compare_summary.json)
- the supporting script
  [../../scripts/torus_nd_d5_intended_quotient_compare_106.py](../../scripts/torus_nd_d5_intended_quotient_compare_106.py)

I did **not** prove a new first-principles theorem about every imported layer in
this note. The point is to freeze the right quotient statement and the right
proof program.

## Executive answer

The honest downstream intended quotient is **not** “literally `(beta,delta)` on
the nose.”

The right theorem-side target is:

> the exact deterministic quotient on the exact marked object that retains the
> grouped base `G` and is exact for current `epsilon4`.

The right checked dynamic comparison target is:

> the carry-jump-to-wrap state-chain bridge `(beta,q0,sigma)`, equivalently
> `(beta,delta)` with `delta = q0 + m sigma`.

The new check `106` shows on regenerated moduli `m=13,15,17`:

1. `(B,beta)` determines `(beta,q0,sigma)` exactly;
2. `(beta,q0,sigma)` is exact for current `epsilon4`, exact for the
   short-corner detector, and deterministic on successor;
3. the reverse map fails globally because `(beta,q0,sigma)` forgets
   source-residue bookkeeping;
4. adjoining `rho = source_u + 1` repairs that loss exactly:
   `(rho,beta,q0,sigma)` recovers `(B,beta)` on every checked modulus;
5. adjoining only `family` does **not** recover `(B,beta)`.

So the correct manuscript claim is:

> the theorem-side intended quotient should be compared to the dynamic bridge by
> a factor map, and the two parameterizations become equivalent only after
> adjoining source residue `rho` or after fixing a splice-connected
> source/component.

That is the form in which full M3 now looks provable.

## 1. What object should be frozen

The `105` note already proves the odd-`m` rigid part:

- every regular carry-jump slice contains a genuine marked length-`m` chain;
- any deterministic quotient exact for terminal carry is injective on that
  chain;
- any exact deterministic quotient for current `epsilon4` already carries the
  canonical clock `beta`;
- if that quotient also retains grouped base `G`, then every theorem-side
  `(G,beta)` readout descends.

So the remaining M3 issue is not “why should the clock descend?” and not “why
should odd `m` force size `m`?”

The remaining issue is only:

> what exact quotient is the downstream local/admissible mechanism actually
> implementing?

At theorem level the safest frozen answer is still:

```text
Q_int = exact deterministic quotient on the exact marked object
        that retains grouped base G.
```

This is the object that matches the logic of `105`.

By contrast, the dynamic bridge

```text
Q_dyn = (beta,q0,sigma)  ~=  (beta,delta)
```

is the strongest checked splice-compatible coordinate model for current-event
and successor behavior on the extracted state-chain object. It is the right
comparison target, but it is not yet the honest literal definition of the
theorem-side intended quotient.

## 2. What the regenerated comparison check actually says

The script
[../../scripts/torus_nd_d5_intended_quotient_compare_106.py](../../scripts/torus_nd_d5_intended_quotient_compare_106.py)
extracts the regenerated carry-jump-to-wrap state-chain object from the active
rows and compares four keys:

- theorem key:
  `(B,beta)`
- dynamic bridge:
  `(beta,q0,sigma)` or `(beta,delta)`
- enriched dynamic bridge:
  `(rho,beta,q0,sigma)`
- weaker enrichment:
  `(family,beta,q0,sigma)`

The saved summary is
[../checks/d5_106_intended_quotient_compare_summary.json](../checks/d5_106_intended_quotient_compare_summary.json),
and the detailed per-modulus output is in
[../checks/d5_106_intended_quotient_compare/details.json](../checks/d5_106_intended_quotient_compare/details.json).

### 2.1 Positive exactness

For each checked modulus `m=13,15,17`:

- the dynamic bridge `(beta,q0,sigma)` is exact for current `epsilon4`;
- it is exact for the short-corner detector;
- it is deterministic on the nonterminal successor;
- the decorated quotient `(beta,a,b)` also passes those same three checks on
  the extracted state-chain object.

So the dynamic bridge really is the right downstream splice-compatible finite
object.

### 2.2 Factor map from theorem key to dynamic bridge

For each checked modulus:

```text
(B,beta)  ->  (beta,q0,sigma)
```

is exact. There are zero theorem-to-dynamic collisions in the regenerated
comparison.

So the theorem-side key already determines the dynamic bridge state. This is
the checked form of the desired factor map

```text
Q_int  ->  Q_dyn.
```

### 2.3 The reverse direction fails for a real reason

For each checked modulus:

- every dynamic key bucket is ambiguous as a theorem-side state;
- the number of ambiguous dynamic buckets is exactly `m^3`;
- the bucket sizes lie in `{m-5, m-4, m-3}` on the checked range.

Concretely:

| `m` | dynamic buckets | ambiguity-size histogram |
| --- | ---: | --- |
| `13` | `2197 = 13^3` | `8:117, 9:1456, 10:624` |
| `15` | `3375 = 15^3` | `10:165, 11:2370, 12:840` |
| `17` | `4913 = 17^3` | `12:221, 13:3604, 14:1088` |

So the dynamic bridge is not missing an occasional edge case. It
systematically forgets a full source-residue bookkeeping layer.

### 2.4 `rho` repairs exactly the lost information

For each checked modulus:

```text
(rho,beta,q0,sigma)  ->  (B,beta)
```

is exact, while

```text
(family,beta,q0,sigma)  ->  (B,beta)
```

is not exact.

So the comparison is very sharp:

- the dynamic bridge loses source-residue bookkeeping;
- family alone is not enough to recover it;
- source residue `rho` is enough.

This is the checked reason to phrase the comparison as

```text
(B,beta)  ~=  (rho,beta,q0,sigma)
```

on the extracted exact marked object.

## 3. What should be proved next

The next theorem package should not try to prove a global identity

```text
Q_int = (beta,delta)
```

because that overstates what the checked data supports.

The right target is a three-step comparison theorem.

### 3.1 Identification lemma on the exact marked object

Prove that on the exact marked carry-jump-to-wrap object, the descended
theorem-side data `(G,beta)` already determines the dynamic digits
`(q0,sigma)`.

This is the symbolic version of the checked map

```text
(B,beta)  ->  (beta,q0,sigma).
```

### 3.2 Source-residue ambiguity lemma

Prove that the only additional bookkeeping forgotten by the dynamic bridge is
the source residue `rho`.

This is the symbolic version of the checked equivalence

```text
(B,beta)  ~=  (rho,beta,q0,sigma),
```

and it is exactly the place where “two parameterizations are essentially the
same” should be stated.

### 3.3 Downstream factor theorem

Then state the intended quotient theorem in the right order:

1. `Q_int` retains grouped base and is exact for current `epsilon4`;
2. therefore `beta` descends by `105`;
3. therefore `(q0,sigma)` descends on the exact marked object;
4. hence `Q_int` factors canonically to the dynamic bridge
   `(beta,q0,sigma)` / `(beta,delta)`;
5. after adjoining `rho` or fixing a splice-connected source/component, the two
   parameterizations are equivalent.

This is the honest closure of full M3.

## 4. Bottom line

The current answer is now precise.

- The downstream intended quotient should still be formulated theorem-side as an
  exact deterministic quotient retaining grouped base.
- The dynamic bridge `(beta,q0,sigma)` / `(beta,delta)` is the right checked
  comparison target, not yet the literal global definition of the intended
  quotient.
- The two parameterizations are **not** globally identical as raw state spaces.
- They **are** checked to become equivalent after adjoining source residue
  `rho`.

So the right next theorem is not “prove the intended quotient is exactly
`(beta,delta)`.” It is:

> prove the comparison theorem
> `Q_int ~= (rho,beta,q0,sigma)` on the exact marked object, and then factor to
> `(beta,delta)`.
