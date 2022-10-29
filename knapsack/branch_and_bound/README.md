## Depth first branch-and-bound

Tracking three values at tree nodes:
- Accumulated value from selected items
- Remaining capacity of knapsack
- Optimistic estimate of realisable value continuing along this branch

If optimistic evaluation is worse than best final value found so far in exploration, don't have to explore that branch any further

## Relaxations

Integrity relaxation:
$ x_i /in {0, 1} $
