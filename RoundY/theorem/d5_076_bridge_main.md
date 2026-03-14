# D5 076 Bridge Main

This note promotes the stable `076` bridge theorem package from `tmp/` into the
RoundY theorem record.

Its purpose is to freeze the two-layer bridge picture:

1. the globally safe abstract bridge `(beta,rho)`;
2. the componentwise concrete bridge `(beta,delta)`.

## 1. Abstract bridge theorem

### Theorem 1.1

On the accessible union of full regular carry-to-wrap chains, there is a
canonical minimal exact partial deterministic bridge

`(beta,rho)`,

where:

- `beta` is the phase-corner clock on the current full chain;
- `rho` is the boundary right-congruence class of the padded future
  current-event word.

This bridge is globally unconditional.

### Meaning

The abstract bridge solves the existence problem once and for all. Even if the
best concrete coordinates later need a component tag or an abstract accessible
subset, the safe theorem object remains `(beta,rho)`.

## 2. Concrete componentwise bridge

### Theorem 2.1

On each splice-connected accessible component, the abstract bridge is realized
concretely by

`(beta,delta)`,

equivalently by `(beta,q,sigma)` with

`delta = q + m sigma`.

On that component:

- the boundary successor is `delta -> delta+1`;
- current `epsilon4` is read exactly from `(beta,delta)`;
- the boundary image is one forward `+1` orbit segment in `Z/m^2 Z`.

### Meaning

The concrete bridge is accepted componentwise. The only remaining global
question is whether the same raw `delta` can be used without a component tag on
the full accessible union.

## 3. Accessible-image theorem

### Theorem 3.1

On each splice-connected accessible component, the realized boundary image is a
forward orbit segment of the odometer step `+1` on `Z/m^2 Z`.

So each component boundary image is either:

- a finite interval of length `< m^2`, or
- the full odometer cycle of length `m^2`.

### Frontier left by 076

The remaining globalization issue is not bridge existence and not local
readout. It is:

> can two different accessible components realize the same `delta` with
> different padded future current-event words?

Equivalently:

> is `rho` globally a function of `delta`?

## 4. Promoted references

This note promotes the substance of:

- `tmp/d5_076_bridge_main.md`

The concrete input package used here is promoted separately at:

- `theorem/d5_076_concrete_bridge_proof.md`

The realization packaging is promoted separately at:

- `theorem/d5_076_realization_trackB.md`
