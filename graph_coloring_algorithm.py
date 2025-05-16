import networkx as nx
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO


def greedy_graph_coloring(adjacency_matrix):
    num_vertices = len(adjacency_matrix)
    if num_vertices == 0:
        return {}, 0, []

    # Calculate degrees of each vertex
    degrees = []
    for i in range(num_vertices):
        degree = 0
        for j in range(num_vertices):
            if adjacency_matrix[i][j] == 1:
                degree += 1
        degrees.append((i, degree))

    # Sort vertices by degree in descending order
    sorted_vertices = [vertex[0] for vertex in sorted(degrees, key=lambda x: x[1], reverse=True)]

    # Initialize colors: -1 means uncolored
    vertex_colors = [-1] * num_vertices

    # Color the vertices
    for vertex in sorted_vertices:
        neighbor_colors = set()
        for neighbor in range(num_vertices):
            if adjacency_matrix[vertex][neighbor] == 1 and vertex_colors[neighbor] != -1:
                neighbor_colors.add(vertex_colors[neighbor])

        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1
        vertex_colors[vertex] = current_color

    # Prepare result in a dictionary format (vertex_index: color)
    coloring_result = {i: vertex_colors[i] for i in range(num_vertices)}

    num_colors_used = 0
    if vertex_colors:
        num_colors_used = max(vertex_colors) if any(c != -1 for c in vertex_colors) else 0

    return coloring_result, num_colors_used, adjacency_matrix


def draw_colored_graph(adjacency_matrix, coloring_result, num_colors_used):
    num_vertices = len(adjacency_matrix)
    if num_vertices == 0:
        return None

    G = nx.Graph()
    for i in range(num_vertices):
        G.add_node(i)
        for j in range(i + 1, num_vertices):
            if adjacency_matrix[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    # Generate a list of distinct colors
    # Using matplotlib's colormaps to get distinct colors
    if num_colors_used > 0:
        try:
            cmap = plt.cm.get_cmap('viridis', num_colors_used + 1)  # +1 to avoid issues if only 1 color
        except ValueError:  # Fallback if colormap doesn't exist or num_colors_used is problematic
            cmap = plt.cm.get_cmap('tab20', num_colors_used + 1)

        node_colors_mapped = [cmap(
            coloring_result.get(node, 0) - 1 / (num_colors_used if num_colors_used > 0 else 1)) if coloring_result.get(
            node, 0) > 0 else 'grey' for node in G.nodes()]
    else:  # Handle case with no colors (e.g. no nodes or no edges)
        node_colors_mapped = ['grey'] * num_vertices

    plt.figure(figsize=(7, 7))
    nx.draw(G, pos, with_labels=True, node_color=node_colors_mapped,
            node_size=800, font_size=12, font_weight='bold', edge_color='gray')

    plt.title(f"Graph Coloring (Largest First Strategy) - {num_colors_used} colors used")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()
    img_buffer.seek(0)

    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"