I think the right answer is:

> **The correct exact rule on the first exact object is a marked Moore chain, not yet a cyclic clock.**
>
> On that chain, the canonical state is the **short-corner index**.
> The intended local/admissible class, once it is exact deterministic for current `epsilon4`, is not seeing a smaller quotient: it is seeing the **whole marked chain**.
> The modulo-(m) clock appears only after promotion/periodization.

## 1. The right exact rule: a marked Moore chain

Take the first exact object to be the marked length-(m) chain
[
C_m=(x_0\to x_1\to \cdots \to x_{m-1}),
]
with current-event output
[
e_i:=\epsilon_4(x_i).
]

This should be treated as an **open Moore automaton**:
[
M_m:=\big({0,\dots,m-1},\ \sigma(i)=i+1\ (i<m-1),\ e_m(i)=e_i\big).
]

The phase-corner package says the active branch has one distinguished short corner, and that it is visible from the two-step event signature
[
(\epsilon_4(x),\epsilon_4(Tx))=(\mathrm{flat},\mathrm{other}*{0010}).
]
So, after taking one-step lookahead at the chain end if needed, there is a unique index (r_m) such that
[
(e*{r_m},e_{r_m+1})=(\mathrm{flat},\mathrm{other}_{0010}).
]
That (r_m) is the **short-corner mark**. This is exactly the structural gain emphasized in `070`: realization is now corner-time descent once one has the right exact deterministic `epsilon4` quotient on the marked chain.

So the first exact rule is:

[
\boxed{
\text{state }i\in{0,\dots,m-1},\quad
i\mapsto i+1,\quad
\text{output }e_m(i),\quad
\text{distinguished mark }r_m
}
]

This is the chain-first version of the later clock.

## 2. Why this is the correct chain-level state, not yet (\beta)

A full cyclic clock (\beta\in \mathbb Z/m\mathbb Z) needs return identification.
The handoffs now explicitly say that return/periodization is a later promotion step, not part of the first exact object. So at chain stage, the right canonical coordinate is simply **position relative to the short corner**.

A convenient normalization is
[
\gamma(x_i):=i-r_m \in {-r_m,\dots,m-1-r_m}.
]
Then
[
\gamma(Tx_i)=\gamma(x_i)+1 \qquad (i<m-1),
]
and the short corner is exactly
[
\gamma=0.
]

So the exact chain rule can be written as
[
\gamma'=\gamma+1,\qquad \epsilon_4=E_m(\gamma),
]
where (E_m) is the fixed event word on that marked chain.

Only after cycle promotion do you periodize (\gamma) to get the canonical clock (\beta).

## 3. The key rigidity theorem on the marked chain

Here is the main theorem I think you want.

### Theorem A

Let
[
q:C_m\to Q
]
be a deterministic quotient of the marked chain that is exact for current `epsilon4`, meaning:

* successor descends:
  [
  q(x_{i+1})=\widehat\sigma(q(x_i));
  ]
* current event factors through (q):
  [
  \epsilon_4(x_i)=H(q(x_i)).
  ]

Then (q) is injective.

### Proof

For each (i), form the suffix signature
[
S_i:=\big(e_i,e_{i+1},\dots,e_{m-1},\bot\big),
]
where (\bot) is an end marker for the open chain.

If (q(x_i)=q(x_j)), then determinism gives
[
q(x_{i+t})=q(x_{j+t})
]
for every common forward time (t), and exactness of current `epsilon4` gives
[
e_{i+t}=e_{j+t}.
]
So (S_i=S_j).

But the (S_i) are all distinct. The reason is that the short-corner detector
[
(\mathrm{flat},\mathrm{other}_{0010})
]
appears at a unique offset from each starting point before the corner, appears at no future offset once you start after the unique corner, and the end marker (\bot) occurs at different times for different starting indices. Hence (S_i\neq S_j) for (i\neq j).

Therefore (q(x_i)\neq q(x_j)) whenever (i\neq j). ∎

