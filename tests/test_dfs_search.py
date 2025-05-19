import unittest
import os
import json
import networkx as nx
from random import shuffle

import numpy as np
from methods.dfs_spanning_tree import create_spanning_tree, generate_random_matrix, save_to_json, validate_input, save_graph_image

class TestDFSFunctions(unittest.TestCase):

    def test_create_spanning_tree_valid(self):
        """Test the creation of a valid spanning tree using DFS"""
        adj_matrix = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]
        start_vertex = 1
        G_full, T_tree, tree_matrix, vertices_list, error = create_spanning_tree(adj_matrix, start_vertex)
        
        self.assertIsNone(error, "Expected no error during spanning tree creation")
        self.assertEqual(len(G_full.nodes), 3, "The full graph should have 3 vertices")
        self.assertEqual(len(T_tree.nodes), 3, "The spanning tree should have 3 vertices")
        self.assertEqual(vertices_list, [1, 2, 3], "DFS traversal should visit vertices in correct order")

    def test_create_spanning_tree_invalid(self):
        """Test invalid graph input to check if the function raises an error"""
        adj_matrix = [
            [0, 0],
            [0, 0]
        ]
        start_vertex = 1
        G_full, T_tree, tree_matrix, vertices_list, error = create_spanning_tree(adj_matrix, start_vertex)
        
        self.assertIsNotNone(error, "Expected error for graph that doesn't form a spanning tree")
        self.assertEqual(error, "Graph is not connected", "Expected error message for non-connected graph")

    def test_generate_random_matrix(self):
        """Test random adjacency matrix generation for a connected graph"""
        n = 5
        adj_matrix = generate_random_matrix(n)
    
        self.assertEqual(len(adj_matrix), n, "The adjacency matrix should have n rows")
        self.assertEqual(len(adj_matrix[0]), n, "The adjacency matrix should have n columns")
    
        G = nx.from_numpy_array(np.array(adj_matrix))
        components = list(nx.connected_components(G))
        self.assertEqual(len(components), 1, "The generated graph should be connected")


    def test_save_to_json(self):
        """Test saving adjacency and tree matrices to a JSON file"""
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        start_vertex = 1
        tree_matrix = [
            [0, 1],
            [1, 0]
        ]
        
        filename = "static/dynamic/logos/dfs_data.json"
        save_to_json(adj_matrix, start_vertex, tree_matrix, filename)
        
        self.assertTrue(os.path.exists(filename), "The JSON file should be created")
        
        # Verify the content of the saved JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['dfs']['adjacency_matrix'], adj_matrix, "Adjacency matrix in JSON doesn't match the input")
            self.assertEqual(data['dfs']['start_vertex'], start_vertex, "Start vertex in JSON doesn't match the input")
            self.assertEqual(data['dfs']['tree_matrix'], tree_matrix, "Tree matrix in JSON doesn't match the input")
        
        # Clean up the generated file after test
        os.remove(filename)

    def test_save_graph_image(self):
        """Test saving the graph image to a file"""
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        start_vertex = 1
        G_full, T_tree, tree_matrix, vertices_list, error = create_spanning_tree(adj_matrix, start_vertex)
        
        filename = "static/dynamic/graphs/spanning_tree_dfs_1.png"
        graph_image_path = save_graph_image(G_full, T_tree, filename)
        
        self.assertTrue(os.path.exists(graph_image_path), "The graph image file should be created")
        
        # Clean up the generated image file after test
        os.remove(graph_image_path)

    def test_validate_input_valid(self):
        """Test validating correct input data"""
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        error = validate_input(2, 1, adj_matrix)
        self.assertIsNone(error, "Expected no validation error for valid input")

    def test_validate_input_invalid_vertices(self):
        """Test invalid number of vertices"""
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        error = validate_input(10, 1, adj_matrix)  # Invalid number of vertices
        self.assertEqual(error, "Number of vertices must be an integer between 1 and 8", "Expected validation error for invalid number of vertices")

    def test_validate_input_invalid_start_vertex(self):
        """Test invalid starting vertex"""
        adj_matrix = [
            [0, 1],
            [1, 0]
        ]
        error = validate_input(2, 3, adj_matrix)  # Invalid start vertex (3 for a 2-vertex graph)
        self.assertEqual(error, "Starting vertex must be an integer between 1 and number of vertices", "Expected validation error for invalid starting vertex")

    def test_validate_input_invalid_matrix(self):
        """Test invalid adjacency matrix (non-symmetric)"""
        adj_matrix = [
            [0, 1],
            [0, 0]
        ]
        error = validate_input(2, 1, adj_matrix)  # Invalid matrix (not symmetric)
        self.assertEqual(error, "Adjacency matrix must be symmetric", "Expected validation error for non-symmetric adjacency matrix")

    def test_validate_input_invalid_matrix_elements(self):
        """Test invalid matrix elements (non-integer)"""
        adj_matrix = [
            [0, 1],
            [1, "a"]
        ]
        error = validate_input(2, 1, adj_matrix)  # Invalid matrix element ("a" instead of 0 or 1)
        self.assertEqual(error, "Matrix elements must be integers 0 or 1", "Expected validation error for invalid matrix element")

    def test_validate_input_invalid_self_loops(self):
        """Test adjacency matrix with self-loops"""
        adj_matrix = [
            [1, 0],
            [0, 0]
        ]
        error = validate_input(2, 1, adj_matrix)  # Invalid matrix (self-loop at index 0)
        self.assertEqual(error, "Self-loops (diagonal elements) are not allowed", "Expected validation error for self-loop in adjacency matrix")

if __name__ == '__main__':
    unittest.main()
