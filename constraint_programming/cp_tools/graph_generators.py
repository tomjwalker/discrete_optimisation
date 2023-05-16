import numpy as np


class DirectedGraph:
    def __init__(self, num_nodes):
        self.nodes = np.arange(num_nodes)
        self._generate_random_directed_graph()

    def _generate_random_directed_graph(self):
        """
        Basic graph generator, ensures valid edges (nodes don't connect to themselves) but little else:
         - doesn't remove edge redundancies (is a directed graph)
         - doesn't ensure connected graph
        :return:
        """

        self.edges = []
        # While loop ensures that if the random graph generator of the inner for loop returns an empty graph (unlikely),
        # the inner loop will be rerun until a non-empty graph exists
        while len(self.edges) == 0:
            for node in self.nodes:
                # Get list of available nodes which this node could connect to (not including itself)
                available_nodes = self.nodes.copy()
                available_nodes = available_nodes[available_nodes != node]

                # Select adjacent nodes at random
                # TODO: have available_nodes as numpy array from start (replace pop above with numpy equivalent)
                available_nodes = np.array(available_nodes)
                select = np.random.choice([False, True], len(available_nodes))
                neighbouring_nodes = available_nodes[select]

                # Structure output as list of (list of) node pairs (this node to one of its neighbours)
                for neighbouring_node in neighbouring_nodes:
                    self.edges.append([node, neighbouring_node])


class UndirectedGraph(DirectedGraph):
    def __init__(self, num_nodes):
        super().__init__(num_nodes)
        self._generate_random_undirected_graph()

    def _generate_random_undirected_graph(self):
        """
        Removes duplicate edges from _generate_random_directed_graph to make it undirected (e.g. only one of [0, 2] and
        [2, 0] in the edge list
        :return:
        """

        self._generate_random_directed_graph()

        undirected_graph = []
        for edge in self.edges:
            # Order edge nodes low to high, so duplicates can be spotted and ignored in if statement below
            ordered_edge = list(np.sort(edge))
            if ordered_edge not in undirected_graph:
                undirected_graph.append(ordered_edge)

        self.edges = undirected_graph


class ConnectedUndirectedGraph(UndirectedGraph):
    def __init__(self, num_nodes):
        super().__init__(num_nodes)
        self._generate_random_connected_graph()

    def _count_distinct_graphs(self):

        graphs = [set(self.edges[0])]    # Initialise with first edge
        for edge in self.edges[1:]:
            for graph in graphs:
                if len(graph.intersection(set(edge))) > 0:
                    pass

    def _generate_random_connected_graph(self):
        """
        On top of _generate_random_directed_graph, ensures the graph is connected (single graph, not multiple graphs)
        :return:
        """

        self._generate_random_undirected_graph()

        # Count graphs
        num_graphs = self._count_distinct_graphs()

        # If number of graphs > 1, connect up with connecting algorithm



        # TODO: code up an algorithm which ensures connected graphs given an input graph
        # raise ValueError("Haven't yet coded up this function")


class CartographicGraph(ConnectedUndirectedGraph):
    def __init__(self, num_nodes):
        super().__init__(num_nodes)
        self._generate_random_cartographic_graph()

    def _generate_random_cartographic_graph(self):
        """
        On top of _generate_random_connected_graph, applies additional topological constraints inherent in 2D maps, e.g.
        - country 1 can touch all (internally) neighbouring countries 2, 3, 4 and 5 with an upper overlap
        - country 2 can touch all (internally) neighbouring countries 3, 4 and 5 with a lower overlap
        - but then country 3 can't also touch country 5 as the upper and lower overlap tricks have both been used up
        :return:
        """

        self._generate_random_connected_graph()
        # TODO: could be hard / take a shortcut by reading into this problem
        # This could be a constraint programming problem in itself!
        raise ValueError("Haven't yet coded up this function")


if __name__ == "__main__":
    graph = CartographicGraph(5)
    print(graph.edges)
