import heapq
import os
import networkx as nx
import matplotlib.pyplot as plt

# Function to build a spanning tree using the Beam Search method
# Inputs: number of vertices, adjacency matrix, weight matrix, optional start vertex, beam width
# Returns: result adjacency matrix if successful, otherwise an error message
def beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, start=0, beam_width=2):
    result_matrix = [[0] * n for _ in range(n)]

    edges = []  # List to store all possible edges with their weights
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] and weight_matrix[i][j]:
                edges.append((weight_matrix[i][j], i, j))  # Store as (weight, vertex1, vertex2)

    pq = [(0, [], {start})]  # Priority queue with tuples: (total weight, list of edges, set of visited vertices)

    while pq:
        candidates = []  # Best candidates for expansion at the current level
        for _ in range(min(beam_width, len(pq))):  # Process up to beam_width candidates
            if not pq:
                break
            total_weight, current_edges, current_visited = heapq.heappop(pq)  # Pop the most promising candidate
            candidates.append((total_weight, current_edges, current_visited))

        if not candidates:
            break

        for total_weight, current_edges, current_visited in candidates:
            for weight, u, v in sorted(edges):  # Try all edges sorted by weight
                # Check if the edge connects to a new vertex (to avoid cycles)
                if (u in current_visited and v not in current_visited) or (v in current_visited and u not in current_visited):
                    new_edges = current_edges + [(u, v, weight)]  # Add the edge to the current list
                    new_visited = current_visited.copy()  # Copy visited set
                    new_visited.add(u)
                    new_visited.add(v)
                    new_total_weight = total_weight + weight  # Update total weight

                    # Termination condition: spanning tree must have exactly n-1 edges
                    if len(new_edges) == n - 1:
                        for uu, vv, _ in new_edges:
                            result_matrix[uu][vv] = result_matrix[vv][uu] = 1  # Fill symmetric matrix
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix  # Return the result matrix

                    # Push the new state into the priority queue
                    heapq.heappush(pq, (new_total_weight, new_edges, new_visited))

    # If spanning tree could not be constructed (graph is disconnected)
    draw_graph(None, adjacency_matrix, weight_matrix, n)
    return "The spanning tree is not built: the graph is disconnected."

# Function to visualize the input graph and the resulting spanning tree (if built)
# Inputs: result adjacency matrix (spanning tree), input adjacency matrix, weight matrix, number of vertices
def draw_graph(result_matrix, adjacency_matrix, weight_matrix, n):
    G = nx.Graph()  # Create an empty graph

    for i in range(1, n + 1):
        G.add_node(i)  # Add graph nodes (1-based index for display)

    all_edges = []  # List of all edges in the input graph
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j]:
                all_edges.append((i + 1, j + 1))  # Convert to 1-based index

    tree_edges = []  # Edges included in the spanning tree (if any)
    if result_matrix:
        for i in range(n):
            for j in range(i + 1, n):
                if result_matrix[i][j]:
                    tree_edges.append((i + 1, j + 1))

    pos = nx.spring_layout(G, seed=42)  # Position nodes using force-directed layout
    plt.figure(figsize=(6, 6))

    # Draw all graph edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)

    # Highlight spanning tree edges in red (if available)
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=14)

    # Set title and save the figure to a static path
    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()
    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    plt.savefig(static_path)
    plt.close()