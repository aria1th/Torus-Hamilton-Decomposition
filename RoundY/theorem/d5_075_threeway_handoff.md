# D5 Three-Way Handoff 075

This note supersedes the older `071` bridge split for active work.

After the `074` round, the live D5 frontier is best organized into:

1. bridge theorem
2. realization integration
3. compute validation

with a separate reviewer role for global critique and hidden-assumption checks.

## 1. Current position

The D5 theorem package is no longer the main open branch.

What is already compressed enough:

- structural chain through the phase-corner theorem
- per-chain exact marked-chain rule
- coarse bridge at carry / distance-to-endpoint level
- conditional corner-time realization theorem

The old bridge candidates have now split cleanly:

- bare `beta` bridge: too coarse for current `epsilon4`
- static decorated bridge `(beta,a,b)`: exact on each chain, but not
  splice-compatible as a deterministic global quotient
- dynamic bridge `(beta,q,sigma)` or equivalently `(beta,delta)` with
  `delta = q + m sigma`: best current candidate

So the main open question is no longer whether any bridge exists.
It is whether the **dynamic boundary-odometer bridge** is the correct exact
global object and can be proved uniformly from the D5 structure.

## 2. Accepted working picture

Treat the following as the current working picture.

### 2.1 Coarse bridge

At the carry / endpoint-distance level, the per-chain quotients already glue.
There is a global coarse `beta` clock.

### 2.2 Dynamic splice state

The first splice-compatible exact bridge supported by the checked data is

`(beta,q,sigma)`,

equivalently

`(beta,delta)` with `delta = q + m sigma mod m^2`.

Here:

- `beta` is the coarse global clock
- `q` is the normalized carry-slice coordinate
- `sigma = source_u + w mod m` is the splice phase

The checked splice law is:

`(q,sigma) -> (q+1, sigma + 1_{q=m-1}) mod m`

equivalently

`delta -> delta + 1 mod m^2`

at the splice, while `delta` is fixed inside each chain.

### 2.3 Event readout

Current `epsilon4` is supported on the checked range by the readout:

- `carry_jump` at `beta = m-1`
- `wrap` at `beta = 0`
- `other_1000` at `beta = m-2` iff `q = m-1`
- `other_0010` at `beta = m-3` iff
  `(q + sigma = 1 mod m)` or `(q = m-1 and sigma != 1)`
- otherwise `flat`

So the missing data are now concentrated in a concrete splice phase, not in an
opaque large controller.

### 2.4 Realization theorem

Once a deterministic global quotient is exact for current `epsilon4`, the
short-corner detector descends automatically, and the canonical clock descends
by corner-time modulo `m`.

The strongest current version no longer needs uniqueness of a short-corner
state on each component; recurrence of the descended short-corner set is
enough.

## 3. What is still not proved

The remaining gaps are now narrow.

### 3.1 Bridge theorem gap

The dynamic bridge `(beta,q,sigma)` / `(beta,delta)` is strongly supported, but
its splice law and current-event readout are still only checked on saved data.
What is missing is a **uniform D5 proof** from the structural chain.

### 3.2 Accessible subset gap

The exact accessible subset `A` of boundary states is not yet cleanly packaged.
For small `m`, especially `m=5`, the saved sample is not the full symbolic
odometer grid. So the right theorem must distinguish:

- full symbolic boundary odometer
- actually accessible splice-invariant subset

### 3.3 Minimality gap

The checked symbolic model says no smaller deterministic exact quotient is
visible than `(beta,q,sigma)`, but this is still a checked-range support
statement, not a uniform theorem.

## 4. Three active jobs

### Job 1: Bridge theorem

Prove the dynamic boundary-odometer bridge uniformly from the D5 structure.

Target:

- identify the correct boundary state
- prove the splice update law
- prove current `epsilon4` readout from that state
- package the exact accessible subset

### Job 2: Realization integration

Integrate the abstract corner-time realization theorem with the dynamic bridge.

Target:

- state the realization theorem directly for the final bridge object
- isolate the exact hypotheses that are still needed
- connect the theorem package to the bridge theorem cleanly

### Job 3: Compute validation

Support or break the dynamic bridge, not broader old candidates.

Target:

- stress-test `(beta,q,sigma)` / `(beta,delta)`
- clarify the accessible subset
- extend support beyond the frozen checked range when safe
- find the first genuine contradiction if the model fails

## 5. Reviewer role

The reviewer should not compete with the three active jobs.

The reviewer should instead ask:

- where does the current argument still rely on checked data rather than proof?
- is the bridge state really canonical, or just one convenient parameterization?
- are there hidden assumptions about accessibility, recurrence, or component
  structure?
- does the realization theorem still hide any uniqueness assumptions in its
  normalization?

## 6. Bottom line

The D5 frontier is now much narrower than before:

> the likely correct exact bridge is a dynamic boundary odometer
> `(beta,q,sigma)` / `(beta,delta)`, and the remaining work is to prove that
> bridge uniformly, integrate the realization theorem with it, and validate the
> accessible exact reduction object.
