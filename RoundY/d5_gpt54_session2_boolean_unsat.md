# d=5 progress note v4

Problem:
Prove the `d=5` case: for every `m >= 3`, the directed torus
`D_5(m) = Cay((Z_m)^5, {e_0,e_1,e_2,e_3,e_4})`
admits a Hamilton decomposition into five arc-disjoint directed Hamilton cycles.

Current target:
1. Close the odd-`m` pilot first.
2. Convert the successful `m=5` evidence into a symbolic return-map rule in the color-covariant frame
   `(q_c,w_c,v_c,u_c) = (x_{c+1},x_{c+2},x_{c+3},x_{c+4})`.
3. Identify the smallest symbolic family that survives the new obstruction found below.

Known assumptions:
- [P] The low-layer clock must be `S mod m`, not the ordinary integer sum `S_Z`.
- [P] The correct odd-`m` base bulk is:
  - layer `S=0`: color `c` uses `+e_{c+1}`,
  - layers `S=1,...,m-1`: color `c` uses `+e_c`.
  Then pure bulk first return gives `Δx = e_{c+1} - e_c`, hence `Δq_c = 1` and `Δw_c = Δv_c = Δu_c = 0`.
- [C] There is a valid `m=5` low-layer Kempe witness with cycle counts `[1,1,1,1,1]`.
- [C] The same 26-move template on `m=7` gives cycle counts `[5,433,1,1,3]`.
- [P] Even `m` cannot be handled by a canonical-start Kempe-only proof because of the odd-`d` sign-product obstruction.

Attempt A:
  Idea:
  Use absolute low layers cut out by the ordinary integer sum `S_Z <= 3`.

  What works:
  - The defect region is finite and easy to parameterize.

  Where it fails:
  - [F] Topological shattering: for `m >= 5`, most bulk orbits never hit that defect set at all.
  - [F] So many color orbits remain trapped in short isolated cycles; Hamiltonicity is impossible.

Attempt B:
  Idea:
  Use the residue clock `S mod m` with the color-covariant charge frame
  `q_c = x_{c+1}`, `w_c = x_{c+2}`, `v_c = x_{c+3}`, `u_c = x_{c+4}`,
  and try to realize the three carries on layers `1,2,3` by a rotationally symmetric Boolean zero-pattern rule.

  What works:
  - [P] The base first return is exactly the desired `q_c -> q_c + 1` bulk shift.
  - [H] This is the cleanest possible odometer architecture.
  - [C] The compressed model becomes a tiny discrete CSP: layers `1,2,3`, each depending only on `B in {0,1}^5`, with rotational covariance and the local permutation constraint.

  Where it fails:
  - [F] The whole `96`-variable Boolean-layer model is already UNSAT at `m=5`.
  - [P] In fact the contradiction appears before layer 2 is even assigned:
    every encountered layer-1 zero-pattern orbit is forced to the default output `0` for color 0.
  - [P] Reason: on a length-5 orbit, rotational covariance means the layer-1 outputs come from a permutation `π in S_5`, so color-0 outputs are `g_s = π(c)-c` along the orbit.
    The odometer target allows only `0` or `2` on layer 1.
    Therefore `π(c)-c in {0,2}` for all `c`, which forces `π(c)=c` for all `c` or `π(c)=c+2` for all `c`.
    But every encountered orbit contains at least one non-carry state that forces output `0`, so the global shift `c -> c+2` is impossible.
    Hence only the identity remains, i.e. layer 1 is forced to be default on every encountered Boolean state.
  - [P] Now take the start
    `x* = (3,4,4,4,0) in P_0`.
    After the fixed layer-0 step, the desired odometer target still needs three extra directions `[2,3,4]`.
    Since layer 1 is forced to be default and only layers 2 and 3 remain nontrivial, this is impossible.
    So the Boolean zero-pattern model cannot work.

Attempt C:
  Idea:
  Keep the residue clock and the color-covariant odometer frame, but enrich the symbolic state beyond Boolean zero-patterns.
  The `m=5` Kempe witness suggests that one-coordinate affine pinning (`x_i = const`) is the right next level.

  What works:
  - [C] The known `m=5` witness uses many pinned constants `0,1,2,3,4` on low layers, exactly the kind of information absent from Attempt B.
  - [H] These constants likely represent transported zero-tests after unfolding the relative coordinates back into the absolute frame.
  - [H] This removes the orbit-collapse obstruction from Attempt B by breaking the forced dichotomy
    `π = id` or `π = shift by 2` on layer 1.

  Where it fails:
  - [O] We do not yet have the explicit affine-pinned symbolic rule.
  - [O] The current witness file records the Kempe move sequence but not yet the compact relative-coordinate formula.

