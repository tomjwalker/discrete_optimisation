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
![image](https://user-images.githubusercontent.com/37417736/200190853-4bbb1433-8268-4d34-9761-0290e1f4b9c3.png)


Best-first:
- Selects the node (at any stage) with best evaluation

Least discrepancy:
- Trust a greedy heuristic, and move away from the heuristic in a very systematic fashion
- Assumes a good search heuristic is available
- Trusting heuristic means branching left on the search tree
- Branches right means heuristic was wrong
- Limited discrepancy search (LDS):
  -  Avoids mistakes
  -  Explores search tree in increasing order of mistakes
  -  Trusts starting heuristic less and less
-  Explores search space in waves:
  -  No mistakes
  -  One mistake (all branches with one and only one rightwards branch)
  -  Two mistakes (all branches with two and only two rightwards branches)
  -  ...


| Strategy name | Strategy | Prunes? | Memory efficient? | 
| --- | --- | --- | --- |
| Depth first | Go deep | When finds new node worse than the found solution | Space: always have essentially one branch at any one time (assessing all items) | 
| Best first | Go for/from the best so far | When all nodes are worse than found solution | Worst case: explores whole tree; Best case: minimal search. Depends on relaxation | 
| Least discrepancy | Trusts greedy heuristic | When all nodes are worse than found solution | Depending on implementation, trade-off between time efficiency and space efficiency | 
