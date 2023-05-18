# Local search


## Optimisation problems encountered
1. **8 queens** - can you find a placement of 8 queens on a chessboard such that no two queens attack each other (constraints are the vertical, horizontal and diagonal lines projected by each placed queen)
2. **Magic square** - 3x3 square containing the integers 1 to 9; all rows, columns and diagonals have to sum to 15
3. **Warehouse location** - Optimising a network of warehouses and customers such that the combined cost of the fixed cost of setting up warehouses, plus the transportation to customers, is minimised
4. **Travelling salesman** - Given a set of cities C and a symmetrical distance matrix D encoding pairwise distances, find a tour of minimal cost visiting each city exactly once
5. **Scheduling and sequencing**


## Approaches
1. **K-OPT** - A local search method, used widely for TSPs which explores potential improvements to a tour via swapping 2 or more edges. There is a trade-off between solution quality and computational complexity based on the number of edges (2-OPT being worse-quality but lighter, higher numbers of edge swaps vice-versa), so K-OPT determines a good K via exploration then exploitation


## WIP: tasks
1. Implement 2-OPT
   a. From city coordinates, a function to calculate distance matrix --- DONE
   b. An initialise route function --- DONE
   c. A 2-OPT swap function
   d. An algorithm for iterating over the route, applying the 2-opt swap over and over, until a best route is returned
   e. A way to update the distance matrix
2. Implement K-OPT
3. Speed up Python implementation for larger TSPs
   a. Vectorise distance calculation
   b. Coursera to Numpy coordinate interface
   c. Numba compiling?