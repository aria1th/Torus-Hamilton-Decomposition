import TorusD5.Common.M15r9.TheoremFloor
import Mathlib.Data.Int.ModEq

namespace TorusD5.Common.M15r9

abbrev SourceIndex := ℤ

def time0 (m : ℕ) : ℕ := (m + 1) / 5
def time1 (m : ℕ) : ℕ := (m - 4) / 5
def time2 (m : ℕ) : ℕ := (2 * m - 3) / 5
def time3 (m : ℕ) : ℕ := (3 * m - 2) / 5
def time4 (m : ℕ) : ℕ := (8 * m - 2) / 5
def time5 (m : ℕ) : ℕ := (9 * m - 1) / 5
def time6 (m : ℕ) : ℕ := (11 * m + 1) / 5

theorem time0_common (r : ℕ) : time0 (15 * r + 9) = 3 * r + 2 := by
  unfold time0
  omega

theorem time1_common (r : ℕ) : time1 (15 * r + 9) = 3 * r + 1 := by
  unfold time1
  omega

theorem time2_common (r : ℕ) : time2 (15 * r + 9) = 6 * r + 3 := by
  unfold time2
  omega

theorem time3_common (r : ℕ) : time3 (15 * r + 9) = 9 * r + 5 := by
  unfold time3
  omega

theorem time4_common (r : ℕ) : time4 (15 * r + 9) = 24 * r + 14 := by
  unfold time4
  omega

theorem time5_common (r : ℕ) : time5 (15 * r + 9) = 27 * r + 16 := by
  unfold time5
  omega

theorem time6_common (r : ℕ) : time6 (15 * r + 9) = 33 * r + 20 := by
  unfold time6
  omega

def IsZeroLeaf (x : SourceIndex) : Prop := x = 7 ∨ x = 11
def IsExc2Leaf (x : SourceIndex) : Prop := x = 12
def IsExc3Leaf (x : SourceIndex) : Prop := x = 15

def IsTypeA1 (x : SourceIndex) : Prop := x ≡ 4 [ZMOD 5]
def IsTypeA2 (x : SourceIndex) : Prop :=
  (x ≡ 0 [ZMOD 5] ∧ x ≠ 15) ∨ x = 1 ∨ x = 6 ∨ x = 16
def IsTypeA3 (x : SourceIndex) : Prop :=
  x ≡ 3 [ZMOD 5] ∧ x ≠ 3 ∧ x ≠ 8 ∧ x ≠ 13
def IsTypeA4 (x : SourceIndex) : Prop :=
  (x ≡ 1 [ZMOD 5] ∧ x ≠ 1 ∧ x ≠ 6 ∧ x ≠ 11 ∧ x ≠ 16) ∨ x = 8
def IsTypeA5 (x : SourceIndex) : Prop := x = 2
def IsTypeA6 (x : SourceIndex) : Prop :=
  (x ≡ 2 [ZMOD 5] ∧ x ≠ 2 ∧ x ≠ 7 ∧ x ≠ 12) ∨ x = 3 ∨ x = 13

def IsTypeB1 (x : SourceIndex) : Prop := x ≡ 4 [ZMOD 5]
def IsTypeB2 (x : SourceIndex) : Prop :=
  (x ≡ 0 [ZMOD 5] ∧ x ≠ 15) ∨ x = 6 ∨ x = 16
def IsTypeB3 (x : SourceIndex) : Prop :=
  x ≡ 3 [ZMOD 5] ∧ x ≠ 3 ∧ x ≠ 8 ∧ x ≠ 13
def IsTypeB4 (x : SourceIndex) : Prop :=
  (x ≡ 1 [ZMOD 5] ∧ x ≠ 6 ∧ x ≠ 11 ∧ x ≠ 16) ∨ x = 8
def IsTypeB5 (x : SourceIndex) : Prop := x = 2
def IsTypeB6 (x : SourceIndex) : Prop :=
  (x ≡ 2 [ZMOD 5] ∧ x ≠ 2 ∧ x ≠ 7 ∧ x ≠ 12) ∨ x = 3 ∨ x = 13

