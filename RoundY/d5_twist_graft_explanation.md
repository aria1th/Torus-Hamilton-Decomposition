# D5 Twist Graft Explanation

Status:
- explanatory diagnosis from Sessions `008` and `009`
- intended as a clean reading of the data, not yet a proved theorem

## One-sentence summary

The clean way to read Sessions `008` and `009` is:

**the current layer-3 predecessor gadget is a twist / holonomy gadget, not a cycle-compression gadget.**

It can turn monodromy on and off, and it can choose the monodromy value, but it does not change the underlying `U_0` cycle partition.

## The right decomposition

There are really two mechanisms in play.

1. The layer-2 seed chooses the **base return geometry**.
2. The layer-3 predecessor gadget chooses the **twist carried around that geometry**.

The evidence says these two mechanisms are largely decoupled in the current family.

More concretely:

- the layer-2 seed controls the orbit partition of the induced `U_0` map;
- the layer-3 gadget contributes an additive monodromy on those cycles;
- but the current gadget does not seem to alter which `U_0` cycles exist.

So the current mixed witnesses should be thought of as a skew-product:

\[
\text{base cycle map} \;+\; \text{cycle holonomy}
\]

rather than as a genuinely new coupled geometry.

## Why Session 008 already suggested this

Session `008` found the first mixed regime.

Exact facts:

- all `24` mixed survivors had the same pilot cycle profile:
  - `m=5`: `5` cycles of length `5`
  - `m=7`: `7` cycles of length `7`
  - `m=9`: `9` cycles of length `9`
- the only thing that changed across those mixed survivors was the monodromy value:
  - ordered pair `(0/3,3/0)` gave `-2 mod m`
  - `(3/0,0/3)` gave `+2 mod m`
  - `(0/3,3/3)` and `(3/3,3/0)` gave `-1 mod m`
  - `(3/0,3/3)` and `(3/3,0/3)` gave `+1 mod m`

So already in `008`, the ordered layer-3 slice pair was controlling a **twist parameter** while leaving the cycle profile unchanged.

That is exactly what a cocycle / holonomy gadget looks like.

## What Session 009 clarified

Session `009` asked the right next question:

can the exact Session `008` twist gadget be transplanted onto stronger cycle seeds?

The answer is subtle but very clean.

### Stage 1

On the representative layer-3 old bit `q=-1`:

- almost every tested layer-2 seed preserved mixed behavior;
- the only failures were the strongest alt-`4` cycle seeds, which stayed cycle-only.

But even when twist survived, **none** of the mixed survivors beat the old mixed baseline:

\[
U_0 = m \text{ cycles of length } m.
\]

So twist survived, but cycle compression did not come with it.

### Stage 2

Stage 2 widened the layer-3 old bit to

\[
\{q=-1,\ q+u=1,\ q+u=-1,\ u=-1\}.
\]

This restored mixed behavior even on the alt-`4` seeds:

- `q=-1` alt `4` and `w+u=2` alt `4` became mixed for layer-3 bits
  - `q+u=1`
  - `q+u=-1`
  - `u=-1`

But the cycle profile still did not move.

So Stage 2 proved something stronger than “the first graft failed”:

**even when the twist is successfully transplanted onto the strong cycle seeds, the current gadget still does not modify the underlying cycle geometry.**

## Clean conceptual picture

The current family seems to have the following structure.

### A. Layer 2 chooses the base partition

The layer-2 seed determines which `U_0` cycles exist.

In the strong-cycle seeds, this is where the interesting compression lives.

### B. Layer 3 chooses the holonomy on that partition

The predecessor-based layer-3 switch decides whether the monodromy on those cycles is:

- zero,
- `\pm 1`,
- or `\pm 2`.

That is why:

- the same ordered slice pair always gives the same monodromy law;
- changing the predecessor flag between `pred_sig1_wu2` and `pred_sig4_wu2` does not change the monodromy law;
- widening the layer-3 old bit can turn mixed behavior on for a seed that previously stayed cycle-only.

### C. But the current gadget does not perturb the base partition

This is the key point.

Across the successful mixed rules, the cycle profile is rigid:

- once a seed lands in the mixed regime, it lands in the same simple `m`-cycle regime;
- the twist changes the holonomy class, not the orbit partition.

So the current graft is not “cycle seed plus twist plus interaction.”

It is better read as:

\[
\text{base return map} \quad \text{plus a holonomy decoration}.
\]

## The clean language to use

If we want one short phrase that explains Sessions `008` and `009`, I would use:

**The current predecessor gadget controls holonomy, not geometry.**

Equivalent phrasing:

- it is a **twist gadget**, not a compression gadget;
- it changes **monodromy**, not the **cycle partition**;
- it behaves like a **cocycle over a fixed base map**, not like a coupled perturbation of the base map itself.

## Why this is useful

This explanation tells us what not to do next.

It says the current problem is probably **not**:

- finding yet another one-bit layer-3 predecessor flag;
- or widening the same twist gadget a little more.

Those moves are good at changing holonomy, and the data say they are already very good at that.

The remaining problem is to make the twist talk to the base geometry.

## What the next successful mechanism would have to do

A stronger mixed witness probably needs one of the following.

1. A layer-3 rule that depends on where one sits inside the compressed layer-2 geometry, not just on the current predecessor flag.
2. A genuinely coupled layer-2/layer-3 gadget that changes the base return map itself.
3. A theorem showing that the current twist-graft family is forced to keep the `m`-cycle mixed profile.

So the next useful branch is not “more holonomy control.”

It is either:

- **interaction**, or
- **classification**.

## Suggested theorem-level statement

A clean theorem target suggested by the data would be:

> In the current twist-graft family, the predecessor-based layer-3 gadget can change the monodromy carried by a `U_0` cycle, but it cannot change the `U_0` cycle partition beyond the existing layer-2 base regimes.

That is not proved yet, but it is the clean mathematical statement that the search data are pointing toward.

## Bottom line

Sessions `008` and `009` should be explained as follows:

- Session `008` found the first nontrivial holonomy gadget.
- Session `009` showed that this gadget is robust and portable.
- But Session `009` also showed that portability of twist is not the same as compression of cycles.

So the real remaining bottleneck is:

**how to make holonomy interact with geometry.**
