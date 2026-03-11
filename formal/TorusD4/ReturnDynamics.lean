import TorusD4.ReturnMaps
import Mathlib.Logic.Function.Iterate

namespace TorusD4

def qCoord (x : P0Coord m) : ZMod m :=
  x.2.2

def abCoord (x : P0Coord m) : QCoord m :=
  (x.1, x.2.1)

def sliceQ (u : QCoord m) : P0Coord m :=
  (u.1, u.2, (-1 : ZMod m))

def RMap : Color → P0Coord m → P0Coord m
  | 0 => R0
  | 1 => R1
  | 2 => R2
  | 3 => R3

def TMap : Color → QCoord m → QCoord m
  | 0 => T0
  | 1 => T1
  | 2 => T2
  | 3 => T3

def qSign : Color → ZMod m
  | 0 => -1
  | 1 => 1
  | 2 => -1
  | 3 => 1

@[simp] theorem qCoord_mk (a b q0 : ZMod m) : qCoord (a, b, q0) = q0 := rfl

@[simp] theorem abCoord_mk (a b q0 : ZMod m) : abCoord (a, b, q0) = (a, b) := rfl

@[simp] theorem qCoord_sliceQ (u : QCoord m) : qCoord (sliceQ u) = (-1 : ZMod m) := by
  rcases u with ⟨a, b⟩
  rfl

@[simp] theorem abCoord_sliceQ (u : QCoord m) : abCoord (sliceQ u) = u := by
  rcases u with ⟨a, b⟩
  rfl

@[simp] theorem qCoord_R0 (x : P0Coord m) : qCoord (R0 (m := m) x) = qCoord x - 1 := by
  rcases x with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · simp [R0, qCoord, hq0]
  · by_cases hbranch : q0 = (-1 : ZMod m) ∧ b = (1 : ZMod m)
    · have h1 : (1 : ZMod m) ≠ 0 := by
        intro h10
        have hneg1 : (-1 : ZMod m) = 0 := by simpa using h10
        exact hq0 (hbranch.1.trans hneg1)
      simp [R0, qCoord, hbranch, h1]
    · simp [R0, qCoord, hq0, hbranch]

@[simp] theorem qCoord_R1 (x : P0Coord m) : qCoord (R1 (m := m) x) = qCoord x + 1 := by
  rcases x with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · simp [R1, qCoord, hq0]
  · by_cases hbranch : q0 = (-1 : ZMod m) ∧ a = (-1 : ZMod m)
    · have h1 : (1 : ZMod m) ≠ 0 := by
        intro h10
        have hneg1 : (-1 : ZMod m) = 0 := by simpa using h10
        exact hq0 (hbranch.1.trans hneg1)
      simp [R1, qCoord, hbranch, h1]
    · simp [R1, qCoord, hq0, hbranch]

@[simp] theorem qCoord_R2 (x : P0Coord m) : qCoord (R2 (m := m) x) = qCoord x - 1 := by
  rcases x with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · simp [R2, qCoord, hq0]
  · by_cases hbranch : q0 = (-1 : ZMod m) ∧ b = (2 : ZMod m)
    · have h1 : (1 : ZMod m) ≠ 0 := by
        intro h10
        have hneg1 : (-1 : ZMod m) = 0 := by simpa using h10
        exact hq0 (hbranch.1.trans hneg1)
      simp [R2, qCoord, hbranch, h1]
    · simp [R2, qCoord, hq0, hbranch]

@[simp] theorem qCoord_R3 (x : P0Coord m) : qCoord (R3 (m := m) x) = qCoord x + 1 := by
  rcases x with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · simp [R3, qCoord, hq0]
  · by_cases hbranch : q0 = (-1 : ZMod m) ∧ a = (0 : ZMod m)
    · have h1 : (1 : ZMod m) ≠ 0 := by
        intro h10
        have hneg1 : (-1 : ZMod m) = 0 := by simpa using h10
        exact hq0 (hbranch.1.trans hneg1)
      simp [R3, qCoord, hbranch, h1]
    · simp [R3, qCoord, hq0, hbranch]

theorem qCoord_RMap (c : Color) (x : P0Coord m) :
    qCoord (RMap (m := m) c x) = qCoord x + qSign (m := m) c := by
  fin_cases c <;> simp [RMap, qSign, sub_eq_add_neg]

theorem R_q_update (c : Color) (x : P0Coord m) :
    qCoord (RMap (m := m) c x) = qCoord x + qSign (m := m) c :=
  qCoord_RMap (m := m) c x

theorem qCoord_iterate_RMap (c : Color) (x : P0Coord m) (n : ℕ) :
    qCoord (((RMap (m := m) c)^[n]) x) = qCoord x + (n : ZMod m) * qSign (m := m) c := by
  induction n with
  | zero =>
      simp [qCoord]
  | succ n ih =>
      rw [Function.iterate_succ_apply', qCoord_RMap, ih, Nat.cast_add]
      ring

theorem R_iterate_q (c : Color) (x : P0Coord m) (n : ℕ) :
    qCoord (((RMap (m := m) c)^[n]) x) = qCoord x + (n : ZMod m) * qSign (m := m) c :=
  qCoord_iterate_RMap (m := m) c x n

@[simp] theorem qCoord_iterate_RMap_sliceQ (c : Color) (u : QCoord m) (n : ℕ) :
    qCoord (((RMap (m := m) c)^[n]) (sliceQ (m := m) u)) =
      (-1 : ZMod m) + (n : ZMod m) * qSign (m := m) c := by
  simpa using qCoord_iterate_RMap (m := m) c (sliceQ (m := m) u) n

@[simp] theorem qCoord_iterate_RMap_sliceQ_m (c : Color) (u : QCoord m) :
    qCoord (((RMap (m := m) c)^[m]) (sliceQ (m := m) u)) = (-1 : ZMod m) := by
  rw [qCoord_iterate_RMap_sliceQ]
  simp

def secondReturnOfRMap (c : Color) (u : QCoord m) : QCoord m :=
  abCoord (((RMap (m := m) c)^[m]) (sliceQ (m := m) u))

theorem iterate_m_sliceQ_eq_sliceQ_secondReturn (c : Color) (u : QCoord m) :
    ((RMap (m := m) c)^[m]) (sliceQ (m := m) u) =
      sliceQ (m := m) (secondReturnOfRMap (m := m) c u) := by
  rcases h :
      (((RMap (m := m) c)^[m]) (sliceQ (m := m) u)) with ⟨a, b, q0⟩
  have hq : q0 = (-1 : ZMod m) := by
    have hq' := qCoord_iterate_RMap_sliceQ_m (m := m) c u
    rw [h] at hq'
    simpa [qCoord] using hq'
  have hab : secondReturnOfRMap (m := m) c u = (a, b) := by
    simp [secondReturnOfRMap, abCoord, h]
  rw [hab, sliceQ, hq]

end TorusD4
