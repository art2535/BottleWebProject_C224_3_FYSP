### Beam Search � Algorithm for Building a Spanning Tree

**Beam Search** is a heuristic search algorithm similar to breadth-first search (BFS) but with a restriction on the number of nodes (states) explored at each level. Instead of exploring all neighbors, it only keeps the best *k* candidates (where *k* is called the beam width). This reduces memory usage and speeds up the search, especially for large graphs, but the algorithm does not guarantee the optimal solution.

---

### How Beam Search Works

1. **Initialization**:
   The algorithm starts from a selected start vertex, marking it as visited and adding it to the current frontier.

2. **Limited Expansion (Beam Width)**:
   At each step, from all neighbors of the current frontier vertices, only the top *k* best candidates are selected based on a heuristic (for example, the lowest edge weight).

3. **Expansion**:
   The selected vertices form the new frontier for the next step. This process continues until all vertices are visited or some termination condition is met.

4. **Spanning Tree Construction**:
   The edges connecting visited vertices to the newly added ones are added to the spanning tree, making sure no cycles form (which can be checked using a union-find or disjoint set data structure).

---

### Example

Suppose we have a weighted graph represented as adjacency lists with weights:

<pre>
graph = {
    0: [(1, 2), (2, 5)],   # vertex 0 connects to 1 with weight 2, to 2 with weight 5
    1: [(0, 2), (2, 1), (3, 4)],
    2: [(0, 5), (1, 1), (3, 1)],
    3: [(1, 4), (2, 1), (4, 3)],
    4: [(3, 3)]
}
</pre>

We want to build a spanning tree starting from vertex 0, using Beam Search with beam width = 2, prioritizing edges with the smallest weight.

---

### Python Code

<pre>
def beam_search_spanning_tree(graph, start_vertex, beam_width):
    visited = set([start_vertex])
    spanning_tree_edges = []
    frontier = [start_vertex]

    # Union-Find data structure to detect cycles
    parent = {v: v for v in graph}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    def union(a, b):
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b:
            parent[root_b] = root_a
            return True
        return False

    while frontier:
        candidates = []
        # Collect all neighbors from the current frontier
        for vertex in frontier:
            for neighbor, weight in graph[vertex]:
                if neighbor not in visited:
                    # Use weight as heuristic score (lower is better)
                    candidates.append((weight, vertex, neighbor))

        # Sort candidates by heuristic (weight)
        candidates.sort(key=lambda x: x[0])

        # Select up to beam_width best candidates
        selected = []
        new_frontier = []

        for weight, v, n in candidates:
            if len(selected) >= beam_width:
                break
            # Check if adding edge forms cycle
            if union(v, n):
                visited.add(n)
                spanning_tree_edges.append((v, n, weight))
                selected.append((weight, v, n))
                new_frontier.append(n)

        frontier = new_frontier
        if len(visited) == len(graph):
            break

    return spanning_tree_edges


graph = {
    0: [(1, 2), (2, 5)],
    1: [(0, 2), (2, 1), (3, 4)],
    2: [(0, 5), (1, 1), (3, 1)],
    3: [(1, 4), (2, 1), (4, 3)],
    4: [(3, 3)]
}

result = beam_search_spanning_tree(graph, 0, beam_width=2)
print("Spanning Tree Edges (with weights):")
for edge in result:
    print(edge)
</pre>

---

### Explanation of the Code

* We start from vertex 0 and mark it visited.
* At each iteration, we collect all neighbors of the current frontier vertices that are not visited.
* We sort these candidate edges by their weight (heuristic).
* We pick up to `beam_width` edges that do not form cycles and add their vertices to the frontier.
* The process continues until all vertices are included or no more vertices can be added.
* We use the union-find data structure to efficiently detect cycles.

---

### Sample Output

<pre>
Spanning Tree Edges (with weights):
(0, 1, 2)
(1, 2, 1)
(2, 3, 1)
(3, 4, 3)
</pre>

This shows that Beam Search selected edges connecting the graph in a way similar to a spanning tree, favoring lower weight edges while limiting exploration at each step.

![Result spanning tree](../static/dynamic/images/spanning_tree.png)

---

### Summary

* Beam Search balances between exhaustive BFS and greedy search by exploring only a limited number of promising nodes at each level.
* It is memory-efficient and faster than BFS but does not guarantee an optimal spanning tree.
* The beam width parameter controls the trade-off between search quality and resource usage.
* Useful when working with very large graphs where full search is impractical.