Candidate lemmas:
- [P] `S_Z <= 3` low-layer support is impossible for `m >= 5`.
- [P] The rotational Boolean-layer model on layers `1,2,3` is UNSAT already at `m=5`.
- [P] Therefore any successful odd-`m` symbolic rule must use more than Boolean zero-pattern data.
- [H] The minimal successful enrichment is likely a small affine-pinned state model on layers `1,2,3`, still with rotational covariance.
- [H] The successful `m=5` Kempe witness should compress to such an affine-pinned model when rewritten in the `(q_c,w_c,v_c,u_c)` frame.

Needed computations/search:
- [C] Decode the `m=5` Kempe witness into the actual direction tuple rule and rewrite it in relative coordinates.
- [C] Fit the resulting rule to a small affine-pinned template:
  layer `L` depends on a few one-coordinate tests `x_i = a_{L,i}` or relative tests `q_c = α`, `w_c = β`, `v_c = γ`.
- [C] Search the enriched affine-pinned model on `m=5,7`.
- [C] Once a candidate is found, use symbolic extraction of `R_c` and `T_c` to check affine conjugacy to the 3D odometer.
- [C] For even `m`, separate Route-5E search remains necessary.

Next branching options:
1. Decode the existing `m=5` witness into an explicit low-layer rule and infer the affine-pinned conditions it is really using.
2. Build a SAT / CP-SAT model for the affine-pinned layer family (Boolean model is now ruled out).
3. Try to hand-prove that any rotationally symmetric odd-`m` witness must use affine priorities on multiply-zero layer-1 states.
4. Start the even-`m` obstruction/repair branch in parallel.

Claim status labels:
  [P] proved
  [C] computationally verified
  [H] heuristic / design principle
  [F] ruled out in the stated scope
  [O] open

Codex template for larger computing:

Task ID:
D5-AFFINE-PINNED-CASCADE-002

Question:
Find an explicit odd-`m` d=5 low-layer rule on the residue clock `S mod m` whose first return is affine-conjugate to a 3-carry odometer, after enriching the state beyond Boolean zero-patterns.

Purpose:
Replace the now-ruled-out Boolean-layer model by the smallest affine-pinned symbolic family that can reproduce the successful `m=5` witness and extend to `m=7` and general odd `m`.

Inputs / Search space:
- dimension `d=5`
- odd moduli `m in {5,7,9}` first
- layer `0`: fixed bulk `+e_{c+1}`
- layers `1,2,3`: default `+e_c`, plus low-layer corrections
- rotational covariance under simultaneous index shift
- symbolic conditions allowed to use:
  - one-coordinate equalities `x_i = a`
  - relative-coordinate equalities `q_c = a`, `w_c = b`, `v_c = c`
  - small ordered priority rules when several colors are simultaneously eligible

Allowed methods:
- SAT / CP-SAT / MILP
- brute force with symmetry reduction
- witness decoding from the known `m=5` Kempe sequence
- symbolic return-map extraction
- affine-conjugacy tests to the 3D odometer
- proof-supporting computation with fixed seeds and full logs

Success criteria:
1. Recover an explicit affine-pinned rule that matches the known `m=5` witness or improves on it.
2. Verify cycle counts `[1,1,1,1,1]` on `m=5` and the same on `m=7`.
3. Extract `R_c` and `T_c` formulas in the relative frame.
4. Show `T_c` is affine-conjugate to the 3D odometer
   `O_3(u,v,w) = (u + 1_{v=w=0}, v + 1_{w=0}, w + 1)`.

Failure criteria:
- No affine-pinned witness works on both `m=5` and `m=7`.
- The candidate requires nonlocal memory beyond low-layer coordinate tests.
- The rule cannot be expressed with vertexwise permutations / local priorities.

Artifacts to save:
  - code
  - raw logs
  - summary report
  - discovered examples / counterexamples
  - tables / plots / proof-supporting computations

Return format:
1. executive summary
2. exact symbolic rule
3. first-return formulas
4. cycle statistics on `m=5,7,9`
5. odometer conjugacy check
6. ruled-out subfamilies
7. hand-proof outline

Reproducibility requirements:
- fixed seeds
- exact solver version
- saved candidate tables in JSON/CSV
- deterministic validation scripts
- raw witness traces
