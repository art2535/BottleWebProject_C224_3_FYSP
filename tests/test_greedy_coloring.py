# test_greedy_coloring.py

import unittest
from methods.graph_coloring_algorithm import greedy_graph_coloring

class TestGreedyGraphColoring(unittest.TestCase):
    def assert_valid_coloring(self, adjacency, coloring):
        """
        Ensures that no two adjacent vertices have the same color.
        """
        n = len(adjacency)
        for i in range(n):
            for j in range(n):
                if adjacency[i][j] == 1:
                    self.assertIn(i, coloring)
                    self.assertIn(j, coloring)
                    self.assertNotEqual(
                        coloring[i], coloring[j],
                        f"Adjacent vertices {i} and {j} share color {coloring[i]}"
                    )

    def test_greedyGraphColoring_emptyGraph_ReturnsEmptyColoring(self):
        """Empty graph."""
        adjacency = []
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(colors, {})
        self.assertEqual(num_colors, 0)
        self.assertEqual(mat, adjacency)

    def test_greedyGraphColoring_singleVertexGraph_ReturnsSingleColor(self):
        """Single isolated vertex."""
        adjacency = [[0]]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertDictEqual(colors, {0: 1})
        self.assertEqual(num_colors, 1)
        self.assertEqual(mat, adjacency)

    def test_greedyGraphColoring_2x2ConnectedGraph_ReturnsTwoDifferentColors(self):
        """Two connected vertices should receive different colors (1 and 2)."""
        adjacency = [
            [0, 1],
            [1, 0]
        ]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(num_colors, 2)
        self.assertDictEqual(colors, {0: 1, 1: 2})

    def test_greedyGraphColoring_2x2DisconnectedGraph_ReturnsOneColor(self):
        """Two disconnected vertices can both have the same color."""
        adjacency = [
            [0, 0],
            [0, 0]
        ]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(num_colors, 1)
        self.assertDictEqual(colors, {0: 1, 1: 1})

    def test_greedyGraphColoring_4x4PathGraph_ReturnsTwoColors(self):
        """A linear graph with 4 vertices (path) should require 2 colors."""
        adjacency = [
            [0,1,0,0],
            [1,0,1,0],
            [0,1,0,1],
            [0,0,1,0]
        ]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(mat, adjacency)
        self.assertEqual(num_colors, 2)
        self.assert_valid_coloring(adjacency, colors)

    def test_greedyGraphColoring_4x4FullyConnectedGraph_ReturnsFourColors(self):
        """A fully connected graph (clique) of 4 vertices requires 4 colors."""
        n = 4
        adjacency = [[0 if i==j else 1 for j in range(n)] for i in range(n)]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(mat, adjacency)
        self.assertEqual(num_colors, 4)
        expected = {0:1, 1:2, 2:3, 3:4}
        self.assertDictEqual(colors, expected)

    def test_greedyGraphColoring_5x5DisconnectedComponents_ReturnsThreeColors(self):
        """
        Two components: K3 and K2.
        Verifies that the algorithm correctly colors both components
        and that the total number of colors matches the heaviest component (K3 → 3 colors).
        """
        adjacency = [
            [0,1,1,0,0],
            [1,0,1,0,0],
            [1,1,0,0,0],
            [0,0,0,0,1],
            [0,0,0,1,0]
        ]
        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(mat, adjacency)
        self.assertEqual(num_colors, 3)
        self.assert_valid_coloring(adjacency, colors)

    def test_greedyGraphColoring_8x8ChainGraph_ReturnsAtMostTwoColors(self):
        """
        Maximum allowed number of vertices (8) in a chain.
        A chain is a bipartite graph, so num_colors should be ≤ 2.
        """
        n = 8
        adjacency = [[0]*n for _ in range(n)]
        for i in range(n-1):
            adjacency[i][i+1] = adjacency[i+1][i] = 1

        colors, num_colors, mat = greedy_graph_coloring(adjacency)
        self.assertEqual(mat, adjacency)
        self.assertTrue(num_colors <= 2)
        self.assert_valid_coloring(adjacency, colors)

if __name__ == '__main__':
    unittest.main()
