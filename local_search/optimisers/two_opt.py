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
    for i in enumerate(node_coordinates):
        for j in enumerate(node_coordinates):
            distance_matrix[i][j] = local_length(node_coordinates[i], node_coordinates[j])
    return distance_matrix


def initialise_route(node_coordinates):
    """Generates a random tour of all points in the coordinate array (passing each only once, with the same start and
    end point)"""

    num_points = len(node_coordinates)
    route = list(range(num_points))
    random.shuffle(route)

    # Add start point to end
    route.append(route[0])

    return route


def swap_two_opt(route, vertex_i, vertex_j):
    """Given a route and two target vertices, reorders the route (returns a new permutation of the points)"""
    pass


def two_opt_solver(distance_matrix):
    pass

#
#
# if __name__ == "__main":


print(EXAMPLE_NODE_COORDS)