# D5 079 Single Critical Lemma

This note records the accepted post-`079` frontier for odd `m` in `d=5`.

The main change after `079` is that the exceptional continuation is no longer
the main live gap. At chart / chain-label level it is now essentially fixed:

`3 -> (terminal chain of 4) -> 1`.

So the D5 frontier should now be treated as a **single-point globalization
problem**.

## 1. What is accepted now

The following should be treated as accepted working context.

### 1.1 Safe global theorem object

The safest global bridge remains the abstract exact bridge

`(beta,rho)`.

This is still the theorem object that can be stated globally without risk.

### 1.2 Concrete componentwise bridge

On each splice-connected accessible component, the strongest concrete bridge is

`(beta,delta)`,

equivalently `(beta,q,sigma)` with `delta = q + m sigma`.

Accepted componentwise package:

- uniform splice law,
- uniform current-event readout,
- component boundary image is a forward `+1` orbit segment in `Z/m^2 Z`.

### 1.3 What `078` and `079` now settle

Accepted reduction:

- local bridge discovery is over;
- fixed-`delta` ambiguity is no longer a local event-law issue;
- by the Track-B reduction, the only remaining possible ambiguity at fixed
  realized `delta` is **tail length / endpoint** ambiguity;
- the exceptional continuation is now strongly supported, and on the larger
  chart model is effectively forced, to pass through the interface
  `3m-2 -> 3m-1`, i.e.
  `3 -> (terminal chain of 4) -> 1`.

So the exceptional patched splice is no longer the main open branch.

## 2. Single critical lemma

The whole remaining globalization question is now concentrated in one lemma.

### Critical Lemma

For odd `m` in the D5 accessible union, if two realized boundary states have
the same concrete label `delta`, then they have the same remaining full-chain
tail length.

Equivalently:

- they have the same right endpoint;
- they have the same padded future current-event word;
- `rho` depends only on `delta`;
- raw global `(beta,delta)` is a valid exact bridge.

So the single remaining theorem-level question is:

> does fixed realized `delta` determine tail length on the full accessible
> union?

## 3. Equivalent final forms

The critical lemma can be stated in any of the following equivalent ways.

### 3.1 Endpoint form

For every realized `delta`, all actual accessible realizations of that `delta`
have the same right endpoint.

### 3.2 Future-word form

For every realized `delta`, all actual accessible realizations of that `delta`
have the same padded future current-event word.

### 3.3 Bridge form

Globally,

`rho = rho(delta)`.

### 3.4 Concrete bridge form

Raw global `(beta,delta)` is the final exact bridge, not just a componentwise
chart.

## 4. Why this is now the only live gap

After `079`, the remaining alternatives have been narrowed as follows.

- If the critical lemma is true, then the abstract global bridge `(beta,rho)`
  upgrades immediately to raw global `(beta,delta)`.
- If the critical lemma is false, then the final theorem should remain:
  global abstract `(beta,rho)`, componentwise concrete `(beta,delta)`.

There is no longer a separate live question about:

- the phase-corner machine,
- the chain rule,
- the local event readout,
- or where the exceptional splice lands in chart coordinates.

Those are no longer the bottleneck.

## 5. What each active line should now do

All active work should now be understood as attacking the same lemma from
different sides.

### Structure side

Show that the actual accessible union is one total component, or at least that
component overlaps cannot create different endpoints at fixed `delta`.

### Theorem side

Reduce the global theorem exactly to the critical lemma and keep the global
statement abstract until the lemma is proved.

### Compute side

Do not reopen local search.
Only test the critical lemma directly:

- repeated realized `delta` on actual larger unions,
- endpoint compatibility,
- explicit gluing of repeated realized `(beta,delta)` states.

## 6. Recommended theorem packaging right now

The safest current packaging is:

- global theorem: abstract `(beta,rho)`;
- componentwise theorem: concrete `(beta,delta)`;
- upgrade clause: if fixed realized `delta` determines tail length, then raw
  global `(beta,delta)` is exact.

## 7. Bottom line

Post-`079`, D5 odd `m` is no longer blocked by rule discovery.

The branch has reduced to one critical globalization lemma:

> same realized `delta` must imply same tail length.

That is the single point that now decides whether the final bridge is globally
raw `(beta,delta)` or globally abstract `(beta,rho)`.
