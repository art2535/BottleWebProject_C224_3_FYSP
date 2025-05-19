import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from bottle import request
import random
import os
import json

from logics.json_utils import save_algorithm_record


def create_spanning_tree(adj_matrix, start_vertex):
    """
    Create a spanning tree using DFS from the adjacency matrix.

    This function generates a graph from the given adjacency matrix, performs a 
    Depth-First Search (DFS) starting from the specified vertex to create a spanning 
    tree, and returns the full graph, the spanning tree, the adjacency matrix of the 
    spanning tree, and a list of vertices in the order they were visited. If an error occurs, it returns the error message.
    """
    n = len(adj_matrix)
    G_full = nx.Graph()

    # Add all nodes to the full graph
    G_full.add_nodes_from(range(n))

    # Add edges to the graph, skipping self-loops (i == j)
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                G_full.add_edge(i, j)

    start_vertex = start_vertex - 1  # Convert to 0-based indexing

    try:
        # Perform DFS to get the edges of the spanning tree
        dfs_edges = list(nx.dfs_edges(G_full, source=start_vertex))  
        T_tree = nx.Graph()  
        T_tree.add_nodes_from(range(n))  # Add nodes to the spanning tree
        T_tree.add_edges_from(dfs_edges)  # Add edges to the spanning tree

        # Track the order of visited vertices
        visited_order = list(nx.dfs_preorder_nodes(G_full, source=start_vertex))

        # Convert the spanning tree to an adjacency matrix
        tree_matrix = nx.to_numpy_array(T_tree, dtype=int).tolist()  
        
        # Update vertices_list to match the DFS visit order (1-based indexing)
        vertices_list = [node + 1 for node in visited_order]  # 1-based index

        return G_full, T_tree, tree_matrix, vertices_list, None  # Return results
    except nx.NetworkXError as e:
        # If an error occurs during DFS, return the error message
        return None, None, None, None, str(e)



def generate_random_matrix(n):
    """
    Generate a random adjacency matrix for a connected graph.

    This function generates a random adjacency matrix for a connected graph with `n` vertices. 
    It first creates a chain of vertices connected sequentially and then adds some random edges 
    to ensure the graph remains connected.
    """
    matrix = [[0] * n for _ in range(n)]  # Initialize an empty matrix
    vertices = list(range(n))  
    random.shuffle(vertices)  # Shuffle vertices to randomize edge creation
    for i in range(n - 1):
        u, v = vertices[i], vertices[i + 1]  # Connect sequential vertices
        matrix[u][v] = matrix[v][u] = 1  # Set the edge between them

    # Add some random edges to ensure the graph stays connected
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.3 and matrix[i][j] == 0:  # 30% chance to add edge
                matrix[i][j] = matrix[j][i] = 1
    return matrix  # Return the generated matrix


def save_to_json(adj_matrix, start_vertex, tree_matrix, filename="static/dynamic/graphs/dfs_data.json"):
    """
    Save input and output data to a JSON file.

    This function saves the adjacency matrix, the start vertex, and the adjacency matrix of the 
    spanning tree to a JSON file for later use.
    """
    data = {
        "dfs": {
            "adjacency_matrix": adj_matrix,
            "start_vertex": start_vertex,
            "tree_matrix": tree_matrix
        }
    }
    # Create directory if it doesn't exist and save the data
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def save_graph_image(G_full, T_tree, filename="static/dynamic/graphs/spanning_tree_dfs_1.png"):
    """
    Save graph to a PNG file with red edges for the spanning tree.

    This function visualizes the full graph with gray edges and the spanning tree with red edges. 
    It saves the graph image as a PNG file.
    """
    plt.figure(figsize=(6, 6))  # Set the size of the figure

    # Generate node positions for visualization
    pos = nx.spring_layout(G_full, seed=42)

    # Draw the full graph with light gray edges
    nx.draw_networkx_edges(G_full, pos, edge_color='lightgray', width=1)

    # Highlight the spanning tree with red edges
    nx.draw_networkx_edges(T_tree, pos, edgelist=T_tree.edges(), edge_color='red', width=2)

    # Draw nodes with light blue color
    nx.draw_networkx_nodes(G_full, pos, node_color='lightblue', node_size=500)

    # Display labels (shift to 1-based index for readability)
    labels = {node: node + 1 for node in G_full.nodes}
    nx.draw_networkx_labels(G_full, pos, labels=labels, font_size=12, font_weight='bold')

    # Save the image
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.axis('off')  # Hide the axes
    plt.tight_layout()  # Adjust layout for better fitting
    plt.savefig(filename, format='png')  # Save as PNG
    plt.close()  # Close the plot

    return filename  # Return the path to the saved image


