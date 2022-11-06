from branch_and_bound.depth_first import depth_first_search
from knapsack_tools.knapsack_generators import generate_knapsack_problem_auto_capacity
import time
import pandas as pd
import matplotlib.pyplot as plt


full_results = None
for num_items in [3, 5, 10, 25, 50, 100, 200, 275]:

    inner_results = dict()
    i = 0
    num_knapsack_problems = 4
    while i < num_knapsack_problems:

        MAX_ALLOWED_ITEM_VALUE = 20
        MAX_ALLOWED_ITEM_WEIGHT = 5
        values, weights, capacity = generate_knapsack_problem_auto_capacity(
            num_items=num_items,
            max_allowed_value=MAX_ALLOWED_ITEM_VALUE,
            max_allowed_weight=MAX_ALLOWED_ITEM_WEIGHT,
        )

        # print(f"Values: {values}, weights: {weights}, capacity: {capacity}")

        time_start = time.perf_counter()

        best_decisions, optimal_value = depth_first_search(values, weights, capacity)

        time_end = time.perf_counter()
        total_time = time_end - time_start

        print(
            f"""
            Number of items: {len(values)}, sub-case: {i}
            Optimal_value: {optimal_value}, solving_time: {total_time}
            """
        )

        inner_results[i] = total_time

        i += 1

    inner_results = pd.Series(inner_results)
    inner_results.name = len(values)

    full_results = pd.concat([full_results, inner_results], axis=1)


def plot_results(full_results):

    fig, ax = plt.subplots()

    full_results.T.plot(style=" o", alpha=0.2, color="blue", legend=False, ax=ax)
    mean_results = full_results.mean()
    mean_results.plot(style="-o", color="red", ax=ax)

    ax.set_xlabel("Number of items")
    ax.set_ylabel("Solving time")

    plt.show()


plot_results(full_results)


stopper = 0