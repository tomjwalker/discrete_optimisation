import numpy as np
from itertools import product
import time


class Incumbent:
    def __init__(self):
        self.best_key = None
        self.best_value = 0

    def update(self, key, value):
        self.best_key = key
        self.best_value = value


def brute_force(values, weights, capacity):

    incumbent_best = Incumbent()

    num_items = len(values)

    for decision_tuple in product([1, 0], repeat=num_items):
        decision_array = np.array(decision_tuple)

        knapsack_value = (values * decision_array).sum()
        knapsack_weight = (weights * decision_array).sum()

        # If feasible, check if beats incumbent best and if so, update incumbent best
        if (knapsack_weight <= capacity) and knapsack_value > incumbent_best.best_value:

            incumbent_best.best_key = decision_array
            incumbent_best.best_value = knapsack_value

        optimal_decisions = incumbent_best.best_key
        optimal_value = incumbent_best.best_value

    return optimal_decisions, optimal_value


if __name__ == "__main__":

    values = np.array([34, 66, 22, 10, 55, 35, 28, 140])
    weights = np.array([3, 6, 2, 1, 5, 3, 2, 10])
    capacity = 11

    time_start = time.perf_counter()

    best_decision_register = brute_force(values, weights, capacity)

    time_end = time.perf_counter()
    total_time_dfs = time_end - time_start

    print(total_time_dfs)
    print(best_decision_register.best_key)
    print(best_decision_register.best_value)

