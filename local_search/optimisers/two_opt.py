# TODO: replace random initialise route with improved initialisation (order edges, etc)

import math
import random

import numpy as np

EXAMPLE_NODE_COORDS = np.array(
    [
        [0, 0],
        [0, 0.5],
        [0, 1],
        [1, 1],
        [1, 0],
        # [2, 0],
        # [2, 1],
    ]
)


def local_length(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def generate_distance_matrix(node_coordinates):
    distance_matrix = np.zeros((len(node_coordinates), len(node_coordinates)))
    for i in range(len(node_coordinates)):
        for j in range(len(node_coordinates)):
            distance_matrix[i][j] = local_length(node_coordinates[i], node_coordinates[j])
    return distance_matrix


def initialise_route(node_coordinates, start_node=None):
    """
    Generates a random tour of all points in the coordinate array. End point (same as start point) omitted, as this is
    dealt with intrinsically in the route distance calculation function.

    Returns: route (list)
    """

    num_points = len(node_coordinates)
    route = list(range(num_points))
    if start_node is None:
        random.shuffle(route)
    else:
        route_start = [start_node]
        route_remainder = route.copy()
        route_remainder.remove(start_node)
        random.shuffle(route_remainder)
        route = route_start + route_remainder

    return route


def swap_two_opt(route, node_idx_i, node_idx_j):
    """Given a route and two target vertices, reorders the route (returns a new permutation of the points)"""

    reordered_route = route[:node_idx_i]
    reordered_route += route[node_idx_i:node_idx_j + 1][::-1]
    reordered_route += route[node_idx_j + 1:]

    return reordered_route


def calculate_route_distance(route, distance_matrix):
    """Given a route and the distance matrix encoding distances between all cities, calculates the route length"""

    distance = 0

    for node_index, _ in enumerate(route[:-1]):
        distance += distance_matrix[route[node_index]][route[node_index + 1]]

    # Add final journey back to start
    distance += distance_matrix[route[-1]][route[0]]

    return distance


def two_opt_solver(node_coordinates, start_node=None, log_intermediate=False):
    """
    Loops over all vertices, applying the 2-OPT vertex swapping algorithm.

    WHILE loop ensures:
    - If, for the first pass of the two inner loops, a better route is found, earlier vertices are rechecked
    - If, for the first pass of the two inner loops, no better route is found, the algorithm terminates

    :param node_coordinates: array of node coordinates, e.g. [[0, 0], [0, 1], [1, 1], [1, 0]]
    :param start_node: optional parameter to specify a start node/vertex, e.g. 0
    :param log_intermediate: optional parameter; if True, stores all intermediate graph lengths, for analysis
    :return: best_route (list), solution_distance_log (np.array)

    """

    # Initialise
    best_route = initialise_route(node_coordinates, start_node=start_node)
    distance_matrix = generate_distance_matrix(node_coordinates)
    improved = True
    start_node_idx = 0
    if start_node is not None:
        start_node_idx = 1
    iteration_num = None
    if log_intermediate:
        # Initialise log `solution_distance_log` with length exceeding number of possible swaps (n^3)
        solution_distance_log = np.zeros(len(best_route) ** 3)
        best_distance_log = np.zeros(len(best_route) ** 3)

        solution_distance_log[0] = calculate_route_distance(best_route, distance_matrix)
        best_distance_log[0] = calculate_route_distance(best_route, distance_matrix)
        iteration_num = 0

    while improved:
        improved = False

        for i in range(start_node_idx, len(best_route)):
            for j in range((i + 1), (len(best_route) + 1)):
                new_route = swap_two_opt(best_route, i, j)

                best_route_dist = calculate_route_distance(best_route, distance_matrix)
                new_route_dist = calculate_route_distance(new_route, distance_matrix)

                if new_route_dist < best_route_dist:
                    best_route = new_route
                    improved = True

                if log_intermediate:
                    iteration_num += 1
                    solution_distance_log[iteration_num] = new_route_dist
                    best_distance_log[iteration_num] = best_route_dist

                print(i, j)

    # Trim logs to length of iteration_num
    solution_distance_log = solution_distance_log[:iteration_num + 1]
    best_distance_log = best_distance_log[:iteration_num + 1]

    return best_route, solution_distance_log, best_distance_log


#
#
# if __name__ == "__main__":

coords = EXAMPLE_NODE_COORDS
distance_matrix = generate_distance_matrix(coords)

# # route = initialise_route(coords)
# route = [0, 4, 1, 3, 2]
# print(f"Initial route: {route}")
#
# route_length = calculate_route_distance(route, distance_matrix)
# print(f"Route length: {route_length}")
#
# route_adj = swap_two_opt(route, 1, 3)
# print(f"New route: {route_adj}")
#
# route_length_adj = calculate_route_distance(route_adj, distance_matrix)
# print(f"New route length: {route_length_adj}")

best_solution, solution_distance_log, best_distance_log = two_opt_solver(
    EXAMPLE_NODE_COORDS,
    start_node=0,
    log_intermediate=True
)
min_length = calculate_route_distance(best_solution, distance_matrix)
print(f"Optimised route: {best_solution}")
print(f"Min route length: {min_length}")
print(f"Route distances over time in solver: {solution_distance_log}")
print(f"Best route distances over time in solver: {best_distance_log}")
