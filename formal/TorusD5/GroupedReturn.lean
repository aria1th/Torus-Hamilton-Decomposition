import TorusD5.FirstReturn

namespace TorusD5

theorem natCast_ne_zero_of_pos_lt [Fact (1 < m)] {n : ℕ} (hn0 : 0 < n) (hnm : n < m) :
    ((n : ℕ) : ZMod m) ≠ 0 := by
  intro h
  exact Nat.not_dvd_of_pos_of_lt hn0 hnm ((ZMod.natCast_eq_zero_iff n m).1 h)

theorem iterate_groupedReturnBase (n : ℕ) (w u : ZMod m) :
    ((groupedReturnBase (m := m)^[n]) (w, u)) = (w + n, u) := by
  induction n generalizing w u with
  | zero =>
      simp
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [groupedReturnBase, Nat.cast_add, add_assoc]

@[simp] theorem iterate_groupedReturnBase_w (n : ℕ) (x : GroupedCoord m) :
    groupedW (m := m) ((groupedReturnBase (m := m)^[n]) x) = groupedW (m := m) x + n := by
  rcases x with ⟨w, u⟩
  simp [iterate_groupedReturnBase]

@[simp] theorem iterate_groupedReturnBase_u (n : ℕ) (x : GroupedCoord m) :
    groupedU (m := m) ((groupedReturnBase (m := m)^[n]) x) = groupedU (m := m) x := by
  rcases x with ⟨w, u⟩
  simp [iterate_groupedReturnBase]

/-- The grouped-return base completes one period in exactly `m` steps. -/
theorem iterate_groupedReturnBase_period (x : GroupedCoord m) :
    ((groupedReturnBase (m := m)^[m]) x) = x := by
  rcases x with ⟨w, u⟩
  rw [iterate_groupedReturnBase]
  ext <;> simp

/-- On each fixed-`u` fiber, no smaller positive iterate can be the identity. -/
theorem iterate_groupedReturnBase_ne_self_of_pos_lt [Fact (1 < m)]
    (x : GroupedCoord m) {n : ℕ} (hn0 : 0 < n) (hnm : n < m) :
    ((groupedReturnBase (m := m)^[n]) x) ≠ x := by
  rcases x with ⟨w, u⟩
  intro h
  rw [iterate_groupedReturnBase] at h
  have hw : w + n = w := by
    simpa using congrArg Prod.fst h
  have hzero : ((n : ℕ) : ZMod m) = 0 := by
    have := congrArg (fun z : ZMod m => z - w) hw
    simpa [sub_eq_add_neg, add_assoc, add_left_comm, add_comm] using this
  exact natCast_ne_zero_of_pos_lt (m := m) hn0 hnm hzero

/-- The grouped-return base acts as a single `m`-cycle on each `u` fiber. -/
theorem iterate_groupedReturnBase_eq_self_iff [Fact (1 < m)]
    (x : GroupedCoord m) {n : ℕ} (hnm : n < m) :
    ((groupedReturnBase (m := m)^[n]) x) = x ↔ n = 0 := by
  constructor
  · intro h
    by_cases hn0 : n = 0
    · exact hn0
    · exfalso
      exact iterate_groupedReturnBase_ne_self_of_pos_lt (m := m) x (Nat.pos_of_ne_zero hn0) hnm h
  · intro hn
    subst hn
    simp

/-- The abstract skew product projects to the grouped-return base under the
base-coordinate projection. -/
theorem iterate_groupedSkew_base (phi : GroupedCoord m → ZMod m) (n : ℕ) (x : SkewCoord m) :
    skewBase (m := m) (((groupedSkew (m := m) phi)^[n]) x) =
      ((groupedReturnBase (m := m)^[n]) (skewBase (m := m) x)) := by
  induction n generalizing x with
  | zero =>
      simp
  | succ n ih =>
      calc
        skewBase (m := m) (((groupedSkew (m := m) phi)^[n + 1]) x)
            = groupedReturnBase (m := m)
                (skewBase (m := m) (((groupedSkew (m := m) phi)^[n]) x)) := by
                  rw [Function.iterate_succ_apply']
                  simp
        _ = groupedReturnBase (m := m)
              (((groupedReturnBase (m := m)^[n]) (skewBase (m := m) x))) := by
                rw [ih]
        _ = ((groupedReturnBase (m := m)^[n + 1]) (skewBase (m := m) x)) := by
              rw [Function.iterate_succ_apply']

end TorusD5
