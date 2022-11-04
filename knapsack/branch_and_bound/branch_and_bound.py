import numpy as np
from math import ceil


class Node:
    def __init__(self, decision_string=None):
        self.decision_string = decision_string
        self.evaluation = None
        self.left = None
        self.right = None

    def __repr__(self):

        indent = ceil(
            2 * len(self.decision_string) / 3) * " "  # About 2 spaces works well as indents when dss are len=3

        # Deal with cases where children haven't yet been assigned keys
        child_strings = []
        for child in [self.left, self.right]:
            try:
                child_string = child.decision_string
            except NameError:
                child_string = "[]"
            child_strings.append(child_string)

        # Generate string representation
        string_representation = f"""
        {indent}{indent}{self.decision_string}
        {indent}/{indent}{indent}{indent}\\
        {child_strings[0]}{indent}{indent}{indent}{child_strings[1]}
        """
        return string_representation


def decision_string_to_array(decision_string):
    array = np.zeros(len(decision_string))
    for idx, char in enumerate(decision_string):
        if char == "x":
            array[idx] = None
        elif char == "1":
            array[idx] = 1
        elif char != "0":
            raise ValueError("Character must be one of {0, 1, x}")
    return array


values = np.array([45, 48, 35])
weights = np.array([5, 8, 3])
capacity = 10


def _calculate_value_densities(item_values, item_weights):
    return item_values / item_weights


def sort_items_by_density(item_values, item_weights):
    value_densities = _calculate_value_densities(item_values, item_weights)
    sort_descending_order = (np.argsort(-value_densities))  # -ve sign for sorting descending
    item_values_sorted = item_values[sort_descending_order]
    item_weights_sorted = item_weights[sort_descending_order]
    return item_values_sorted, item_weights_sorted


class Incumbent:
    def __init__(self):
        self.best_node_key = None
        self.best_node_value = 0

    def update(self, key, value):
        self.best_node_key = key
        self.best_node_value = value


def _get_current_value(item_values_sorted, decision_array):
    return (item_values_sorted * (decision_array == 1)).sum()


def _get_remaining_capacity(item_weights_sorted, decision_array, knapsack_capacity):
    weights_selected = item_weights_sorted * (decision_array == 1)
    cumulative_weight = np.cumsum(weights_selected)
    remaining_capacities = knapsack_capacity - cumulative_weight
    last_determined_decision = np.argmax(np.isnan(decision_array)) - 1
    if (~np.isnan(decision_array)).sum() == 0:
        # Deal with the root case, where no decisions have yet been taken (decision array all Nones)
        remaining_capacity = knapsack_capacity
    else:
        remaining_capacity = remaining_capacities[last_determined_decision]
    return remaining_capacity


def _get_optimistic_evaluation(item_weights_sorted, decision_array, knapsack_capacity, item_values_sorted):
    # Assume all (currently undefined) children item decisions are selected
    decision_array_optimistic = decision_array.copy()
    decision_array_optimistic[np.isnan(decision_array_optimistic)] = 1

    # Calculate cumulative weight of assumed decisions, and get index where knapsack capacity exceeded
    weights_selected = item_weights_sorted * decision_array_optimistic
    cumulative_weight = np.cumsum(weights_selected)
    remaining_capacity = knapsack_capacity - cumulative_weight
    index_exceeded = np.argmax(remaining_capacity < 0)  # argmax gives first index where condition is true

    # Get fraction of item (at exceed position) which would satisfy weight
    remaining_capacity_before_item = remaining_capacity[index_exceeded - 1]
    problem_item_weight = item_weights_sorted[index_exceeded]
    feasible_fraction = remaining_capacity_before_item / problem_item_weight

    # Get value of knapsack with this linear relaxation
    decision_array_full_items = decision_array_optimistic.copy()
    decision_array_full_items[index_exceeded:] = 0
    full_values_selected = (item_values_sorted * decision_array_full_items).sum()
    fractional_item_selected = item_values_sorted[index_exceeded] * feasible_fraction
    optimistic_evaluation = full_values_selected + fractional_item_selected

    return optimistic_evaluation


def evaluate_node(node, item_values_sorted, item_weights_sorted, knapsack_capacity):
    decision_array = decision_string_to_array(node.decision_string)
    current_value = _get_current_value(item_values_sorted, decision_array)
    remaining_capacity = _get_remaining_capacity(item_weights_sorted, decision_array, knapsack_capacity)
    optimistic_evaluation = _get_optimistic_evaluation(
        item_weights_sorted,
        decision_array,
        knapsack_capacity,
        item_values_sorted,
    )

    node.evaluation = {
        "current_value": current_value,
        "remaining_capacity": remaining_capacity,
        "optimistic_evaluation": optimistic_evaluation,
    }


def generate_child_string(parent_decision_string, child_decision):
    index_first_unknown = parent_decision_string.find("x")
    child_decision_string = parent_decision_string[:index_first_unknown] + \
        str(int(child_decision)) + \
        parent_decision_string[(index_first_unknown + 1):]
    return child_decision_string


def check_if_node_max_depth(node):
    # If last character is anything other than "x" (0 or 1) assume decisions still to be made
    return node.decision_string[-1] != "x"


def depth_first_search(
        parent_node,
        incumbent_best_selection,
        item_values_sorted,
        item_weights_sorted,
        knapsack_capacity
):
    for (decision, child) in {1: parent_node.left, 0: parent_node.right}.items():

        child = Node()
        child.decision_string = generate_child_string(parent_node.decision_string, decision)
        evaluate_node(child, item_values_sorted, item_weights_sorted, knapsack_capacity)

        print(f"Evaluating {child.decision_string}")
        print(f"Current incumbent decisions = {incumbent_best_selection.best_node_key}")
        print(f"Current incumbent value = {incumbent_best_selection.best_node_value}")

        is_max_depth = check_if_node_max_depth(child)
        is_node_feasible = child.evaluation["remaining_capacity"] >= 0

        if is_node_feasible:
            if child.evaluation["current_value"] > incumbent_best_selection.best_node_value:
                if is_max_depth:
                    # If node is a max depth node - all decisions taken e.g. "101"...
                    # and it supersedes incumbent best value found...
                    # Replace incumbent best in register
                    incumbent_best_selection.best_node_key = child.decision_string
                    incumbent_best_selection.best_node_value = child.evaluation["current_value"]
                    print(f"NEW BEST FOUND! Best value {incumbent_best_selection.best_node_value}")

                else:
                    # If decisions still to be taken, but current optimistic estimate is exceeding current
                    # best so far; continue down search tree
                    depth_first_search(
                        child,
                        incumbent_best_selection,
                        item_values_sorted,
                        item_weights_sorted,
                        knapsack_capacity
                    )


if __name__ == "__main__":

    # Order items by value density (best to worst)
    values_sorted, weights_sorted = sort_items_by_density(values, weights)

    # Instantiate root node and incumbent best register
    root = Node("xxx")
    incumbent_best = Incumbent()
    evaluate_node(root, values_sorted, weights_sorted, capacity)

    is_node_max_depth = check_if_node_max_depth(root)
    is_feasible = root.evaluation["remaining_capacity"] >= 0

    # temp input for future function
    node = root

    if is_feasible and not is_node_max_depth:
        depth_first_search(
            root,
            incumbent_best,
            values_sorted,
            weights_sorted,
            capacity
        )









stopper = 1
