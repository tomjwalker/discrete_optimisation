#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np


def _generate_value_table(item_values, item_weights, knapsack_capacity):
    # initialise table
    optimal_value_table = np.zeros((knapsack_capacity + 1, len(item_values) + 1))

    for j in range(1, optimal_value_table.shape[1]):

        weight_new_item = item_weights[j - 1]
        value_new_item = item_values[j - 1]

        for k in range(0, optimal_value_table.shape[0]):

            value_same_capacity_one_less_item = optimal_value_table[k, j - 1]
            new_optimal_value = value_same_capacity_one_less_item  # initialise

            if weight_new_item <= k:
                value_possible_after_adding_new_item = value_new_item + optimal_value_table[k - weight_new_item, j - 1]
                new_optimal_value = max(
                    (value_same_capacity_one_less_item, value_possible_after_adding_new_item)  # overwrite if necessary
                )

            optimal_value_table[k, j] = new_optimal_value

    return optimal_value_table


def _get_decision_variables(item_values, item_weights, knapsack_capacity, optimal_value_table):
    decision_variables = np.zeros_like(item_values)
    remaining_optimal_value = optimal_value_table[knapsack_capacity, len(item_values)]
    k = knapsack_capacity

    for j in range(optimal_value_table.shape[1] - 2, -1, -1):

        if optimal_value_table[k, j] == remaining_optimal_value:
            decision_variables[j] = 0
        else:
            decision_variables[j] = 1
            k -= item_weights[j]
            remaining_optimal_value = optimal_value_table[k, j]

    return list(decision_variables)


def dynamic_programming(item_values, item_weights, knapsack_capacity):

    optimal_value_table = _generate_value_table(item_values, item_weights, knapsack_capacity)
    best_decisions = _get_decision_variables(item_values, item_weights, knapsack_capacity, optimal_value_table)

    best_value = int(optimal_value_table[-1][-1])
    
    # # prepare the solution in the specified output format
    # output_data = str(value) + ' ' + str(1) + '\n'
    # output_data += ' '.join(map(str, taken))
    return best_decisions, best_value


if __name__ == '__main__':

    values = np.array([34, 66, 22, 10, 55, 35, 28, 140])
    weights = np.array([3, 6, 2, 1, 5, 3, 2, 10])
    capacity = 11

    optimal_decisions, optimal_value = dynamic_programming(values, weights, capacity)
    print(optimal_decisions, optimal_value)