### Corollary A.1

The minimal exact deterministic current-event quotient of the marked chain is the marked chain itself.

So there is **no nontrivial exact deterministic `epsilon4` quotient** of the first exact object.

That is stronger than just “size at least (m)”: at chain stage, exactness already forces identity.

## 4. What quotient is the intended local/admissible class actually seeing?

Now let (\mathcal O(x_i)) be the current datum seen by the intended local/admissible class on the marked chain.

Define the induced quotient in the usual deterministic way:
[
x_i \sim_{\mathcal O} x_j
\iff
\big(\mathcal O(x_i),\mathcal O(x_{i+1}),\dots,\mathcal O(x_{m-1}),\bot\big)
============================================================================

\big(\mathcal O(x_j),\mathcal O(x_{j+1}),\dots,\mathcal O(x_{m-1}),\bot\big).
]

Call the quotient (Q_{\mathcal O}(C_m)).

Then:

* (Q_{\mathcal O}(C_m)) is the smallest deterministic quotient induced by the intended class on the chain;
* if (Q_{\mathcal O}(C_m)) is also exact for current `epsilon4`, then by Theorem A it must be injective;
* therefore, in that case,
  [
  |Q_{\mathcal O}(C_m)|=m
  ]
  and (Q_{\mathcal O}(C_m)\cong C_m).

So the intended class, **once exact for current `epsilon4`**, is not seeing a compressed quotient of the correct exact rule. It is seeing the full marked chain.

This matches the compute summary in `070`: on the checked frozen range, the existing admissible catalog already gives exact deterministic quotients of size exactly (m) on the marked length-(m) slice chains. 

## 5. The practical interpretation

This means the best candidate answer is:

### Correct exact rule on the marked chain

The correct chain-level rule is the **marked chain itself**:
[
i\mapsto i+1
]
with current-event output word (e_m(i)) and unique short-corner mark (r_m).

Equivalently, use the short-corner coordinate
[
\gamma=i-r_m.
]

### Quotient seen by the intended class

The intended local/admissible class is seeing the **identity quotient** of that rule, not a smaller one, provided its quotient is exact deterministic for current `epsilon4`.

So the right picture is:

[
\boxed{
\text{marked chain rule}
;\longrightarrow;
\text{intended quotient}
;\stackrel{\text{if exact for }\epsilon_4}{=};
\text{same marked chain}
}
]

## 6. How this fits corner-time and the later clock

Once the quotient is the full marked chain, the short corner is already visible in the quotient. Then the later realization step becomes easy:

* at chain stage, the quotient carries the exact short-corner index (\gamma);
* after periodization, (\gamma) becomes the cyclic corner-time / clock;
* that is the `070` corner-time descent picture. 

So the logical order is now very clean:

1. prove the first exact object is the marked chain;
2. prove the intended class induces a deterministic quotient on that chain;
3. prove that quotient is exact for current `epsilon4`;
4. conclude it is already the full marked chain;
5. only then promote to the cyclic clock.

## 7. My best current conclusion

I would state the candidate theorem package as:

**Marked-Chain Exact Rule Theorem.**
The first exact D5 object is the marked Moore chain (M_m) with unique short-corner mark.

**Marked-Chain Quotient Rigidity.**
Any deterministic quotient of (M_m) that is exact for current `epsilon4` is injective.

**Intended-Class Corollary.**
Hence the quotient induced by the intended local/admissible class on the marked chain, if exact for current `epsilon4`, is isomorphic to the full marked chain itself.

That is, I think, the right formal answer to “what is the correct exact rule?” and “what quotient is the intended class actually seeing?”

The remaining unclosed step is not the shape of the rule anymore. It is the D5-specific proof that the intended class’s induced quotient on the marked chain really is exact deterministic for current `epsilon4` in general odd (m). The `070` note says that on checked marked chains the existing admissible catalog already behaves exactly that way, which is strong evidence that this is the right rule and the right quotient. 
