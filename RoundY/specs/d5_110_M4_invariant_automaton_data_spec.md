# D5 110: M4 Invariant-Automaton Data Spec

This spec answers the post-`110` question:

> what exact data would count as serious evidence for M4?

## Short answer

Current evidence is **not yet sufficient** for M4.

What is missing is not more prose about `(beta,delta)`, and not full
Hamilton-cycle output. What is missing is a finite-state packet that directly
matches the selector criterion of `108`.

The required packet should be built on the intended invariant state space
`I = (beta,delta)` or an explicitly equivalent normalization.

## Why `110` does not close M4

`110` sharpens M5 by showing that, once a graph-level factor map to the M3 base
exists, Hamiltonicity reduces to one fiber-return map on an `m^2`-point fiber.

That does **not** supply the graph witness descent package for M4. The missing
M4 content remains exactly the same as in `108`:

1. colorwise generator readouts `g_c(I)`;
2. predecessor transports `P_j(I)`;
3. the local inverse identity
   `#{j : g_c(P_j(I)) = j} = 1`.

So M4 still wants invariant-automaton data, not M5-style return data.

## Required packet

For each checked modulus `m`, the packet should contain five sections.

### 1. Invariant catalog

The realized invariant states.

Required fields:

- `state_id`
- `beta`
- `delta`

Optional but useful:

- a sample representative vertex
- a sample representative local witness record
- any equivalent coordinates used internally

### 2. Generator table

For each realized invariant state `I` and each color `c in {0,1,2,3,4}`,
record the chosen torus generator

`g_c(I) in {0,1,2,3,4}`.

This should be stored rowwise:

- one row per invariant state
- one length-5 array of generators ordered by color

The first mandatory summary is:

- each row must be a permutation of `{0,1,2,3,4}`.

### 3. Predecessor transport table

For each realized invariant state `I` and each generator `j in {0,1,2,3,4}`,
record

`P_j(I) = I(x - e_j)`.

This should also be stored rowwise:

- one row per invariant state
- one length-5 array of predecessor `state_id`s ordered by generator

The mandatory summary is:

- every predecessor target must be another realized invariant state.

### 4. Local inverse-identity table

For each realized invariant state `I` and color `c`, record the unique incoming
generator

`j = j(c,I)` such that `g_c(P_j(I)) = j`.

This should be stored rowwise:

- one row per invariant state
- one length-5 array ordered by color

The mandatory summary is:

- every entry is unique and lies in `{0,1,2,3,4}`.

### 5. Failure witnesses

If any of the above tables fail to close uniformly, include a small witness
section with:

- the failing modulus
- the invariant state
- the color / generator involved
- the conflicting values
- one or two sample representative vertices

If there are no failures, this section should be empty.

## Optional formula layer

If the tables suggest clean formulas, include:

- `formula_candidates`
- `formula_fit_summary`

for example affine or piecewise-affine descriptions of:

- `g_c(beta,delta)`
- `P_j(beta,delta)`
- `j(c,beta,delta)`

This is optional. The packet is already useful without closed formulas.

## Minimal acceptance criteria

An M4 packet is strong enough to send if, for each checked modulus:

1. the invariant catalog is complete on the realized state space;
2. every generator row is a permutation of `{0,1,2,3,4}`;
3. every predecessor row lands in the catalog;
4. the local inverse identity is unique at every state and color;
5. any failures are explicitly witnessed.

That is the smallest packet that directly supports the finite-state selector
criterion from `108`.

## What not to send instead

Do not substitute any of the following for the required packet:

- sampled torus arcs without invariant indexing
- only raw `(beta,delta)` exactness summaries
- only factor-cycle counts
- only Hamiltonicity statistics

Those may be useful later, but they do not answer the current M4 question.
