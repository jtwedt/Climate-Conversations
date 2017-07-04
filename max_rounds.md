# Computation of max #/rounds

The idea from Judy is to compute how many questions the youngest player can be asked and using that as the upper limit for the number of rounds.

Basically everywhere I say question in this doc I really mean event...

## Ideas 

Concepts we have to consider in doing this:
* Example of a case in which we need to be careful: 
  * Let's say the youngest player has 10 questions available, and the 2nd youngest player has those 10 questions + 2 more = 12 questions. The upper bound on the # of rounds is actually 6, not 5 (aka 10/2), because the older player can draw from those two additional questions. 

## Determine the max number of rounds

Let's see if we can come up with an equation representing the optimal number of rounds. Let $n =$ #/ players, $m =$ the max #/rounds, $p_1...p_i...p_n$ are the players in ascending order of age ($p_1$ is youngest), $q_1...q_i...q_n$ are the numbers of questions available for the $i$th player.

Bounds on possible $m$: 
$q_1/n <= m <= q_1$

We can always verify the above bound in tests for correctness.

1 player case:
* Base case
* $n=1$, $m = q_1$

2 player case:
* $n=2$

\[
\begin{cases}
m = & floor(q_2/2) \textrm{ if } floor(q_2/2) \le q_1
    & q_1 \textrm{ else}
\end{cases}
\]

min(q_2/2, q_1) with integer division (rounded down to nearest int)

Examples for 2-player game:
q_1: 4
q_2: 5
m = 2  (fl(q_2/2) = 2, which is <= q_1, so m=2 )
verify: assign m to q_1 ==> remaining (q_2: 3), assign m to q_2 ==> remain (q_2: 1)
min(5/2, 4) = 2

q_1: 4
q_2: 6
m = 3  (fl(q_2/2) = 3, which is <= q_1, so m=3 )
verify: assign m to q_1 ==> remaining (q_2: 3), assign m to q_2 ==> remain (q_2: 3)
min(6/2, 4) = 3

q_1: 2
q_2: 5
m = 2  (fl(q_2/2) = 2, which is <= q_1, so m=2 )
verify: assign m to q_1 ==> remaining (q_2: 3), assign m to q_2 ==> remain (q_2: 1)
min(5/2, 2) = 2

q_1: 2
q_2: 6
m = 2  (fl(q_2/2) = 3, which is > q_1, so m=2 )
verify: assign m to q_1 ==> remaining (q_2: 4), assign m to q_2 ==> remain (q_2: 2)
min(6/2, 2) = 2

q_1: 2
q_2: 3
m = 1 (fl(q_2/2) = 1, which is <= q_1, so m=1 )
verify: assign m to q_1 ==> remaining (q_2: 2), assign m to q_2 ==> remain (q_2: 1)
min(3/2, 2) = 1

Can this be extended to 3 players? $n$ players?

3 player case:
* $n=3$

To validate:
q_2 must have at least 2*m q's; q_3 >= 3*m q's, etc.

Example:
q_1: 4
q_2: 5
q_3: 15
m = 2
Since 15/3 = 5
min(q_3/3, q_2/2, q_1) = min(15/3, 5/2, 4) = min(5, 2, 4) = 2

**Found the pattern:** $min(q_n/n, ... , q_i/i, ..., q_1/1)$

## Choosing q's for max

* Randomly choose $m$ questions from youngest player's pool
* Remove those questions from the other players' possible pools
* Continue until the oldest player has their questions determined
