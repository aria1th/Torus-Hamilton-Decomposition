import TorusD5.GroupedReturn

namespace TorusD5

/-- Accumulated cocycle along the grouped base orbit for `n` steps. -/
def cocycleSum (phi : GroupedCoord m → ZMod m) : ℕ → GroupedCoord m → ZMod m
  | 0, _ => 0
  | n + 1, (w, u) => cocycleSum phi n (w, u) + phi (w + n, u)

@[simp] theorem cocycleSum_zero (phi : GroupedCoord m → ZMod m) (x : GroupedCoord m) :
    cocycleSum (m := m) phi 0 x = 0 := rfl

@[simp] theorem cocycleSum_succ (phi : GroupedCoord m → ZMod m) (n : ℕ) (w u : ZMod m) :
    cocycleSum (m := m) phi (n + 1) (w, u) =
      cocycleSum (m := m) phi n (w, u) + phi (w + n, u) := rfl

/-- Exact iterate formula for the abstract grouped skew-product over the affine
base `(w,u) ↦ (w+1,u)`. -/
theorem iterate_groupedSkew (phi : GroupedCoord m → ZMod m) (n : ℕ) (w u t : ZMod m) :
    (((groupedSkew (m := m) phi)^[n]) (w, u, t)) =
      (w + n, u, t + cocycleSum (m := m) phi n (w, u)) := by
  induction n generalizing w u t with
  | zero =>
      simp [cocycleSum]
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [groupedSkew, cocycleSum, Nat.cast_add, add_assoc, add_left_comm, add_comm]

@[simp] theorem iterate_groupedSkew_base_apply
    (phi : GroupedCoord m → ZMod m) (n : ℕ) (w u t : ZMod m) :
    skewBase (m := m) (((groupedSkew (m := m) phi)^[n]) (w, u, t)) =
      (w + n, u) := by
  simp [iterate_groupedSkew]

@[simp] theorem iterate_groupedSkew_twist_apply
    (phi : GroupedCoord m → ZMod m) (n : ℕ) (w u t : ZMod m) :
    skewTwist (m := m) (((groupedSkew (m := m) phi)^[n]) (w, u, t)) =
      t + cocycleSum (m := m) phi n (w, u) := by
  simp [iterate_groupedSkew]

/-- After one full grouped-base period, the base returns to `(w,u)` and the
twist changes by the orbit cocycle sum. -/
theorem iterate_groupedSkew_period (phi : GroupedCoord m → ZMod m) (w u t : ZMod m) :
    (((groupedSkew (m := m) phi)^[m]) (w, u, t)) =
      (w, u, t + cocycleSum (m := m) phi m (w, u)) := by
  rw [iterate_groupedSkew]
  ext <;> simp

end TorusD5
