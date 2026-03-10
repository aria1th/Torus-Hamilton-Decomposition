Problem:
Construct a d=5 cyclic-equivariant permutation-valued local field
\[
\Pi_\theta\in S_5,
\qquad f_c(x)=x+e_{\Pi_{\theta(x)}(c)}
\]
whose induced five color maps are arc-disjoint Hamilton cycles.

Current target:
Extract the theorem-level form of the master-field branch after the Codex quotient run:
1. what is actually ruled out by D5-MASTER-FIELD-QUOTIENT-001,
2. what is *not* ruled out,
3. what the next finite quotient search should use as primary variables.

Known assumptions:
- There is a cyclic phase action \(\rho\) (simultaneous color/coordinate shift).
- We want cyclic equivariance
  \[
  \Pi_{\rho\theta}=\rho\Pi_\theta\rho^{-1}.
  \]
- In the previous quotient run, color-0 output was anchored at every phase by a preassigned map
  \[
  a(\theta):=\Pi_\theta(0).
  \]
  Those anchors came from one-color q-clock / clean-fiber candidates.

Attempt A:
  Idea:
  Interpret the quotient CP-SAT run as a genuine coupling search over permutation tables.

  What works:
  - It correctly certifies both anchored schemas as infeasible.

  Where it fails:
  - This interpretation is mathematically misleading.
  - Under cyclic equivariance, prescribing \(a(\theta)=\Pi_\theta(0)\) on every phase already determines the entire permutation field uniquely on each rotation orbit. So there is essentially no remaining coupling freedom.

Attempt B:
  Idea:
  Treat the master-field as an orbit-anchor problem.
  For a prescribed representative-color anchor \(a:\Theta\to\mathbb Z_5\), reconstruct the unique cyclic-equivariant field by
  \[
  \Pi_\theta(c)=a(\rho^{-c}\theta)+c \pmod 5.
  \]

  What works:
  - This gives a clean theorem-level reformulation.
  - Outgoing-Latin becomes an orbitwise condition on the five-term anchor word.
  - The Codex no-go becomes immediate and local: both searched anchors already fail outgoing-Latin on an explicit layer-2 phase.

  Where it fails:
  - It rules out only the *anchored extensions* of the Class A / Class B representative-color rules.
  - It does **not** rule out the underlying phase spaces themselves.
  - Therefore the next branch should not be “enlarge state space” by default; it should first free the anchor / permutation field from the one-color prescription.

Candidate lemmas:
- [P] Orbit-anchor reconstruction lemma.
  If \(\Pi\) is cyclic-equivariant and \(a(\theta)=\Pi_\theta(0)\), then for every phase \(\theta\),
  \[
  \Pi_\theta(c)=a(\rho^{-c}\theta)+c.
  \]
  Hence the anchor \(a\) determines \(\Pi\) uniquely.

- [P] Orbit-anchor outgoing criterion.
  A prescribed anchor \(a\) yields an outgoing-Latin field iff for every phase \(\theta\), the five residues
  \[
  a(\rho^{-c}\theta)+c \qquad (c=0,1,2,3,4)
  \]
  are pairwise distinct.

- [P] Predecessor-pattern incoming criterion.
  Once \(\Pi\) is fixed, incoming-Latin at a vertex \(x\) depends only on the predecessor phase pattern
  \[
  (\theta(x-e_0),\dots,\theta(x-e_4))
  \]
  and requires
  \[
  (\Pi_{\theta(x-e_0)}^{-1}(0),\dots,\Pi_{\theta(x-e_4)}^{-1}(4))
  \in S_5.
  \]

- [P] Explicit anchored no-go for schema A.
  In the `stable_anchor_two_atom` schema, the phase
  \[
  \theta_A=(2,(0,0,0,0,1))
  \]
  occurs for every \(m\ge 5\); for example at
  \[
  x=(m-1,0,0,0,3).
  \]
  Its anchor word is
  \[
  (2,2,2,2,4),
  \]
  so the induced permutation is
  \[
  \Pi_{\theta_A}=(2,0,4,0,1),
  \]
  not a permutation. Therefore schema A is impossible for all \(m\ge 5\).

- [P] Explicit anchored no-go for schema B.
  In the `unit_anchor_three_atom` schema, the phase
  \[
  \theta_B=(2,(0,0,0,0,1))
  \]
  occurs for every \(m\ge 5\); for example at
  \[
  x=(0,1,0,1,0).
  \]
  Its anchor word is also
  \[
  (2,2,2,2,4),
  \]
  giving the same non-permutation
  \[
  \Pi_{\theta_B}=(2,0,4,0,1).
  \]
  Therefore schema B is impossible for all \(m\ge 5\).

Needed computations/search:
- Search over master-field anchors \(a\) or directly over \(\Pi_\theta\), not over extensions of pre-fixed one-color anchors.
- Keep cyclic equivariance and predecessor-pattern incoming constraints hard.
- Encode q-clock / clean-fiber / clean-frame as derived structural constraints on the induced color-0 first return, rather than as a pre-fixed direction table.
- First test on the current phase spaces (same \(\Theta\)) before enlarging the state space.

Next branching options:
1. [Preferred] Free-anchor master-field search on the current quotient state space.
   Variables: one permutation \(\Pi_\theta\in S_5\) per phase orbit (or equivalently one anchor word satisfying the outgoing criterion).
   Hard constraints: cyclic equivariance, incoming-Latin, layer-0 / high-layer defaults.
   Soft / derived targets: representative-color clean frame, single-cycle section return, unit monodromy.

2. Add one extra phase bit only if the free-anchor search on the current quotient fails for structural reasons.

3. As a reduced subbranch, search shift-type fields
   \[
   \Pi_\theta(c)=c+\alpha(\theta)
   \]
   as the smallest nontrivial coupled family; if even this already shows useful no-go structure, promote it to a theorem.

Claim status labels:
  [P] Orbit-anchor reconstruction and outgoing criterion are rigorous.
  [P] Schema A and schema B anchored no-go are rigorous and hold for all \(m\ge 5\).
  [C] The previous Codex CP-SAT infeasibility is now explained by these local anchored collisions.
  [H] The next successful branch should treat \(\Pi_\theta\) or the anchor \(a\) as primary, not as an extension of a one-color witness.
  [O] Existence of a free-anchor quotient master field is still open.
