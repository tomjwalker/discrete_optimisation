# Constraint programming

Technique (orthogonal to bounding heuristics - hence can be used in conjunction to good effect) to reduce search space of optimisation problems by carefully considering the implications of constraints on the domains of the decision variables.


## Optimisation problems encountered
1. **8 queens** - can you find a placement of 8 queens on a chessboard such that no two queens attack each other (constraints are the vertical, horizontal and diagonal lines projected by each placed queen)
2. **Map colouring** - for a given map (graph with nodes as countries and edges encoding adjacencies) find the minimum set of colours which ensures no two adjacent countries are shaded the same
3. **SEND + MORE = MONEY** - assign digits to the letters ensuring the equation works as an addition; additional constraint that no two letters can have the same constraint
4. 