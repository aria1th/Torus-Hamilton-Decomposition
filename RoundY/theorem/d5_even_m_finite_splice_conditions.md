# D5 Even-`m` Finite-Splice Theorem: Necessary And Sufficient Conditions

This note clarifies what should count as the real proof target if the even
`d=5` branch is recentered around a finite-splice theorem.

The main distinction is:

- what may be necessary for the **truth** of the even theorem;
- what is necessary or sufficient for the **current proof method**.

Only the second question is presently answerable in a stable way.

## 1. The right reading of the target

The current even-`m` goal should not be phrased first as

> "find a witness that works after finitely many repairs".

The better theorem target is:

> find a reduced return object whose bulk law is odometric and whose
> non-generic behavior is confined to a finite splice set.

If such an object is proved, the remaining closure step should be a finite
combinatorial gluing argument, not an open-ended search.

So the central theorem object is a **finite-splice theorem on the reduced
return object**, not a raw move-level repair statement.

## 2. What is not actually necessary

The following are useful but should not be confused with logical necessities
for the even theorem itself.

### 2.1 Parity barrier

The parity barrier against Kempe-from-canonical is important because it tells us
to abandon the naive route.

But it is **not** necessary for the truth of the final even theorem.

It is a route-selection theorem:

- it shows one natural direct proof route cannot work;
- it does not by itself force the finite-splice route to be the only possible
  proof.

### 2.2 Exact odd formulas as written

The specific odd-branch formulas

- `s_u = m(u+2)-1`,
- `e_u = m(u-1)-2`,
- `u -> u-3`,
- `3m-3 -> 3m-2 -> 3m-1`

are best viewed as the current D5-shaped target, not as logically necessary
syntax.

A conjugate or equivalent reduced model would be just as good if it supplies
the same finite-splice structure.

## 3. Conditions that are close to necessary for the current proof method

For the present Route-E-style proof strategy, the following conditions are
close to necessary.

### 3.1 A reduced return object

There must be a section / return object on which the even problem becomes
visible as a deterministic reduced dynamics.

Without that, "finite splice" has no precise meaning.

### 3.2 Generic bulk law off a defect set

Outside a designated defect set, the successor law must collapse to one generic
odometer-like rule.

If non-generic behavior persists on a positive-density or unstructured part of
the section, then the proof is no longer a finite-splice proof.

### 3.3 Finite defect support

The non-generic part must be confined to:

- finitely many defect packets, or
- finitely many arithmetic family-block types, or
- a finite quotient carrying the entire splice ambiguity.

If the number of defect types grows with orbit history in an uncontrolled way,
the current method breaks.

### 3.4 A finite splice relation

The defect packets must induce a finite splice map or permutation on the block
labels.

This is what turns the closure step into a finite theorem rather than an
infinite itinerary analysis.

### 3.5 No persistent defect propagation

For this proof method, one must rule out the possibility that defects keep
generating new unresolved defects forever.

Equivalently, one needs a statement of the form:

> every non-generic continuation is confined to a fixed finite splice set, and
> defect packets do not propagate indefinitely outside that set.

This is the right replacement for the vague phrase
"it cannot require infinitely many repairs".

## 4. Strong sufficient package for the current D5 route

The strongest clean sufficient package currently visible is the package already
isolated in the even theorem note.

It has two layers.

### 4.1 Formal-extension sufficient package

It is sufficient to prove, on the true accessible boundary union:

1. the same first-exit theorem with universal targets;
2. the same componentwise concrete bridge
   `delta = q + m sigma` and splice law `delta' = delta + 1 (mod m^2)`;
3. the same tail-length reduction at fixed realized `delta`;
4. regular continuation for every realized regular label;
5. the same exceptional interface
   `3m-3 -> 3m-2 -> 3m-1`.

Then the odd final globalization proof carries over unchanged.

So this package is a **sufficient condition for the final even boundary
theorem**, relative to the accepted odd proof architecture.

### 4.2 Critical-row sufficient package

There is also a more D5-specific stronger sufficient package:

1. the regular sector splits into source windows `I_u`;
2. inside each `I_u`, the successor law is the generic odometer step
   `delta -> delta + 1`;
3. each regular window starts at `s_u` and ends at `e_u`, with
   `e_u + 1 = s_{u-3}`;
4. the unique missing source is `u = 3`;
5. the exceptional window ends at `3m-3` and continues through
   `3m-2 -> 3m-1`.

This stronger package automatically yields the formal-extension hypotheses, so
it is a concrete **sufficient condition for the current D5 even proof route**.

## 5. What should count as a reasonable contradiction target

The best contradiction target is not the sentence

> "infinitely many repairs are needed".

That is too informal.

The right contradiction targets are these.

### 5.1 Infinite defect support

If new non-generic rows keep appearing without collapsing to finitely many
packet types, then finite splice fails.

### 5.2 Mixed continuation status at a fixed reduced label

If the same reduced boundary label can be both continuing and terminal in
different actual realizations, then the finite-splice quotient is not exact
enough to close.

### 5.3 Recurrent unresolved defect packet

If a defect packet can recur without entering the generic bulk or a finite
splice cycle, then the defect dynamics are not well-founded.

### 5.4 Unbounded defect-memory growth

If the splice state must keep accumulating new memory rather than factoring
through a finite defect quotient, then the theorem is not a finite-splice
theorem in the current sense.

So a proof that

- defect support is finite,
- bulk law is generic outside it, and
- no persistent defect propagation occurs

is exactly the right way to exclude the "infinite repair" scenario.

## 6. Best current judgment

For the present D5 even program:

- **likely necessary for this proof method:** reduced section, generic bulk
  law, finite defect support, finite splice map, no persistent defect
  propagation;
- **strong sufficient package:** the critical-row package above;
- **not necessary in itself:** parity barrier, or the exact odd-coordinate
  formulas as syntax.

So the clean current theorem goal is:

> prove a finite-splice theorem on the even reduced return object, ideally in
> the critical-row form, and prove a no-persistent-defect-propagation lemma on
> that object.

## 7. Bottom line

The correct even-`m` D5 proof target is:

1. a reduced return object;
2. generic odometer bulk outside a finite defect set;
3. a finite splice theorem on the defect packets;
4. a no-persistent-defect-propagation lemma.

That package is strong enough to make

> "finite repair works"

mathematically precise, and it gives the right contradiction framework for
ruling out

> "repair would have to continue indefinitely".
