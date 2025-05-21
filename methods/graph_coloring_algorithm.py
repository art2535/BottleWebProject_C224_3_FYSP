# methods/graph_coloring_algorithm.py

import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def greedy_graph_coloring(adjacency_matrix):
    """
    Performs greedy graph coloring using the largest-degree-first strategy.

    :param adjacency_matrix: list of lists containing 0s and 1s representing the graph
    :return: (coloring_dict, num_colors_used, adjacency_matrix)
    """
    n = len(adjacency_matrix)
    if n == 0:
        # Return empty result if matrix is empty
        return {}, 0, adjacency_matrix

    # Calculate the degree (number of edges) of each vertex
    degrees = {i: sum(adjacency_matrix[i]) for i in range(n)}

    # Sort vertices in descending order based on degree
    # This is the "largest degree first" heuristic
    vertices = sorted(degrees, key=lambda v: degrees[v], reverse=True)

    colors = {}  # Dictionary to store the assigned color for each vertex

    # Assign colors to each vertex one by one
    for v in vertices:
        # Get a set of colors used by the adjacent vertices of v
        used = {
            colors[u]
            for u in range(n)
            if adjacency_matrix[v][u] == 1 and u in colors
        }

        # Find the smallest color ID that is not used by neighbors
        c = 1
        while c in used:
            c += 1

        # Assign the found color to the vertex
        colors[v] = c

    # Determine the highest color ID used (i.e., total number of colors)
    max_color = max(colors.values()) if colors else 0

    # Return coloring dictionary, number of colors used, and original matrix
    return colors, max_color, adjacency_matrix


def draw_colored_graph(adjacency_matrix, coloring_result, num_colors_used):
    """
    Draws the graph with nodes colored based on the coloring result.
    Returns a base64-encoded PNG image suitable for embedding in HTML.

    :param adjacency_matrix: 2D list representing the graph structure
    :param coloring_result: dictionary mapping node index to color ID
    :param num_colors_used: number of distinct colors used
    :return: base64-encoded PNG image as a data URI string
    """
    n = len(adjacency_matrix)
    if n == 0:
        # No graph to draw
        return None

    # Create a new undirected graph using NetworkX
    G = nx.Graph()

    # Add nodes labeled 0 to n-1
    G.add_nodes_from(range(n))

    # Add edges where the adjacency matrix has a 1
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] == 1:
                G.add_edge(i, j)

    # Generate layout positions for all nodes (spring layout gives nice spacing)
    pos = nx.spring_layout(G, seed=42)

    # Create a color palette appropriate for the number of colors used
    palette = []
    if num_colors_used <= 10:
        cmap = plt.cm.get_cmap('tab10')  # Up to 10 distinct colors
        palette = [cmap(i) for i in range(num_colors_used)]
    elif num_colors_used <= 20:
        cmap = plt.cm.get_cmap('tab20')  # Up to 20 colors
        palette = [cmap(i) for i in range(num_colors_used)]
    else:
        cmap = plt.cm.get_cmap('viridis')  # Continuous color map for more than 20
        palette = [cmap(i / (num_colors_used - 1 if num_colors_used > 1 else 1)) for i in range(num_colors_used)]

    # Map each node to its corresponding color
    node_colors = []
    for node in G.nodes():
        cid = coloring_result.get(node, 0)
        # Convert color ID to actual RGBA color from the palette
        if cid > 0 and cid - 1 < len(palette):
            node_colors.append(palette[cid - 1])
        else:
            node_colors.append('lightgrey')  # Default color for uncolored nodes

    # Create a matplotlib figure for the graph
    plt.figure(figsize=(7, 7))
    labels = {i: i + 1 for i in G.nodes()}
    nx.draw(
        G, pos,
        labels=labels,
        node_color=node_colors,
        node_size=700,
        font_size=10,
        font_weight='bold',
        edge_color='gray',
        width=1.5
    )

    # Add a title showing the coloring strategy and color count
    plt.title(f"Graph Coloring (Largest First) – {num_colors_used} colors", fontsize=14)

    # Save the image to a BytesIO buffer in PNG format
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    # Encode image to base64 so it can be used directly in HTML <img>
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"