def validate_input(vertices, start_vertex, adj_matrix):
    """
    Validate user input.

    This function checks the validity of the number of vertices, the start vertex, 
    and the adjacency matrix. It ensures that the adjacency matrix dimensions match 
    the number of vertices and that matrix elements are valid integers (0 or 1), 
    symmetric, and without self-loops.
    """
    if not isinstance(vertices, int) or not (1 <= vertices <= 8):
        return "Number of vertices must be an integer between 1 and 8"
    if not isinstance(start_vertex, int) or not (1 <= start_vertex <= vertices):
        return "Starting vertex must be an integer between 1 and number of vertices"
    if not adj_matrix or len(adj_matrix) != vertices or any(len(row) != vertices for row in adj_matrix):
        return "Invalid adjacency matrix dimensions"
    
    # Validate matrix elements (must be 0 or 1)
    for i in range(vertices):
        for j in range(vertices):
            if not isinstance(adj_matrix[i][j], int) or adj_matrix[i][j] not in [0, 1]:
                return "Matrix elements must be integers 0 or 1"
            # Check for self-loops (diagonal elements should be 0)
            if i == j and adj_matrix[i][j] == 1:
                return "Self-loops (diagonal elements) are not allowed"
            # Check for symmetry in the adjacency matrix
            if adj_matrix[i][j] != adj_matrix[j][i]:
                return "Adjacency matrix must be symmetric"
    return None  # Return None if all checks pass




def process_dfs_request():
    """
    Process DFS spanning tree request and return data.

    This function processes the request to generate a spanning tree using DFS. It handles 
    user input (either generating a random adjacency matrix or receiving one from the form), 
    validates the input, creates the spanning tree, and saves the results (graph image, 
    adjacency matrices) to files. It also logs the algorithm's execution.

    Returns:
        dict: A dictionary containing:
            - 'vertices': The number of vertices in the graph.
            - 'adj_matrix': The adjacency matrix of the graph.
            - 'start_vertex': The starting vertex for DFS.
            - 'graph_path': The path to the saved graph image.
            - 'tree_matrix': The adjacency matrix of the spanning tree.
            - 'vertices_list': A list of vertex labels.
            - 'error': Any error message encountered.
    """

    # Initialize variables to store error message, graph data, and other results
    error = None  
    graph_path = None  
    tree_matrix = None  
    vertices_list = None  
    adj_matrix = None  
    vertices = 3  # Default number of vertices
    start_vertex = 1  # Default starting vertex for DFS

    input_data = {}  # To store the input data for logging

    # Check if it's a POST request (form submission)
    if request.method == 'POST':  
        try:
            # Retrieve the action (whether to build or generate a graph)
            action = request.forms.get('action')

            # Get the number of vertices from the form, default to 3 if not provided
            vertices = request.forms.get('vertices', '3')
            vertices = int(vertices.strip()) if vertices.strip() else 3  # Ensure it's an integer

            # Handle the case where the user wants to generate a random graph
            if action == 'generate':
                adj_matrix = generate_random_matrix(vertices)  # Generate random adjacency matrix
                start_vertex = random.randint(1, vertices)  # Randomly pick a starting vertex
            else:
                # If the user provided a custom adjacency matrix, read it from the form
                adj_matrix = []  
                for i in range(vertices):
                    row = []
                    for j in range(vertices):
                        val = request.forms.get(f'edge_{i+1}_{j+1}', '0').strip()  # Get edge values
                        row.append(int(val) if val else 0)  # Convert values to integers and build the row
                    adj_matrix.append(row)  # Add the row to the adjacency matrix

                # Get the starting vertex from the form, default to 1 if not provided
                start_vertex = request.forms.get('start_vertex', '1').strip()  
                start_vertex = int(start_vertex) if start_vertex else 1

            # Save the input data for logging purposes
            input_data = {
                'num_vertices': vertices,
                'adjacency_matrix': adj_matrix,
                'start_vertex': start_vertex
            }

            # Validate the input data
            error = validate_input(vertices, start_vertex, adj_matrix)

            # If validation passed and the action is to build the spanning tree
            if not error and action == 'build':
                # Attempt to create a spanning tree using DFS
                G, T, tree_matrix, vertices_list, graph_error = create_spanning_tree(adj_matrix, start_vertex)

                if graph_error:
                    error = graph_error  # Set error if there's an issue with tree creation
                elif G and T:
                    # Save the graph image and tree data if the spanning tree was created successfully
                    graph_path = save_graph_image(G, T)
                    save_to_json(adj_matrix, start_vertex, tree_matrix)

        except (ValueError, TypeError) as e:
            # Handle any input errors (invalid values or types)
            error = "Invalid input: Please enter valid numbers"
            input_data = {
                'num_vertices': vertices,
                'adjacency_matrix': adj_matrix,
                'start_vertex': start_vertex
            }

        # Log the algorithm run, including input data and error message
        save_algorithm_record(
            algorithm='dfs',
            input_data=input_data,
            result_matrix=tree_matrix if tree_matrix else None,
            error_message=error
        )

    # If no adjacency matrix is provided, initialize it with zeros
    if not adj_matrix:
        adj_matrix = [[0] * vertices for _ in range(vertices)]

    # Return the response with all relevant data
    return {
        'vertices': vertices,
        'adj_matrix': adj_matrix,
        'start_vertex': start_vertex,
        'graph_path': graph_path,
        'tree_matrix': tree_matrix,
        'vertices_list': vertices_list,
        'error': error
    }
