import Mathlib

namespace RoundComposite

variable (Solved : Nat -> Nat -> Prop)

def UniformSolved (d : Nat) : Prop :=
  ∀ {m : Nat}, 3 ≤ m -> Solved d m

def PointwiseCompositeExpansion : Prop :=
  ∀ {a b m : Nat}, 0 < a -> 0 < b -> 3 ≤ m ->
    Solved a m -> Solved b (m ^ a) -> Solved (a * b) m

theorem three_le_pow_of_three_le {m a : Nat} (hm : 3 ≤ m) (ha : 0 < a) :
    3 ≤ m ^ a := by
  exact le_trans hm (Nat.le_self_pow (Nat.ne_of_gt ha) m)

theorem uniform_mul_of_pointwise
    (hExp : PointwiseCompositeExpansion Solved)
    {a b : Nat} (ha : 0 < a) (hb : 0 < b)
    (hA : UniformSolved Solved a) (hB : UniformSolved Solved b) :
    UniformSolved Solved (a * b) := by
  intro m hm
  exact hExp ha hb hm (hA hm) (hB (three_le_pow_of_three_le hm ha))

def UniformMulClosed : Prop :=
  ∀ {a b : Nat}, 0 < a -> 0 < b ->
    UniformSolved Solved a -> UniformSolved Solved b ->
    UniformSolved Solved (a * b)

theorem uniform_mul_closed_of_pointwise
    (hExp : PointwiseCompositeExpansion Solved) :
    UniformMulClosed Solved := by
  intro a b ha hb hA hB
  exact uniform_mul_of_pointwise Solved hExp ha hb hA hB

def PrimeBaseSolved : Prop :=
  ∀ {p : Nat}, Nat.Prime p -> UniformSolved Solved p

theorem uniform_product_of_two_primes
    (hExp : PointwiseCompositeExpansion Solved)
    (hPrime : PrimeBaseSolved Solved)
    {p q : Nat} (hp : Nat.Prime p) (hq : Nat.Prime q) :
    UniformSolved Solved (p * q) := by
  exact uniform_mul_of_pointwise Solved hExp hp.pos hq.pos
    (hPrime hp) (hPrime hq)

end RoundComposite
