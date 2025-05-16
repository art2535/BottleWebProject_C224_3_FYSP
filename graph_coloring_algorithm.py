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
    # If degrees are equal, original index is used as a tie-breaker (inherent in sort stability)
    sorted_vertices_indices = [vertex_info[0] for vertex_info in sorted(degrees, key=lambda x: x[1], reverse=True)]

    # Initialize colors: -1 means uncolored, colors are 1-indexed
    vertex_colors = [-1] * num_vertices

    # Color the vertices
    for vertex_idx in sorted_vertices_indices:
        neighbor_colors = set()
        for neighbor_idx in range(num_vertices):
            if adjacency_matrix[vertex_idx][neighbor_idx] == 1 and vertex_colors[neighbor_idx] != -1:
                neighbor_colors.add(vertex_colors[neighbor_idx])

        current_color = 1
        while current_color in neighbor_colors:
            current_color += 1
        vertex_colors[vertex_idx] = current_color

    # Prepare result in a dictionary format (vertex_index: color)
    coloring_result = {i: vertex_colors[i] for i in range(num_vertices)}

    num_colors_used = 0
    if any(c != -1 for c in vertex_colors):  # Check if any vertex was colored
        num_colors_used = max(c for c in vertex_colors if c != -1) if any(c != -1 for c in vertex_colors) else 0

    return coloring_result, num_colors_used, adjacency_matrix


def draw_colored_graph(adjacency_matrix, coloring_result, num_colors_used):
    """
    Draws the graph with colored vertices and saves it as a base64 encoded string.

    Args:
        adjacency_matrix (list of list of int): The adjacency matrix of the graph.
        coloring_result (dict): A dictionary mapping vertex indices to their assigned colors (1-indexed).
        num_colors_used (int): The total number of unique colors used.

    Returns:
        str: Base64 encoded string of the graph image, or None if an error occurs.
    """
    num_vertices = len(adjacency_matrix)
    if num_vertices == 0:
        return None

    G = nx.Graph()
    for i in range(num_vertices):
        G.add_node(i)  # Ensure all nodes are added, even if isolated
        for j in range(i + 1, num_vertices):  # Iterate to avoid duplicate edges and self-loops for Graph
            if adjacency_matrix[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    node_colors_list = []  # This will store the actual color string/tuple for each node

    if num_colors_used > 0:
        # Define a list of visually distinct colors
        # Matplotlib's 'tab10' and 'tab20' provide good default sets of RGB(A) tuples
        if num_colors_used <= 10:
            # cmap(i) returns an RGBA tuple when cmap is from plt.cm.get_cmap('tab10')
            palette_source = plt.cm.get_cmap('tab10')
            # Create a list of actual color values for the number of colors used
            color_palette = [palette_source(i) for i in range(num_colors_used)]
        elif num_colors_used <= 20:
            palette_source = plt.cm.get_cmap('tab20')
            color_palette = [palette_source(i) for i in range(num_colors_used)]
        else:
            # For more than 20 colors, sample from a continuous map like 'viridis'
            # or cycle through 'tab20' colors. Sampling 'viridis':
            palette_source = plt.cm.get_cmap('viridis')
            color_palette = [palette_source(i / (num_colors_used - 1 if num_colors_used > 1 else 1)) for i in
                             range(num_colors_used)]
            # Alternative for many colors: cycle through tab20 if you prefer its distinctiveness
            # palette_source_tab20 = plt.cm.get_cmap('tab20')
            # color_palette = [palette_source_tab20(i % 20) for i in range(num_colors_used)]

        for node_idx in G.nodes():  # Iterate in the order nodes were added or sorted by G.nodes()
            assigned_color_id = coloring_result.get(node_idx)  # 1-indexed color ID from your algorithm

            if assigned_color_id is not None and assigned_color_id > 0:
                # Convert 1-indexed color ID to 0-indexed for palette
                color_list_index = assigned_color_id - 1

                # Ensure the index is within the bounds of your generated palette
                if 0 <= color_list_index < len(color_palette):
                    node_colors_list.append(color_palette[color_list_index])
                else:
                    # Fallback: If color_id is out of palette range (should ideally not happen
                    # if num_colors_used is correctly calculated as max(color_id)).
                    # Cycle through the palette as a robust fallback.
                    node_colors_list.append(color_palette[color_list_index % len(color_palette)])
            else:
                node_colors_list.append('lightgrey')  # Default for uncolored or invalid color_id
    else:  # Handles num_colors_used = 0 (e.g., graph with no edges or no nodes that got colored)
        node_colors_list = ['lightgrey'] * G.number_of_nodes()

    plt.figure(figsize=(7, 7))  # Increased figure size for better clarity
    nx.draw(G, pos, with_labels=True, node_color=node_colors_list,
            node_size=700, font_size=10, font_weight='bold', edge_color='gray', width=1.5)

    plt.title(f"Graph Coloring (Largest First Strategy) - {num_colors_used} colors used", fontsize=14)

    # Save to a BytesIO buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory
    img_buffer.seek(0)  # Rewind the buffer

    # Encode image to base64
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"