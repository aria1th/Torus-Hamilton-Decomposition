# D5 076 Concrete Bridge Proof

This note promotes the stable concrete-input package from the `076` bridge
line.

It isolates the concrete facts needed to pass from the abstract bridge
`(beta,rho)` to the componentwise odometer model `(beta,delta)`.

## 1. Intrinsic boundary digits

On the unique `Theta = 2` state `(q,w,u,2)` of a full regular chain, define

`sigma = w + u - q - 1 mod m`

and then define

`delta = q + m sigma`.

This is the intrinsic current-state version of the older source-residue
boundary coordinate.

## 2. Uniform splice law

### Theorem 2.1

Under first return to the `Theta = 2` section,

- `q' = q+1 mod m`,
- `sigma' = sigma + 1_{q=m-1} mod m`,
- hence `delta' = delta + 1 mod m^2`.

So consecutive full regular chains always satisfy the odometer splice law

`delta -> delta+1`.

## 3. Uniform current-event readout

Current `epsilon4` is a function of `(beta,delta)` alone.

Writing `delta <-> (q,sigma)`, define:

- `a = 1_{q=m-1}`,
- `b` as the accepted boundary bit that detects the `other_0010` corner.

Then the event law is:

- `beta = m-1` gives `carry_jump`,
- `beta = 0` gives `wrap`,
- `beta = m-2` gives `other_1000` iff `a=1`, else `flat`,
- `beta = m-3` gives `other_0010` iff `b=1`, else `flat`,
- all other positions are `flat`.

So `(beta,delta)` is exact for current `epsilon4`.

## 4. Componentwise image structure

On each splice-connected accessible component, the realized boundary labels form
one forward `+1` orbit segment in `Z/m^2 Z`.

That is the concrete bridge package used later in the globalization and
tail-length notes.

## 5. Promoted references

This note promotes the substance of:

- `tmp/d5_076_concrete_bridge_proof.md`
- `tmp/d5_076_track_c_compute.md`
