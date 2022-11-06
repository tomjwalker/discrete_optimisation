import numpy as np


def generate_knapsack_problem_simple(num_items, max_allowed_value, max_allowed_weight, max_allowed_capacity):
    """
    Simple, independent generation of knapsack values, weights and capacity
    :param num_items:
    :param max_allowed_value:
    :param max_allowed_weight:
    :param max_allowed_capacity:
    :return:
    """
    values = np.random.choice(max_allowed_value, num_items)
    weights = np.random.choice(np.arange(1, max_allowed_weight + 1), num_items)
    capacity = np.random.choice(np.arange(1, max_allowed_capacity), 1)[0]

    return values, weights, capacity


def generate_knapsack_problem_auto_capacity(num_items, max_allowed_value, max_allowed_weight):
    """
    Capacity is generated as around the average item weight * number of items, with the intention of having an optimal
    decision vector of roughly the same amount of 1s and 0s
    :param num_items:
    :param max_allowed_value:
    :param max_allowed_weight:
    :return:
    """
    values = np.random.choice(max_allowed_value, num_items)
    weights = np.random.choice(np.arange(1, max_allowed_weight + 1), num_items)
    capacity = round((max_allowed_weight * num_items) / 2)
    # Ensure at least one item will be selected
    if capacity < weights.min():
        capacity = weights.min()

    return values, weights, capacity
