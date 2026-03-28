# d=5 gap audit after the visibility local closure (2026-03-27)

## 0. What changed in this pass

The full-gate double-top slice

```text
C_m^{full,top} = {c=m-2, d=m-1, e=m-1}
```

was the last explicitly isolated local proof debt in the visibility compact-machine program.
The note

```text
d5_full_gate_doubletop_slice_proof_closure_2026-03-27.md
```

now proves that law (in fact for all `t notin {0,2}`), so the local visibility chain is closed.

---

## 1. What is now in theorem-order inside the current chain

The present bundle now contains theorem-order writeups for the local pieces below.

### 1.1. Control / bulk / compact-return side

- promoted-control low-band cocycle closure,
- universal lower-strip kinematics and first-return time `=m`,
- anomaly-free compact `c=0` return law in the coordinate
  ```text
  A = a - 1[e=m-1].
  ```

### 1.2. Hinge / corner / top-row side

- hinge conveyor,
- corner burst atlas,
- `t!=0` top-row transducer packet,
- `t=0` top-row early cascade,
- `t=0` global compact law,
- double-top / `Omega_m` symbolic law,
- full gate including the double-top slice,
- universal `U -> H` compact bridge,
- actual-entry atlas.

### 1.3. Visibility reduction side

- corrected first-top-hit reduction,
- explicit actual-entry atlas,
- compact visibility machine assembly.

So the corrected induced visibility map

```text
widehat G_t : widehat E_t -> widehat E_t cup B_m
```

is now assembled entirely from proved local components.

---

## 2. What is still not proved in the current chain

### 2.1. Arithmetic/global visibility

The next unresolved step is no longer local selector analysis.
It is the arithmetic analysis of the reduced compact machine:

- acyclicity / cycle structure of `widehat G_t`,
- identification of base windows along compact cycles,
- proof that every orbit meets one of those windows in the splice-safe regimes.

This is the main remaining visibility theorem.

### 2.2. Existence of splicers / base single-cycles

Independently of visibility, the broader existence-first program still needs the resonant existence step:

- existence of `B_m` single-cycle witnesses (or an equivalent splice certificate)
  in the target residue classes.

That is not a local law problem; it is a global existence problem.

---

## 3. Dependency audit

The current chain is **not** first-principles self-contained from the raw dynamics upward.
It still imports several March 25 baseline theorem packets, most importantly:

- the width-1 section-return theorem,
- the promoted-collar complete local dynamics packet,
- the promoted-control lower scattering / low-band packet.

However:

- these imported packets are now included in the archive as baseline dependencies,
- the newer March 26–27 notes make explicit exactly where those inputs are used,
- and no further hidden local inputs are currently being used on the visibility side.

So the remaining gap is not “there might be another missing local lemma”.
The remaining gap is global/arithmetic.

---

## 4. Bottom line

After the full-gate closure, the current proof state is:

- **local visibility mechanics:** closed at theorem-order, modulo the already-included March 25 baseline packets;
- **remaining open work:** arithmetic acyclicity / base-window analysis of `widehat G_t`, and resonant splice existence.

That is the cleanest honest summary of where the project stands today.
