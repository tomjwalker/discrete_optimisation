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


## Search strategies

Depth-first:
- Prunes when a node estimation is worse than best-found solution

![image](https://user-images.githubusercontent.com/37417736/198833336-5301480f-d9b0-4e97-9629-3ea05d0f903d.png)


Best-first:
- Selects the node (at any stage) with best evaluation

Least discrepancy:
- Trust a greedy heuristic, and move away from the heuristic in a very systematic fashion


| Strategy name | Strategy | Prunes? | Memory efficient? | 
| --- | --- | --- | --- |
| Depth first | Strategy | Prunes? | Memory efficient? | 
| Best first | Go for/from the best so far | When all nodes are worse than found solution | - Worst case: explores whole tree \ Best case: minimal search. Depends on relaxation | 
| Least discrepancy | Strategy | Prunes? | Memory efficient? | 
