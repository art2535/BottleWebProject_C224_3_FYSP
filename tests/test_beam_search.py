import unittest
from methods.beam_search_spanning_tree import beam_search_spanning_tree

class TestBeamSearch(unittest.TestCase):
    def count_edges(self, matrix):
        """Counts the number of edges in an adjacency matrix."""
        if isinstance(matrix, str):
            return None
        return sum(sum(row) for row in matrix) // 2 if matrix else 0

    def test_beamSearch_3x3FullyConnected_ReturnsMinimumSpanningTree(self):
        """Checks MST for a 3x3 fully connected graph with distinct weights."""
        n = 3
        adjacency_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        weight_matrix = [
            [0, 5, 1],
            [5, 0, 4],
            [1, 4, 0]
        ]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix)
        expected = [
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 0]
        ]
        self.assertIsInstance(result, list)
        self.assertEqual(self.count_edges(result), 2)
        self.assertEqual(result, expected)

    def test_beamSearch_7x7FullyConnected_ReturnsValidSpanningTree(self):
        """Checks if MST is correctly built for a 7x7 fully connected graph."""
        n = 7
        adjacency_matrix = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
        weight_matrix = [[(i + j + 1) % 10 + 1 if i != j else 0 for j in range(n)] for i in range(n)]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, beam_width=3)
        self.assertIsInstance(result, list)
        self.assertEqual(self.count_edges(result), 6)
        for i in range(n):
            for j in range(n):
                self.assertIn(result[i][j], [0, 1])
                self.assertEqual(result[i][j], result[j][i])

    def test_beamSearch_5x5SameWeights_ReturnsValidSpanningTree(self):
        """Checks if MST is valid for a 5x5 graph where all edges have equal weights."""
        n = 5
        adjacency_matrix = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
        weight_matrix = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix)
        self.assertIsInstance(result, list)
        self.assertEqual(self.count_edges(result), 4)
        for i in range(n):
            for j in range(n):
                self.assertIn(result[i][j], [0, 1])
                self.assertEqual(result[i][j], result[j][i])

    def test_beamSearch_SparseConnectedGraph_ReturnsSameAsInput(self):
        """Verifies that a sparse but connected graph returns the correct MST (same as input)."""
        n = 4
        adjacency_matrix = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        weight_matrix = [
            [0, 2, 0, 0],
            [2, 0, 3, 0],
            [0, 3, 0, 4],
            [0, 0, 4, 0]
        ]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix)
        expected = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        self.assertIsInstance(result, list)
        self.assertEqual(self.count_edges(result), 3)
        self.assertEqual(result, expected)

    def test_beamSearch_DisconnectedGraph_ReturnsErrorMessage(self):
        """Checks if a disconnected graph correctly returns an error message."""
        n = 4
        adjacency_matrix = [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 0]
        ]
        weight_matrix = [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 0]
        ]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix)
        self.assertIsInstance(result, str)
        self.assertIn("not built", result)

    def test_beamSearch_5x5WeightedGraph_ReturnsValidSpanningTree(self):
        """Tests MST generation on a 5x5 graph with varied weights."""
        n = 5
        adjacency_matrix = [
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [0, 1, 1, 0, 1],
            [0, 0, 1, 1, 0]
        ]
        weight_matrix = [
            [0, 100, 1, 0, 0],
            [100, 0, 50, 2, 0],
            [1, 50, 0, 2, 1],
            [0, 2, 2, 0, 3],
            [0, 0, 1, 3, 0]
        ]
        result = beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, beam_width=3)
        self.assertIsInstance(result, list)
        self.assertEqual(self.count_edges(result), 4)
        for i in range(n):
            for j in range(n):
                self.assertIn(result[i][j], [0, 1])
                self.assertEqual(result[i][j], result[j][i])

if __name__ == '__main__':
    unittest.main()