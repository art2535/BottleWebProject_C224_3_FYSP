### Depth-first search (DFS) is an algorithm for building a spanning tree

**Depth-First Search** (or **Depth-First Search**, DFS) is one of the basic graph search algorithms that is used to traverse or search the depth of a graph. This algorithm explores the vertices of a graph, starting from some vertex and following the path until it reaches a vertex with untouched neighbors. After that, the algorithm returns to the last vertex with unvisited neighbors and continues the search. This allows DFS to build a **spanning tree** (or **spanning tree**) for connected graphs.

### How the algorithm works

1. **Initialization**:
The algorithm starts by selecting the initial vertex and marks it as visited.
   
2. **Recursive traversal**:
From the current vertex, the algorithm moves to one of the unvisited adjacent vertices and repeats the process until the end of the branch is reached (or there are no unvisited neighbors).
   
3. **Return and continuation**:
   If the current vertex has no unvisited neighbors, the algorithm returns to the previous vertex and repeats the process for the remaining unvisited vertices.

4. **Ending**:
   The process continues until all vertices of the graph are visited (for a connected graph).

### Features and Benefits of DFS

- **Deep approach**: The algorithm delves into the graph until it is possible to go further, which makes it useful for finding paths or connected components.
- **Stack Usage**: The DFS implementation uses the **stack** data structure, which stores the vertices to be visited. In the recursive version of the stack, the system stack plays the role.
  
### A depth-first search algorithm for building a spanning tree

When performing a depth-first search in a connected graph, you can build a **spanning tree**. This tree consists of vertices and edges that connect all vertices without forming cycles. A spanning tree can be useful, for example, for finding shortest paths or building routes.

To build a spanning tree using DFS, follow these steps:

1. **Choosing the starting vertex**:
   To begin with, an arbitrary vertex of the graph is selected.

2. **The crawl process**:
   During the traversal, the algorithm will mark the edges that pass through during the study. These edges will form a spanning tree.

3. **Ending**:
   After all the vertices are visited and the spanning tree is built, the algorithm shuts down.

### Example Code

Suppose we have a graph with vertices 0, 1, 2, 3, 4 and edges between them. After running DFS, the algorithm can follow the following path:

<pre>
	graph = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1, 3],
        3: [2, 4],
        4: [3]
    }

    def dfs(graph, vertex, visited, parent, spanning_tree_edges):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                spanning_tree_edges.append((vertex, neighbor))
                dfs(graph, neighbor, visited, vertex, spanning_tree_edges)

    def depth_first_search(graph, start_vertex):
        visited = set()
        spanning_tree_edges = []
        dfs(graph, start_vertex, visited, None, spanning_tree_edges)
        return spanning_tree_edges

    spanning_tree_edges = depth_first_search(graph, 0)

    print("Spanning Tree Edges:", spanning_tree_edges)
</pre>

### Output
<pre>
    Spanning Tree Edges: [(0, 1), (0, 2), (2, 3), (3, 4)]
</pre>

- It starts from vertex 0.
- It moves to vertex 1, marking the edge (0, 1).
- Then, it moves to vertex 2 (from vertex 1), marking the edge (1, 2).
- It continues to vertex 3, marking the edge (2, 3).
- Finally, it moves to vertex 4, marking the edge (3, 4).

The edges that form the spanning tree are: ```(0, 1), (1, 2), (2, 3), and (3, 4)```. This is the correct result for the depth-first search starting from vertex 0 in the given graph.

### Visualization
![Result spanning tree](../static/dynamic/images/figure-dfs_1.jpg)

### Algorithm Application

1. **Connected Component Search**:
DFS is used to search for connected components in a graph. If there are several components in the graph, then DFS will help you find all the vertices that can be reached from the initial vertex.

2. **Topological Sorting**:
DFS helps to perform topological sorting in directed acyclic graphs (DAGs).

3. **Spanning Trees**:
In weight minimization or route construction tasks, DFS helps to build spanning trees for various graphs.

4. **Maze Search**:
The algorithm is suitable for finding solutions in maze solving and playing with grid maps.

### Advantages and disadvantages

**Advantages**:
- Ease of implementation.
- Can be used for different types of graphs (oriented and undirected).
- Works well with tasks where you need to go through all the vertices.

**Disadvantages**:
- The algorithm can get "stuck" in a deep part of the graph if it is not possible to find a path to other parts of the graph.
- For graphs with a large number of vertices and edges, DFS may be less efficient compared to other algorithms.

### Conclusion

The depth-first search algorithm is an important tool for working with graphs. Its use in building a spanning tree helps to efficiently traverse graphs and search for connections between vertices. Despite its drawbacks, the algorithm remains a powerful tool for many applications.