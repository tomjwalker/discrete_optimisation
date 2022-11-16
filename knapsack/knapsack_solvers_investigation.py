from optimisers.depth_first import depth_first_search
from optimisers.dynamic_programming import dynamic_programming
from knapsack_tools.knapsack_generators import generate_knapsack_problem_auto_capacity
from optimisers.brute_force import brute_force
import time
import pandas as pd
import matplotlib.pyplot as plt


# TODO: a decorator is probably a neater way of doing this
def time_and_run_optimiser(optimiser_function, optimiser_name, knapsack_case, verbose=True):

    (values, weights, capacity) = knapsack_case

    time_start = time.perf_counter()

    best_decisions, optimal_value = optimiser_function(values, weights, capacity)

    time_end = time.perf_counter()
    total_time = time_end - time_start

    if verbose:
        print(f"Optimal value ({optimiser_name}): {optimal_value}, solving_time: {total_time}")

    return best_decisions, optimal_value, total_time


full_results_dfs = None
full_results_dp = None
full_results_bf = None
for num_items in [3, 5, 10, 25, 50, 75, 100, 150, 200, 250]:

    inner_results_dfs = dict()
    inner_results_dp = dict()
    inner_results_bf = dict()
    i = 0
    num_knapsack_problems = 10
    while i < num_knapsack_problems:

        MAX_ALLOWED_ITEM_VALUE = 20
        MAX_ALLOWED_ITEM_WEIGHT = 5
        knapsack_problem = generate_knapsack_problem_auto_capacity(
            num_items=num_items,
            max_allowed_value=MAX_ALLOWED_ITEM_VALUE,
            max_allowed_weight=MAX_ALLOWED_ITEM_WEIGHT,
        )

        # print(f"Values: {values}, weights: {weights}, capacity: {capacity}")
        print(f"Number of items: {len(knapsack_problem[0])}, sub-case: {i}")

        best_decisions, optimal_value, inner_results_dfs[i] = time_and_run_optimiser(
            depth_first_search,
            "depth_first_search",
            knapsack_problem,
            verbose=True
        )

        _, _, inner_results_dp[i] = time_and_run_optimiser(
            dynamic_programming,
            "dynamic_programming",
            knapsack_problem,
            verbose=True
        )

        i += 1

    inner_results_dfs = pd.Series(inner_results_dfs)
    inner_results_dfs.name = len(knapsack_problem[0])

    inner_results_dp = pd.Series(inner_results_dp)
    inner_results_dp.name = len(knapsack_problem[0])

    full_results_dfs = pd.concat([full_results_dfs, inner_results_dfs], axis=1)
    full_results_dp = pd.concat([full_results_dp, inner_results_dp], axis=1)

full_results_bf = None
for num_items in [3, 4, 5, 6, 8, 10, 15, 20]:

    inner_results_bf = dict()
    i = 0
    num_knapsack_problems = 5
    while i < num_knapsack_problems:

        MAX_ALLOWED_ITEM_VALUE = 20
        MAX_ALLOWED_ITEM_WEIGHT = 5
        knapsack_problem = generate_knapsack_problem_auto_capacity(
            num_items=num_items,
            max_allowed_value=MAX_ALLOWED_ITEM_VALUE,
            max_allowed_weight=MAX_ALLOWED_ITEM_WEIGHT,
        )

        # print(f"Values: {values}, weights: {weights}, capacity: {capacity}")
        print(f"Number of items: {len(knapsack_problem[0])}, sub-case: {i}")

        _, _, inner_results_bf[i] = time_and_run_optimiser(
            brute_force,
            "brute_force",
            knapsack_problem,
            verbose=True
        )

        i += 1

    inner_results_bf = pd.Series(inner_results_bf)
    inner_results_bf.name = len(knapsack_problem[0])

    full_results_bf = pd.concat([full_results_bf, inner_results_bf], axis=1)


def plot_results(full_results, axis, ylim_max=None, solver_name=None, individual_color="blue", average_color="red"):

    full_results.T.plot(style=" o", alpha=0.2, color=individual_color, legend=False, ax=axis)
    mean_results = full_results.mean()
    mean_results.plot(style="-o", color=average_color, ax=axis)

    axis.set_xlabel("Number of items")
    axis.set_ylabel("Solving time")
    axis.set_title(f"{solver_name}")
    if ylim_max is not None:
        axis.set_ylim(0, ylim_max)


fig, ax = plt.subplots(2, 2)

# Brute force (tries all combos), for baseline - truncated to smaller max number of items, as explodes!
plot_results(full_results_bf, axis=ax[0][0], solver_name="Brute Force",
             individual_color="yellow", average_color="purple")

max_time_dynamic_prog = full_results_dp.mean().max()
max_time_branch_bound = full_results_dfs.mean().max()
ylim_max = 1.2 * max(max_time_dynamic_prog, max_time_branch_bound)
plot_results(full_results_dfs, axis=ax[1][0], ylim_max=ylim_max, solver_name="Depth-first Search")
plot_results(full_results_dp, axis=ax[1][1], ylim_max=ylim_max, solver_name="Dynamic Programming",
             individual_color="green", average_color="orange")

plt.tight_layout()
plt.show()

stopper = 0
