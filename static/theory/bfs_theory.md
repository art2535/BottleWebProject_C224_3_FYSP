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

Suppose we have a graph with vertices 0, 1, 2, 3, 4 and edges between them. After running BFS, the algorithm can follow the following path:

<pre>
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2, 4],
    4: [3]
}

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

spanning_tree_edges = breadth_first_search(graph, 0)

print("Spanning Tree Edges:", spanning_tree_edges)
</pre>

### Output
<pre>
    Spanning Tree Edges: [(0, 1), (0, 2), (2, 3), (3, 4)]
</pre>

- It starts from vertex 0.
- It visits vertex 1 and vertex 2, marking the edges (0, 1) and (0, 2).
- Then it visits vertex 3 from vertex 2, marking the edge (2, 3).
- Finally, it visits vertex 4 from vertex 3, marking the edge (3, 4).

The edges that form the spanning tree are: (0, 1), (0, 2), (2, 3), and (3, 4). This is the correct result for the breadth-first search starting from vertex 0 in the given graph.

![Result spanning tree](../static/dynamic/images/figure-dfs_1.jpg)

### Algorithm Application

1. **Connected Component Search**:
BFS is used to search for connected components in a graph. If there are several components in the graph, then BFS will help you find all the vertices that can be reached from the initial vertex.

2. **Shortest Path Search**:
BFS helps to find the shortest path in unweighted graphs.

3. **Spanning Trees**:
In network design or route construction tasks, BFS helps to build spanning trees for various graphs.

4. **Maze Search**:
The algorithm is suitable for finding solutions in maze solving and navigating grid-based maps.

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