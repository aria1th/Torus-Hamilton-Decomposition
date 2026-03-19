# D5 131: compute request for the remaining 032 shape theorem

## Target

Close the remaining first-principles content behind front-end seed isolation `032`.
The normal-form part is already settled: once the live endpoint seed class is known to be an oriented bridge-type class, the normalized representative is forced to be

- left `[2,2,1]`
- right `[1,4,4]`.

So the missing input is only the endpoint-word shape theorem.

## Requested computation / certification

For the odd-`m`, `d=5` endpoint-local front end after the earlier tiny static repair branches are pruned:

1. enumerate the surviving endpoint seed classes up to the accepted front-end symmetries;
2. identify, for each surviving class,
   - whether it has a shared bridge symbol,
   - whether the left word has one repeated oriented neighbor,
   - whether the right word has one repeated oriented neighbor;
3. certify whether there is exactly one surviving oriented bridge-type class;
4. give the explicit symmetry map sending that class to the normalized seed
   `[2,2,1] / [1,4,4]`;
5. for every other seed class, record whether it is
   - symmetry-equivalent to the same class,
   - already closed by an earlier tiny static repair branch, or
   - eliminated because it fails the local endpoint feasibility test.

## Acceptance criteria

The request is successful only if it returns all of the following.

- A complete symmetry-reduced list of surviving seed classes.
- A proof certificate, table, or exact checker output that exactly one class is of oriented bridge type.
- An explicit normalization map from that class to `[2,2,1] / [1,4,4]`.
- A disposition for every other class: symmetry duplicate, earlier closed branch, or local infeasibility.

## Why this is enough

Once the above is fixed, the remaining theorem step is immediate:

- `032` reduces to the statement that the live front-end seed class is that unique oriented bridge-type class;
- the numerical normal form then follows symbolically with no additional odd-`m` argument.
