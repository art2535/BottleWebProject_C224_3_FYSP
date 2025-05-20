import os
import unittest
import networkx as nx
import random

from methods.dfs_spanning_tree import create_spanning_tree, generate_random_matrix, save_graph_image, validate_input

class TestGraphAlgorithms(unittest.TestCase):
    """
    Unit tests for graph algorithms related to building a spanning tree using DFS.
    """

    def test_createSpanningTree_3x3FullyConnected_ReturnsSpanningTree(self):
        """
        Test that a fully connected 3x3 adjacency matrix returns a valid spanning tree
        and related graph structures.
        """
        adj_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        start_vertex = 1
        G_full, T_tree, tree_matrix, vertices_list, error = create_spanning_tree(adj_matrix, start_vertex)
        
        self.assertIsNone(error)
        self.assertIsInstance(G_full, nx.Graph)
        self.assertIsInstance(T_tree, nx.Graph)
        self.assertIsInstance(tree_matrix, list)
        self.assertIsInstance(vertices_list, list)
        self.assertEqual(len(tree_matrix), 3)
        self.assertEqual(len(tree_matrix[0]), 3)

    def test_createSpanningTree_4x4Disconnected_ReturnsErrorMessage(self):
        """
        Test that a disconnected 4x4 matrix returns an appropriate error
        and does not return a spanning tree.
        """
        adj_matrix = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]
        start_vertex = 1
        G_full, T_tree, tree_matrix, vertices_list, error = create_spanning_tree(adj_matrix, start_vertex)

        self.assertEqual(error, "Graph is not connected")
        self.assertIsNone(T_tree)
        self.assertIsNone(tree_matrix)
        self.assertIsNone(vertices_list)


    def test_generateRandomMatrix_3Vertices_ReturnsValidAdjacencyMatrix(self):
        """
        Test that a 3x3 random adjacency matrix contains only 0 or 1 values
        and has the correct dimensions.
        """
        adj_matrix = generate_random_matrix(3)
        self.assertEqual(len(adj_matrix), 3)
        self.assertEqual(len(adj_matrix[0]), 3)
        self.assertTrue(all(cell in (0, 1) for row in adj_matrix for cell in row))

    def test_generateRandomMatrix_5Vertices_ReturnsValidAdjacencyMatrix(self):
        """
        Same as above, but for 5 vertices.
        """
        adj_matrix = generate_random_matrix(5)
        self.assertEqual(len(adj_matrix), 5)
        self.assertEqual(len(adj_matrix[0]), 5)
        self.assertTrue(all(cell in (0, 1) for row in adj_matrix for cell in row))

   
    def test_validateInput_ValidInput_ReturnsNone(self):
        """
        Test that valid input parameters return no error.
        """
        adj_matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        error = validate_input(3, 2, adj_matrix)
        self.assertIsNone(error)

    def test_validateInput_InvalidVertices_ReturnsErrorMessage(self):
        """
        Test that invalid number of vertices (e.g., too large) returns an appropriate error.
        """
        adj_matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        error = validate_input(10, 2, adj_matrix)
        self.assertEqual(error, "Number of vertices must be an integer between 1 and 8")

    def test_validateInput_InvalidStartVertex_ReturnsErrorMessage(self):
        """
        Test that an invalid starting vertex returns an appropriate error.
        """
        adj_matrix = [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        error = validate_input(3, 5, adj_matrix)
        self.assertEqual(error, "Starting vertex must be an integer between 1 and number of vertices")

    def test_validateInput_InvalidAdjacencyMatrix_ReturnsErrorMessage(self):
        """
        Test that an incorrectly sized adjacency matrix returns an error.
        """
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        error = validate_input(3, 2, adj_matrix)
        self.assertEqual(error, "Invalid adjacency matrix dimensions")

    def test_validateInput_InvalidMatrixElement_ReturnsErrorMessage(self):
        """
        Test that non-binary matrix elements (e.g., 2) return an error.
        """
        adj_matrix = [
            [0, 1, 2],
            [1, 0, 1],
            [0, 1, 0]
        ]
        error = validate_input(3, 2, adj_matrix)
        self.assertEqual(error, "Matrix elements must be integers 0 or 1")

    def test_validateInput_SelfLoop_ReturnsErrorMessage(self):
        """
        Test that matrices with self-loops (diagonal elements = 1) return an error.
        """
        adj_matrix = [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]
        error = validate_input(3, 2, adj_matrix)
        self.assertEqual(error, "Self-loops (diagonal elements) are not allowed")

   
    def test_saveGraphImage_ValidGraph_ReturnsImagePath(self):
        """
        Test that the image of a graph is saved and the file path returned is correct.
        """
        G_full = nx.Graph()
        G_full.add_edges_from([(0, 1), (1, 2)])
        T_tree = nx.Graph()
        T_tree.add_edges_from([(0, 1)])
        
        filename = save_graph_image(G_full, T_tree)
        self.assertTrue(filename.endswith('.png'))
        self.assertTrue(os.path.exists(filename))


if __name__ == "__main__":
    unittest.main()