@[simp] theorem typeA1_eq_typeB1 (x : SourceIndex) : IsTypeA1 x ↔ IsTypeB1 x := Iff.rfl
@[simp] theorem typeA3_eq_typeB3 (x : SourceIndex) : IsTypeA3 x ↔ IsTypeB3 x := Iff.rfl
@[simp] theorem typeA5_eq_typeB5 (x : SourceIndex) : IsTypeA5 x ↔ IsTypeB5 x := Iff.rfl
@[simp] theorem typeA6_eq_typeB6 (x : SourceIndex) : IsTypeA6 x ↔ IsTypeB6 x := Iff.rfl

theorem typeA2_iff_typeB2_or_one (x : SourceIndex) :
    IsTypeA2 x ↔ IsTypeB2 x ∨ x = 1 := by
  unfold IsTypeA2 IsTypeB2
  constructor
  · intro hx
    rcases hx with h0 | h1 | h6 | h16
    · exact Or.inl (Or.inl h0)
    · exact Or.inr h1
    · exact Or.inl (Or.inr (Or.inl h6))
    · exact Or.inl (Or.inr (Or.inr h16))
  · intro hx
    rcases hx with hB | h1
    · rcases hB with h0 | h6 | h16
      · exact Or.inl h0
      · exact Or.inr (Or.inr (Or.inl h6))
      · exact Or.inr (Or.inr (Or.inr h16))
    · exact Or.inr (Or.inl h1)

theorem typeB4_iff_typeA4_or_one (x : SourceIndex) :
    IsTypeB4 x ↔ IsTypeA4 x ∨ x = 1 := by
  unfold IsTypeA4 IsTypeB4
  constructor
  · intro hx
    rcases hx with h | h8
    · by_cases h1 : x = 1
      · exact Or.inr h1
      · exact Or.inl (Or.inl ⟨h.1, h1, h.2.1, h.2.2.1, h.2.2.2⟩)
    · exact Or.inl (Or.inr h8)
  · intro hx
    rcases hx with hA | h1
    · rcases hA with h | h8
      · exact Or.inl ⟨h.1, h.2.2.1, h.2.2.2.1, h.2.2.2.2⟩
      · exact Or.inr h8
    · subst x
      exact Or.inl ⟨Int.ModEq.refl 1, by norm_num, by norm_num, by norm_num⟩

theorem typeA2_agrees_away_from_one {x : SourceIndex} (hx : x ≠ 1) :
    IsTypeA2 x ↔ IsTypeB2 x := by
  rw [typeA2_iff_typeB2_or_one]
  constructor
  · intro h
    rcases h with h | h1
    · exact h
    · exact False.elim (hx h1)
  · intro h
    exact Or.inl h

theorem typeA4_agrees_away_from_one {x : SourceIndex} (hx : x ≠ 1) :
    IsTypeA4 x ↔ IsTypeB4 x := by
  rw [typeB4_iff_typeA4_or_one]
  constructor
  · intro h
    exact Or.inl h
  · intro h
    rcases h with h | h1
    · exact h
    · exact False.elim (hx h1)

theorem stableGeometry_typeA_iff (family : TorusD5.CommonResidueFamily) :
    TorusD5.stablePacketGeometryOfFamily family = .typeA ↔
      family = .r8s ∨ family = .r8sPlus4 := by
  cases family <;> simp [TorusD5.stablePacketGeometryOfFamily]

theorem stableGeometry_typeB_iff (family : TorusD5.CommonResidueFamily) :
    TorusD5.stablePacketGeometryOfFamily family = .typeB ↔
      family = .r16uPlus2 ∨ family = .r16uPlus6 ∨
      family = .r16uPlus10 ∨ family = .r16uPlus14 := by
  cases family <;> simp [TorusD5.stablePacketGeometryOfFamily]

end TorusD5.Common.M15r9
