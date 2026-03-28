import TorusD5.Basic

namespace TorusD5

section ExactQuotient

variable {X Q A C : Type*}

/-- The full future event word emitted from `x` under successor `F` and event
map `E`. -/
def futureWord (F : X → X) (E : X → A) (x : X) : ℕ → A :=
  fun n => E ((F^[n]) x)

/-- Future words separate states if the full future event word determines the
starting state. -/
def FutureWordsSeparateStates (F : X → X) (E : X → A) : Prop :=
  Function.Injective (futureWord F E)

/-- A quotient map is exact/deterministic for an event map if both successor and
current event factor through it. -/
structure IsExactDeterministicQuotient (F : X → X) (E : X → A) (p : X → Q) where
  succ : Q → Q
  event : Q → A
  succ_comm : ∀ x, p (F x) = succ (p x)
  event_comm : ∀ x, E x = event (p x)

/-- A coordinate is retained by a quotient if it factors through the quotient
state. -/
structure RetainsCoordinate (p : X → Q) (c : X → C) where
  readout : Q → C
  exact_eq : ∀ x, c x = readout (p x)

@[simp] theorem retainsCoordinate_apply {p : X → Q} {c : X → C}
    (h : RetainsCoordinate p c) (x : X) :
    h.readout (p x) = c x := by
  symm
  exact h.exact_eq x

/-- The quotient carries the full future word on its own state space. -/
def quotientFutureWord {F : X → X} {E : X → A} {p : X → Q}
    (hQ : IsExactDeterministicQuotient F E p) (q : Q) : ℕ → A :=
  futureWord hQ.succ hQ.event q

theorem iterate_proj_eq_iterate_succ {F : X → X} {E : X → A} {p : X → Q}
    (hQ : IsExactDeterministicQuotient F E p) (n : ℕ) (x : X) :
    p ((F^[n]) x) = ((hQ.succ^[n]) (p x)) := by
  induction n generalizing x with
  | zero =>
      rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
      rw [hQ.succ_comm, ih]

theorem futureWord_eq_quotientFutureWord {F : X → X} {E : X → A} {p : X → Q}
    (hQ : IsExactDeterministicQuotient F E p) (x : X) :
    futureWord F E x = quotientFutureWord hQ (p x) := by
  funext n
  unfold futureWord quotientFutureWord
  rw [hQ.event_comm]
  simpa using congrArg hQ.event (iterate_proj_eq_iterate_succ (hQ := hQ) n x)

theorem futureWord_eq_of_proj_eq {F : X → X} {E : X → A} {p : X → Q}
    (hQ : IsExactDeterministicQuotient F E p) {x y : X} (hxy : p x = p y) :
    futureWord F E x = futureWord F E y := by
  rw [futureWord_eq_quotientFutureWord hQ x, futureWord_eq_quotientFutureWord hQ y, hxy]

/-- The standard rigidity transport step: if future words already separate
states, then any exact deterministic quotient must be injective. -/
theorem injective_of_futureWordsSeparateStates {F : X → X} {E : X → A} {p : X → Q}
    (hSep : FutureWordsSeparateStates F E)
    (hQ : IsExactDeterministicQuotient F E p) :
    Function.Injective p := by
  intro x y hxy
  apply hSep
  exact futureWord_eq_of_proj_eq hQ hxy

/-- Any coordinate descends uniquely to the quotient image once the quotient map
is injective. -/
noncomputable def descendToRange (p : X → Q) (_hp : Function.Injective p) (c : X → C) :
    Set.range p → C :=
  fun q => c (Classical.choose q.2)

@[simp] theorem descendToRange_apply (p : X → Q) (hp : Function.Injective p) (c : X → C) (x : X) :
    descendToRange p hp c ⟨p x, ⟨x, rfl⟩⟩ = c x := by
  unfold descendToRange
  let hq : ∃ y, p y = p x := ⟨x, rfl⟩
  change c (Classical.choose hq) = c x
  have hchoose : p (Classical.choose hq) = p x := Classical.choose_spec hq
  have hx : Classical.choose hq = x := hp hchoose
  simp [hx]

theorem existsUnique_descendToRange (p : X → Q) (hp : Function.Injective p) (c : X → C) :
    ∃! cbar : Set.range p → C, ∀ x, cbar ⟨p x, ⟨x, rfl⟩⟩ = c x := by
  refine ⟨descendToRange p hp c, ?_, ?_⟩
  · intro x
    exact descendToRange_apply p hp c x
  · intro cbar hc
    funext q
    rcases q with ⟨q, hq⟩
    rcases hq with ⟨x, rfl⟩
    simpa using hc x

theorem existsUnique_descendToRange_of_exactQuotient
    {F : X → X} {E : X → A} {p : X → Q}
    (hSep : FutureWordsSeparateStates F E)
    (hQ : IsExactDeterministicQuotient F E p)
    (c : X → C) :
    ∃! cbar : Set.range p → C, ∀ x, cbar ⟨p x, ⟨x, rfl⟩⟩ = c x := by
  exact existsUnique_descendToRange p (injective_of_futureWordsSeparateStates hSep hQ) c

end ExactQuotient

end TorusD5
