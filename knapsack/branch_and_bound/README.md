## Depth first branch-and-bound

Tracking three values at tree nodes:
- Accumulated value from selected items
- Remaining capacity of knapsack
- Optimistic estimate of realisable value continuing along this branch

If optimistic evaluation is worse than best final value found so far in exploration, don't have to explore that branch any further

## Relaxations
Relaxations are used to calculate optimistic evaluations of nodes. Good relaxations are close to the actual optimal result, and can reduce the search space significantly

Capacity relaxation (over-simplistic):
- Ignore constraint $\sum_i{w_ix_i} \le K$

Linear relaxation (more powerful relaxation):
- $x_i \in \{ 0, 1 \}$ relaxed to $0 \le x_i \le 1$
