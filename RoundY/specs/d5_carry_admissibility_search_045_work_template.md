Work Template:
    Task ID:
    D5-CARRY-ADMISSIBILITY-SEARCH-045

    Question:
    For the unresolved best-seed channel
        R1 -> H_L1
    in the seed pair
        left = [2,2,1], right = [1,4,4],
    can the carry-slice bit
        c = 1_{q = m-1}
    be realized by the smallest admissible lifted observable family,
    without reopening full raw-q exposure or realization of the residual sheet d?

    Purpose:
    The active branch now has an explicit checked normal form
        B <- B+c <- B+c+d
    with
        B = (s,u,v,layer,family),
        c = 1_{q = m-1},
        d = 1_{next carry u >= m-3}.
    The controller logic is already solved on raw coordinates, and the residual
    binary sheet d is now structurally understood. The live local/computational
    problem is therefore narrower:
        realize c admissibly.
    Proof writing can wait. This branch should focus on exact search,
    validation, collisions, minimality, and saved artifacts.

    Current target:
    Do not search for a new controller.
    Do not search for full raw q.
    Do not search for local realization of d.
    Search only for the smallest admissible observable/gadget that realizes
        c = 1_{q = m-1}
    on the checked active branch.

    Fixed scope / checked base:
    - primary seed pair:
      - left  = [2,2,1]
      - right = [1,4,4]
    - unresolved channel:
      - R1 -> H_L1
    - checked moduli:
      - m in {5,7,9,11}
    - active-branch normal form available from:
      - 037, 039, 040, 041, 042, 043, 044

    Known assumptions:
    - 033 reduces the best-seed obstruction to the unresolved R1 -> H_L1 corridor.
    - 037 shows the raw active corridor already carries a visible odometer on
      (q,w,layer).
    - 039 gives exact raw birth/entry formulas.
    - 040 shows the raw current-coordinate family already realizes the reduced
      control logic on the checked active union.
    - 041 proves the first 025-style grouped-state-descending families are too
      small: regular fire is not a function of current grouped state
          (s,u,v)
      even after conditioning on the family bit.
    - 042 shows:
      - exceptional fire descends to
          B = (s,u,v,layer,family),
      - regular fire descends to B+c,
      - c is not a function of B,
      - B+c is not dynamically closed,
      - the structural lift over B has fiber size <= 3.
    - 043 shows the deterministic cover over B+c is 2-sheet and that obvious
      short carry-window surrogates fail on larger checked moduli.
    - 044 gives the checked explicit normal form
          B <- B+c <- B+c+d
      with canonical binary anticipation sheet
          d = 1_{next carry u >= m-3}.
    - The local open branch after 044 is still only admissible realization of c.

    What this task is NOT:
    - not a proof-writing task
    - not a manuscript task
    - not a generic transducer search
    - not a search for realization of d
    - not a search for full raw q
    - not another search in families that still descend to current B

    Main computational objective:
    Find the smallest admissible lifted family F such that on the checked active
    branch,
        F(state) = c(state) = 1_{q = m-1}
    exactly.

    Secondary structural objective:
    If no such F exists in the first lifted admissible families, identify the
    exact next missing admissibility datum:
    - edge sheet,
    - 1-step grouped transition sheet,
    - 2-step grouped transition sheet,
    - anchored cocycle sheet,
    - or some other minimal lifted coordinate.

    Suggested search ordering:

    Pass 0. Freeze the exact carry-labeled dataset
    ----------------------------------------------
    Extract and save the exact active-union dataset for each checked modulus,
    with rows carrying at least:
    - modulus m
    - source class / family tag
    - current raw coordinates: q,w,u,layer
    - grouped state: s,u,v
    - derived base state B = (s,u,v,layer,family)
    - carry bit c = 1_{q=m-1}
    - residual bit d = 1_{next carry u >= m-3}
    - regular/exceptional fire flags
    - predecessor/successor identifiers if available

    Goal:
    Make one canonical frozen dataset that all later search passes read.

    Pass 1. Minimal admissible families that do NOT descend to current B
    --------------------------------------------------------------------
    Search only families whose value can distinguish states inside a fixed B-fiber.
    Natural first families to test:

    1A. Current-edge admissible families
        - observables tied to the current active edge / current directed step,
          not just the current grouped vertex state
        - any 025-compatible edge-tied point cocycle variants that are evaluated
          on the current active edge rather than forced to descend to B

    1B. 1-step grouped-transition families
        - observables depending on the ordered pair
            (B_t, B_{t+1})
          or equivalent admissible transition class
        - this includes coboundary-style differences of grouped-descending gauges
          if they no longer collapse to current B

    1C. 2-step grouped-transition families
        - observables depending on
            (B_t, B_{t+1}, B_{t+2})
          or the minimal equivalent transition signature
        - only if 1-step families fail

    1D. Anchored lifted cocycle families
        - omit-base anchored or edge-anchored cocycle residues allowed by the
          reduced 025 framework, provided they are not forced to descend to B
        - keep these binary or very low-cardinality whenever possible

    1E. Tiny binary gadgets motivated by carry detection
        - families designed specifically to test the carry slice rather than to
          recover general q
        - do not widen to general phase recovery unless a candidate survives

    Pass 2. Exactness tests for each candidate family
    -------------------------------------------------
    For each candidate family F, compute exactly on m = 5,7,9,11:
    - whether F is a function of the admissible object being tested
    - whether F equals c exactly on the entire checked active union
    - collision counts by B-fiber
    - collision counts by B+c-fiber
    - false positives / false negatives relative to c
    - whether F is only succeeding on a strict subset (e.g. regular only,
      or a single layer slice)
    - support profile by regular / exceptional / carry / noncarry regions

    Pass 3. Minimality / redundancy pruning
    ---------------------------------------
    Among exact candidates, identify:
    - smallest cardinality
    - smallest support description
    - smallest transition depth
    - whether the candidate is equivalent to another one under a trivial
      relabeling or complement
    - whether the candidate is effectively just a disguised raw-q test
      (reject if it is not admissible in the intended sense)

    Pass 4. Integration check with existing reduced controller
    ----------------------------------------------------------
    For any exact admissible carry candidate F, verify that
    - exceptional fire remains a function of B,
    - regular fire becomes exact from B+F,
    - the raw reduced controller off / active_reg / active_exc + F reproduces
      the correct trigger set on the checked active union,
    - no prehits appear on the checked active union,
    - no target misses appear on the checked active union.

    Pass 5. Optional robustness extension
    -------------------------------------
    Only if a positive candidate survives Passes 2--4, optionally test additional
    odd moduli beyond the base set, for example:
    - m in {13,15,17}
    or any other feasible extension.

    This extension is for code confidence only and must be clearly separated from
    the core checked scope.

    Explicit success criteria:
    1. Produce at least one admissible lifted family F that is exact for
           c = 1_{q=m-1}
       on the checked active branch for m = 5,7,9,11.
    2. Show that F is not merely another grouped-state-descending family.
    3. Show that B+F gives the already-known exact regular trigger logic.
    4. Save exact collision tables and support profiles.
    5. Identify the smallest surviving positive family up to obvious symmetry /
       complement / relabeling.

    Stronger success criteria:
    6. Show that the surviving positive family has a clean structural meaning,
       e.g. carry sheet, carry predictor, current-edge carry detector, or
       anchored cocycle carry class.
    7. Show that it plausibly generalizes beyond the checked moduli.

    Explicit failure criteria:
    - no candidate in Pass 1 is exact for c on m = 5,7,9,11, or
    - every exact candidate is inadmissible in the intended reduced sense, or
    - every exact candidate is just full raw-q recovery in disguise.

    If failure occurs, return the exact next missing admissibility datum:
    - current edge sheet,
    - 1-step transition sheet,
    - 2-step transition sheet,
    - anchored cocycle sheet,
    - or broader lifted gauge.

    Candidate lemmas / claims to support computationally:
    - [C] On the checked active union,
          w = s - u  (mod m).
    - [C] Exceptional fire is already a function of
          B = (s,u,v,layer,family).
    - [C] Regular fire is already a function of B+c.
    - [C] c is not a function of B.
    - [C] The active branch has checked normal form
          B <- B+c <- B+c+d
          with
          d = 1_{next carry u >= m-3}.
    - [H] The next concrete local/computational target is admissible realization
          of c, not realization of d.
    - [H] The first plausible positive family should be a lifted admissible
          carry detector rather than a full q-recovery observable.
    - [F] The next honest branch is realization of d first.
    - [O] Full D5 Hamilton decomposition remains open.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - frozen carry-labeled active datasets
    - candidate family catalog
    - exactness / collision tables
    - false-positive / false-negative tables
    - support-profile tables
    - minimal positive family summary (if positive)
    - exact obstruction summary (if negative)
    - reproducible scripts for every pass

    Recommended filenames:
    - analysis_summary.json
    - frozen_active_carry_dataset_045.json
    - candidate_family_catalog_045.json
    - carry_realization_search_summary_045.json
    - carry_exactness_tables_045.json
    - carry_collision_profiles_045.json
    - carry_support_profiles_045.json
    - minimal_positive_carry_family_045.json
    - admissibility_obstruction_045.json
    - representative_positive_candidates_045.json
    - representative_negative_candidates_045.json

    Return format:
    - exact statement of whether c was realized
    - smallest surviving admissible family (if positive)
    - exact collision/obstruction summary (if negative)
    - whether the positive family is current-edge, 1-step transition,
      2-step transition, anchored cocycle, or other
    - whether B+candidate is enough for regular trigger logic
    - explicit recommendation for the next branch:
      - proof from the positive candidate,
      - wider validation of the positive candidate,
      - or escalation to the next lifted admissibility class

    Reproducibility requirements:
    - fixed best seed pair [2,2,1] / [1,4,4]
    - fixed unresolved channel R1 -> H_L1
    - fixed checked moduli 5,7,9,11 for the core branch
    - deterministic extraction order
    - frozen base dataset used by all search passes
    - exact script path and invocation recorded
    - exact separation of:
      - prior checked facts from 041/042/043/044,
      - new 045 carry-realization search facts,
      - optional robustness tests beyond the core moduli

    Notes for execution priority:
    - prioritize exact extraction and exactness tests over broad search
    - prioritize smallest binary / low-cardinality families
    - do not spend time writing proofs in this branch
    - if a positive candidate appears, validate it hard before widening
    - if the first lifted class fails cleanly, stop and report the precise next
      admissibility datum rather than diffusing into generic search
