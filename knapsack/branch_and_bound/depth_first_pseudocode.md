**Inputs**: values (list of floats), weights (list of floats), capacity (float)
**Outputs**: optimal decision (list of booleans), maximised value (float)

**Algorithm:**
1. Calculate value density (values / weights)
2. Sort items by value density (highest first)
3. Initialise **root node** of search tree
4. Initialise **incumbent best**, an object which stores the node key and value of the best search tree node (maximum value, node is at max depth)
5. Evaluate node:
  a. Generate decision string
  b. Calculate optimistic estimate according to given relaxation
  c. Check if node at max depth
  d. If node not at max depth and solution is feasible:
      5. Apply DFS(node, incumbent), defined as:
          a. For child_node in node.children (ordered so that left is first in the list):
              i. Generate child_node decision string (key for the node, which encodes decisions already taken and yet to take, e.g. "10x" at level 2
              ii. Evaluate node (current value, remaining capacity, optimistic evaluation)
              iii. Check if child_node is max depth node (e.g. "101", no remaining decisions to take)
              iv. If child_node is max depth:
                  1. If beats incumbent value, update incumbent object
              v. Else:
                  1. If feasible (remaining capacity +ve) and optimistic estimate beats incumbent value:
                      a. Apply DFS (child_node, incumbent)
