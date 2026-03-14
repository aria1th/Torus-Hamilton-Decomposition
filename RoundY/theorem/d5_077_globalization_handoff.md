# D5 Globalization Handoff 077

This note is the current researcher-facing handoff after accepting the `076`
bridge / realization / compute round.

It is meant for a new collaborator who does **not** need the full history.
The goal is to explain only:

- what is now accepted,
- what is still open,
- what the precise problem is,
- and what kinds of work are now useful.

## 1. Current status

For odd `m` in `d=5`, the branch is no longer looking for the right local rule.
The likely rule shape is already visible:

- one canonical phase clock `beta`,
- one boundary memory state,
- corner-time realization once current `epsilon4` is exact on the final bridge.

The theorem package up to the phase-corner theorem is no longer the main
frontier. The per-chain marked-chain rule is no longer the main frontier. The
coarse bridge is no longer the main frontier.

The live issue is now a single narrow bridge question:

> does the concrete boundary odometer label `delta` globalize across the full
> accessible union, or is the true exact bridge only the abstract
> right-congruence object `rho`?

## 2. What is accepted

### 2.1 Structural package

The accepted structural chain through the phase-corner theorem gives:

- the active regular dynamics are organized by the clock `beta`,
- countdown/reset behavior is controlled by the phase-corner scheduler,
- the per-chain dynamics are exact marked length-`m` chains.

### 2.2 Abstract bridge

The safest current theorem-level bridge is

`(beta,rho)`,

where `rho` is the boundary right-congruence class of the padded future current
event word.

This bridge is canonical, minimal, deterministic, and exact for current
`epsilon4`.

### 2.3 Abstract realization theorem

On the abstract bridge:

- the canonical clock already descends as the first coordinate `beta`,
- the short-corner detector descends automatically,
- recurrence is only needed to characterize the clock by corner-time.

### 2.4 Best concrete coordinate model

The strongest current concrete candidate is

`(beta,q,sigma)`,

equivalently

`(beta,delta)` with `delta = q + m sigma`.

Componentwise, this model now has a strong theorem-style package:

- uniform splice law,
- uniform current-event readout,
- orbit-segment description of the component boundary image.

## 3. What is still open

The remaining open problem is **globalization**.

Componentwise, the concrete odometer bridge appears correct. Globally, there is
still one possible obstruction:

> can the same realized `delta` occur in two different accessible components
> with different padded future current-event words?

If the answer is **no**, then raw global `(beta,delta)` is the correct exact
bridge.

If the answer is **yes**, then the correct final theorem object remains the
abstract bridge `(beta,rho)`, and `(beta,delta)` is only a componentwise chart.

So the real question is no longer bridge existence. It is:

- raw global `delta`, or
- abstract `rho` with only componentwise concrete identification.

## 4. What the current evidence says

The current support picture is:

- componentwise `rho <-> delta` is strongly supported;
- the concrete bridge survives the direct frozen-row checks;
- the accessible boundary image is already the full `m^2` grid on the checked
  larger range;
- the only observed ambiguity mechanism is terminal/component ambiguity on
  disjoint finite component proxies;
- there is no observed local event-readout ambiguity at fixed `delta`.

So the evidence does **not** currently suggest that the concrete odometer is
wrong. It suggests only that the global union may need a component tag unless
one proves that the actual accessible union is already one suitable total
component, or otherwise component-independent at fixed `delta`.

## 5. Precise problem statement

The main current D5 problem is:

> prove or disprove that on the full accessible regular union, the padded
> future current-event word attached to a realized `delta` depends only on
> `delta` and not on the accessible component in which it is realized.

Equivalent formulations:

- does raw global `(beta,delta)` define an exact deterministic quotient?
- is the abstract bridge `(beta,rho)` globally identified with the concrete
  odometer bridge `(beta,delta)`?
- does the concrete odometer require a component tag?

## 6. Useful directions

Only three directions are now useful.

### 6.1 Global component structure

Prove the actual splice-connected structure of the accessible regular union.
This is the cleanest way to settle whether component ambiguity is real or only a
proxy artifact.

### 6.2 Globalization criterion

Work directly with the criterion:

- fix a realized `delta`,
- compare all accessible occurrences of that `delta`,
- decide whether their padded future current-event words always agree.

### 6.3 Targeted compute support

Only run compute that addresses:

- fixed-`delta` ambiguity on true accessible unions,
- accessible-image closure,
- larger-odd-`m` support for or against raw global `(beta,delta)`.

No broad controller search is useful now.

## 7. What should not be reopened

Do not reopen:

- broad witness search,
- old tiny-controller or tiny-decoration scans,
- general odd-`d` speculation,
- even-`m` speculation,
- theorem-side phase-corner discovery work.

Those are no longer the active bottlenecks.

## 8. Reading order

For a new researcher, the shortest reading path is:

1. this note;
2. `RoundY/theorem/d5_076_unified_handoff.md`;
3. `tmp/d5_076_bridge_main.md`;
4. `tmp/d5_076_realization_trackB.md`;
5. `tmp/d5_076_concrete_bridge_proof.md`;
6. `tmp/d5_076_track_c_compute.md`.

Then read only the bundled data / logs actually needed for the specific
question being worked on.

## 9. Bottom line

The D5 odd-`m` branch is now close in the following precise sense:

- the theorem package is mostly stabilized,
- the abstract exact bridge is in hand,
- the concrete odometer bridge is strong componentwise,
- and the remaining gap is one sharp globalization question.

That is the current frontier.
