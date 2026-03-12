import TorusD5.Cocycle

namespace TorusD5

abbrev SectionMap (m : ℕ) := SectionCoord m → SectionCoord m
abbrev GroupedMap (m : ℕ) := GroupedCoord m → GroupedCoord m
abbrev SkewMap (m : ℕ) := SkewCoord m → SkewCoord m

/-- Componentwise formulation of the extracted first-return carry law. -/
structure HasCarryFirstReturn (R : SectionMap m) : Prop where
  q_eq : ∀ x, qCoord (m := m) (R x) = qCoord (m := m) x + 1
  w_eq : ∀ x,
    wCoord (m := m) (R x) =
      wCoord (m := m) x + topCarry (m := m) (qCoord (m := m) x)
  u_eq : ∀ x, uCoord (m := m) (R x) = uCoord (m := m) x + 1

/-- Componentwise formulation of the extracted grouped-return base law. -/
structure HasGroupedReturnBase (U : GroupedMap m) : Prop where
  w_eq : ∀ x, groupedW (m := m) (U x) = groupedW (m := m) x + 1
  u_eq : ∀ x, groupedU (m := m) (U x) = groupedU (m := m) x

/-- A skew map projects to the affine grouped-return base and carries a cocycle
on the twist coordinate. -/
structure ProjectsToGroupedSkew (F : SkewMap m) (phi : GroupedCoord m → ZMod m) : Prop where
  base_eq : ∀ x,
    skewBase (m := m) (F x) = groupedReturnBase (m := m) (skewBase (m := m) x)
  twist_eq : ∀ x,
    skewTwist (m := m) (F x) = skewTwist (m := m) x + phi (skewBase (m := m) x)

theorem hasCarryFirstReturn_firstReturnBase :
    HasCarryFirstReturn (m := m) (firstReturnBase (m := m)) where
  q_eq := firstReturnBase_q (m := m)
  w_eq := firstReturnBase_w (m := m)
  u_eq := firstReturnBase_u (m := m)

theorem hasGroupedReturnBase_groupedReturnBase :
    HasGroupedReturnBase (m := m) (groupedReturnBase (m := m)) where
  w_eq := groupedReturnBase_w (m := m)
  u_eq := groupedReturnBase_u (m := m)

theorem projectsToGroupedSkew_groupedSkew (phi : GroupedCoord m → ZMod m) :
    ProjectsToGroupedSkew (m := m) (groupedSkew (m := m) phi) phi where
  base_eq := groupedSkew_base (m := m) phi
  twist_eq := groupedSkew_twist (m := m) phi

theorem eq_firstReturnBase_of_hasCarryFirstReturn {R : SectionMap m}
    (hR : HasCarryFirstReturn (m := m) R) :
    R = firstReturnBase (m := m) := by
  funext x
  rcases x with ⟨q, w, u⟩
  apply Prod.ext
  · simpa using hR.q_eq (q, w, u)
  · apply Prod.ext
    · simpa using hR.w_eq (q, w, u)
    · simpa using hR.u_eq (q, w, u)

theorem eq_groupedReturnBase_of_hasGroupedReturnBase {U : GroupedMap m}
    (hU : HasGroupedReturnBase (m := m) U) :
    U = groupedReturnBase (m := m) := by
  funext x
  rcases x with ⟨w, u⟩
  apply Prod.ext
  · simpa using hU.w_eq (w, u)
  · simpa using hU.u_eq (w, u)

theorem eq_groupedSkew_of_projectsToGroupedSkew {F : SkewMap m} {phi : GroupedCoord m → ZMod m}
    (hF : ProjectsToGroupedSkew (m := m) F phi) :
    F = groupedSkew (m := m) phi := by
  funext x
  rcases x with ⟨w, u, t⟩
  have hbase := hF.base_eq (w, u, t)
  have htwist := hF.twist_eq (w, u, t)
  have hw : (F (w, u, t)).1 = w + 1 := by
    simpa [groupedReturnBase] using congrArg Prod.fst hbase
  have hu : (F (w, u, t)).2.1 = u := by
    simpa [groupedReturnBase] using congrArg Prod.snd hbase
  apply Prod.ext
  · simpa [groupedSkew] using hw
  · apply Prod.ext
    · simpa [groupedSkew] using hu
    · simpa [groupedSkew] using htwist

end TorusD5
