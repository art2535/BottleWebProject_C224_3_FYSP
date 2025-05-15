## Theory: Spanning Tree Construction using Beam Search

### Key Concepts

- **Graph Representation**: The graph is typically represented by an adjacency matrix or adjacency list, where each edge has an associated weight.
- **Beam Search**: This is a heuristic search algorithm that explores the most promising nodes (up to a predefined beam width) at each level of the search tree.
- **Spanning Tree**: A spanning tree of a graph is a tree that connects all the vertices without any cycles and uses the fewest number of edges possible.

---

### Visual Example

<img src="/static/resources/art2535.jpg" alt="Graph Example" align="left" width="300" style="margin-right: 20px; border: 1px solid #444; border-radius: 8px;">

The image shows a weighted undirected graph with 6 vertices. Our goal is to construct a spanning tree using the **Beam Search** algorithm.

Beam Search starts from an arbitrary node (e.g., A), evaluates neighboring nodes based on edge weights, and selects the most promising paths. It avoids cycles and prunes less optimal branches based on a fixed **beam width**.

This makes the algorithm faster than exhaustive search, though it may not always yield the optimal solution.

---

### Algorithm Steps

1. **Step 1**: Initialize the beam with a starting node.
2. **Step 2**: For each node in the beam, explore all possible next nodes.
3. **Step 3**: Keep only the most promising nodes (based on weight) within the beam width.
4. **Step 4**: Repeat until a full spanning tree is formed.

---

### Advantages

- Faster than exhaustive search due to pruning.
- Adaptable to different types of graph search problems.

### Disadvantages

- Might miss the optimal solution.
- Heavily depends on beam width and heuristic.

---

### Example: Adjacency and Weight Matrices

Given `n = 4` vertices:

#### Adjacency Matrix