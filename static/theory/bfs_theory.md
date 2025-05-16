
### Breadth-first search (BFS) is an algorithm for building a spanning tree

**Breadth-First Search** (or **BFS**) is one of the basic graph search algorithms that is used to traverse or search the breadth of a graph. This algorithm explores the vertices of a graph, starting from some vertex and visiting all its neighbors before moving on to the neighbors' neighbors. This layered approach allows BFS to build a **spanning tree** for connected graphs.

### How the algorithm works

1. **Initialization**:  
   The algorithm starts by selecting the initial vertex, marking it as visited, and adding it to a queue.

2. **Level-order traversal**:  
   From the current vertex, the algorithm visits all unvisited adjacent vertices, adds them to the queue, and repeats the process for the next vertex in the queue.

3. **Continuation**:  
   The process continues until there are no more vertices in the queue.

4. **Ending**:  
   The algorithm stops when all vertices of the graph are visited (for a connected graph).

<p align="center">
  <img src="../static/dynamic/images/bfs_algorithm.gif" alt="How algorithm works">
</p>

### Features and Benefits of BFS

- **Layered approach**: The algorithm explores the graph level by level, which is useful for finding the shortest path in unweighted graphs.  
- **Queue Usage**: The BFS implementation uses the **queue** data structure, which stores the vertices to be visited in FIFO order.  
- **Memory**: In the worst case, the algorithm takes **O(V)** memory, where V is the number of vertices in the graph.

### A breadth-first search algorithm for building a spanning tree

When performing a breadth-first search in a connected graph, you can build a **spanning tree**. This tree consists of vertices and edges that connect all vertices without forming cycles. A spanning tree can be useful, for example, for finding shortest paths or building routes.

To build a spanning tree using BFS, follow these steps:

1. **Choosing the starting vertex**:  
   To begin with, an arbitrary vertex of the graph is selected.

2. **The traversal process**:  
   During the traversal, the algorithm will mark the edges that are used to discover new vertices. These edges will form a spanning tree.

3. **Ending**:  
   After all the vertices are visited and the spanning tree is built, the algorithm shuts down.

### Example

Suppose we have a graph with vertices 0, 1, 2, 3, 4, 5 and edges between them:

<pre>
graph = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1],
    3: [0, 5],
    4: [1, 5],
    5: [3, 4]
}
</pre>

### BFS Implementation

<pre>
from collections import deque

def breadth_first_search(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])
    visited.add(start_vertex)
    spanning_tree_edges = []

    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                spanning_tree_edges.append((vertex, neighbor))
    return spanning_tree_edges

graph = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1],
    3: [0, 5],
    4: [1, 5],
    5: [3, 4]
}

spanning_tree_edges = breadth_first_search(graph, 0)

print("Spanning Tree Edges:", spanning_tree_edges)
</pre>

### Output

<pre>
Spanning Tree Edges: [(0, 1), (0, 3), (1, 2), (1, 4), (3, 5)]
</pre>

### Explanation

- Start from vertex 0.  
- Visit vertices 1 and 3: edges (0, 1), (0, 3).  
- Visit vertices 2 and 4 from vertex 1: edges (1, 2), (1, 4).  
- Visit vertex 5 from vertex 3: edge (3, 5).

The edges that form the spanning tree are: **(0, 1), (0, 3), (1, 2), (1, 4), (3, 5)**

The graph contains **6 vertices and 5 edges**, which is correct for a spanning tree.

### Visualization
<p align="center">
    <img src="../static/dynamic/images/bfs_tree_theory.png" alt="Spanning tree result">
</p>

### Algorithm Application

1. **Connected Component Search**:  
   BFS is used to search for connected components in a graph.

2. **Shortest Path Search**:  
   BFS helps to find the shortest path in unweighted graphs.

3. **Spanning Trees**:  
   In network design or route construction tasks, BFS helps to build spanning trees.

4. **Maze Search**:  
   BFS is suitable for finding solutions in maze solving and navigating grid-based maps.

### Advantages and disadvantages

**Advantages**:  
- Simple and easy to implement.  
- Finds the shortest path in unweighted graphs.  
- Works well with tasks where level-by-level traversal is needed.

**Disadvantages**:  
- Can require a lot of memory for wide graphs.  
- Not suitable for deep traversals compared to DFS.

### Conclusion

The breadth-first search algorithm is an essential tool for working with graphs. Its use in building a spanning tree helps to efficiently traverse graphs and discover connections between vertices. Despite some limitations, the algorithm is widely used in various practical applications.