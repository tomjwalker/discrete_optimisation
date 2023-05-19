import math
import numpy as np
import random


EXAMPLE_NODE_COORDS = np.array(
    [
        [0, 0],
        [0, 0.5],
        [0, 1],
        [1, 1],
        [1, 0],
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
        print(route_remainder)
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


def two_opt_solver(distance_matrix):
    pass


#
#
# if __name__ == "__main":

coords = EXAMPLE_NODE_COORDS
distance_matrix = generate_distance_matrix(coords)


# route = initialise_route(coords)
route = [0, 4, 1, 3, 2]
print(f"Initial route: {route}")

route_length = calculate_route_distance(route, distance_matrix)
print(f"Route length: {route_length}")

route_adj = swap_two_opt(route, 1, 3)
print(f"New route: {route_adj}")

route_length_adj = calculate_route_distance(route_adj, distance_matrix)
print(f"New route length: {route_length_adj}")

print(route_adj)