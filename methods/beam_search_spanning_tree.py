import heapq  # Module for working with priority queues (heaps)
import os
import networkx as nx  # Library for working with graphs
import matplotlib.pyplot as plt  # Library for visualizing graphs

# Function to build a spanning tree using the Beam Search method
# Inputs: number of vertices, adjacency matrix, weight matrix
# Returns: result adjacency matrix if successful, otherwise an error message
def beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, start=0, beam_width=2):
    result_matrix = [[0] * n for _ in range(n)]  # Result matrix (spanning tree)
    visited = [False] * n  # Array to track visited vertices
    visited[start] = True  # Mark the starting vertex as visited

    edges = []  # List of all edges with weights
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] and weight_matrix[i][j]:
                edges.append((weight_matrix[i][j], i, j))  # Add edge (weight, vertex1, vertex2)

    pq = [(0, [], {start})]  # Priority queue of states: (total weight, edges, visited vertices)

    while pq:
        candidates = []  # Best candidates at the current level
        for _ in range(min(beam_width, len(pq))):  # Limit the beam width
            if not pq:
                break
            total_weight, current_edges, current_visited = heapq.heappop(pq)  # Get the lightest path
            candidates.append((total_weight, current_edges, current_visited))

        if not candidates:
            break

        for total_weight, current_edges, current_visited in candidates:
            for weight, u, v in sorted(edges):  # Iterate edges in ascending order of weight
                # Check if the edge can be added without creating a cycle
                if (u in current_visited and v not in current_visited) or (v in current_visited and u not in current_visited):
                    new_edges = current_edges + [(u, v, weight)]  # Update edge list
                    new_visited = current_visited | {u, v}  # Update visited set
                    new_total_weight = total_weight + weight  # Update total weight

                    # Termination condition for small graphs (n <= 4)
                    if n <= 4 and len(new_edges) == n - 2:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    # Termination condition for graphs with >= 5 vertices
                    if n >= 5 and len(new_visited) == n:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    # Add new state to the priority queue
                    heapq.heappush(pq, (new_total_weight, new_edges, new_visited))

    # If spanning tree was not built (graph is disconnected)
    draw_graph(None, adjacency_matrix, weight_matrix, n)
    return "The spanning tree is not built: the graph is disconnected."

# Function to visualize the graph and the spanning tree
# Inputs: result adjacency matrix, input adjacency matrix, weight matrix, number of vertices
# Output: saves an image of the graph
def draw_graph(result_matrix, adjacency_matrix, weight_matrix, n):
    G = nx.Graph()  # Create an empty graph

    for i in range(1, n + 1):
        G.add_node(i)  # Add nodes (1-based index)

    all_edges = []  # All edges from the adjacency matrix
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j]:
                all_edges.append((i + 1, j + 1))  # Shift index for display

    tree_edges = []  # Edges of the spanning tree (if available)
    if result_matrix:
        for i in range(n):
            for j in range(i + 1, n):
                if result_matrix[i][j]:
                    tree_edges.append((i + 1, j + 1))

    pos = nx.spring_layout(G, seed=42)  # Layout for positioning nodes
    plt.figure(figsize=(6, 6))

    # Draw all edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)

    # Draw tree edges in red
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=14)

    # Settings and save image
    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()
    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    plt.savefig(static_path)
    plt.close()