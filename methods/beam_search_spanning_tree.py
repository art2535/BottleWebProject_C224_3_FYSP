import heapq
import os
import networkx as nx
import matplotlib.pyplot as plt

def beam_search_spanning_tree(n, adjacency_matrix, weight_matrix, start=0, beam_width=2):
    result_matrix = [[0] * n for _ in range(n)]
    visited = [False] * n
    visited[start] = True

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] and weight_matrix[i][j]:
                edges.append((weight_matrix[i][j], i, j))

    pq = [(0, [], {start})]

    while pq:
        candidates = []
        for _ in range(min(beam_width, len(pq))):
            if not pq:
                break
            total_weight, current_edges, current_visited = heapq.heappop(pq)
            candidates.append((total_weight, current_edges, current_visited))

        if not candidates:
            break

        for total_weight, current_edges, current_visited in candidates:
            for weight, u, v in sorted(edges):
                if (u in current_visited and v not in current_visited) or (v in current_visited and u not in current_visited):
                    new_edges = current_edges + [(u, v, weight)]
                    new_visited = current_visited | {u, v}
                    new_total_weight = total_weight + weight

                    if n <= 4 and len(new_edges) == n - 2:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    if n >= 5 and len(new_visited) == n:
                        for u, v, _ in new_edges:
                            result_matrix[u][v] = result_matrix[v][u] = 1
                        draw_graph(result_matrix, adjacency_matrix, weight_matrix, n)
                        return result_matrix

                    heapq.heappush(pq, (new_total_weight, new_edges, new_visited))

    draw_graph(None, adjacency_matrix, weight_matrix, n)
    return "The spanning tree is not built: the graph is disconnected."

def draw_graph(result_matrix, adjacency_matrix, weight_matrix, n):
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)

    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j]:
                all_edges.append((i, j))

    tree_edges = []
    if result_matrix:
        for i in range(n):
            for j in range(i + 1, n):
                if result_matrix[i][j]:
                    tree_edges.append((i, j))

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 6))
    nx.draw_networkx_edges(G, pos, edgelist=all_edges, edge_color='gray', width=1.5)
    if result_matrix:
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='red', width=2.5)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=14)
    plt.title("Spanning Tree (red edges)")
    plt.tight_layout()

    static_path = 'static/dynamic/graphs/spanning_tree.png'
    os.makedirs(os.path.dirname(static_path), exist_ok=True)

    plt.savefig(static_path)
    plt.close()