from branch_and_bound.depth_first import depth_first_search
from dynamic_programming.dynamic_programming import dynamic_programming
from knapsack_tools.knapsack_generators import generate_knapsack_problem_auto_capacity
import time
import pandas as pd
import matplotlib.pyplot as plt


full_results_dfs = None
full_results_dp = None
for num_items in [3, 5, 10, 25, 50, 75, 100, 150, 200, 250]:

    inner_results_dfs = dict()
    inner_results_dp = dict()
    i = 0
    num_knapsack_problems = 10
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

        best_decisions_dfs, optimal_value_dfs = depth_first_search(values, weights, capacity)

        time_end = time.perf_counter()
        total_time_dfs = time_end - time_start

        print(
            f"""
            Number of items: {len(values)}, sub-case: {i}
            Optimal value (DFS): {optimal_value_dfs}, solving_time: {total_time_dfs}
            """
        )

        inner_results_dfs[i] = total_time_dfs

        # Clean up this duplicated block with a decorator
        time_start = time.perf_counter()

        best_decisions_dp, optimal_value_dp = dynamic_programming(values, weights, capacity)

        time_end = time.perf_counter()
        total_time_dp = time_end - time_start

        print(
            f"""
            Optimal value (dynamic programming): {optimal_value_dp}, solving_time: {total_time_dp}
            """
        )

        inner_results_dp[i] = total_time_dp

        i += 1

    inner_results_dfs = pd.Series(inner_results_dfs)
    # noinspection PyUnboundLocalVariable
    inner_results_dfs.name = len(values)

    inner_results_dp = pd.Series(inner_results_dp)
    inner_results_dp.name = len(values)

    full_results_dfs = pd.concat([full_results_dfs, inner_results_dfs], axis=1)
    full_results_dp = pd.concat([full_results_dp, inner_results_dp], axis=1)


def plot_results(full_results, individual_color="blue", average_color="red"):

    fig, ax = plt.subplots()

    full_results.T.plot(style=" o", alpha=0.2, color=individual_color, legend=False, ax=ax)
    mean_results = full_results.mean()
    mean_results.plot(style="-o", color=average_color, ax=ax)

    ax.set_xlabel("Number of items")
    ax.set_ylabel("Solving time")

    plt.show()


plot_results(full_results_dfs)

plot_results(full_results_dp, individual_color="green", average_color="orange")

stopper = 0
