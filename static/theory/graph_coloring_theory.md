### Graph Coloring

Graph coloring is a special case of graph labeling; it is an assignment of labels traditionally called "colors" to elements of a graph subject to certain constraints. In its simplest form, it is a way of coloring the vertices of a graph such that no two adjacent vertices share the same color; this is called a **vertex coloring**.

---

### Greedy Algorithm for Graph Coloring

The greedy algorithm is a simple and often effective heuristic for graph coloring. It processes the vertices in a specific order, assigning each vertex the smallest available color not used by its already-colored neighbors.

**Largest First Strategy (Welsh-Powell Algorithm based):**
This is a common variant of the greedy algorithm.
1.  **Calculate Degrees**: Compute the degree of each vertex (number of edges connected to it).
2.  **Sort Vertices**: List the vertices in descending order of their degrees.
3.  **Coloring**:
    * Iterate through the sorted list of vertices.
    * For each vertex, assign it the smallest color that has not been used by any of its already-colored neighbors.
    * If all adjacent vertices are already colored, and all available colors are used by them, a new color is introduced.

---

### How the Algorithm Works (Largest First)

1.  **Initialization**:
    * No vertices are colored initially.
    * Available colors are typically represented by positive integers (1, 2, 3, ...).

2.  **Ordering**:
    * Order the vertices $v_1, v_2, \ldots, v_n$ such that $degree(v_i) \ge degree(v_{i+1})$ for all $i$.

3.  **Color Assignment**:
    * For $i = 1$ to $n$:
        * Consider vertex $v_i$.
        * Look at the colors of the neighbors of $v_i$ that have already been colored (i.e., neighbors $v_j$ where $j < i$).
        * Assign to $v_i$ the smallest integer color $c \ge 1$ such that no already-colored neighbor of $v_i$ has color $c$.

---

### Example

Consider a graph with 5 vertices and the following adjacency list:
* 0: [1, 2, 3] (degree 3)
* 1: [0, 2, 4] (degree 3)
* 2: [0, 1, 3] (degree 3)
* 3: [0, 2, 4] (degree 3)
* 4: [1, 3]    (degree 2)

**Sorted by Degree (example order if degrees are equal, e.g., by index):** 0, 1, 2, 3, 4

1.  **Vertex 0 (degree 3)**: No neighbors colored. Assign Color 1.
    * `colors[0] = 1`
2.  **Vertex 1 (degree 3)**: Neighbor 0 is Color 1. Assign Color 2.
    * `colors[1] = 2`
3.  **Vertex 2 (degree 3)**: Neighbor 0 is Color 1, Neighbor 1 is Color 2. Assign Color 3.
    * `colors[2] = 3`
4.  **Vertex 3 (degree 3)**: Neighbor 0 is Color 1, Neighbor 2 is Color 3. Assign Color 2. (Color 2 is available as it's not used by neighbors 0 or 2).
    * `colors[3] = 2`
5.  **Vertex 4 (degree 2)**: Neighbor 1 is Color 2, Neighbor 3 is Color 2. Assign Color 1.
    * `colors[4] = 1`

**Resulting Colors**:
* Vertex 0: Color 1
* Vertex 1: Color 2
* Vertex 2: Color 3
* Vertex 3: Color 2
* Vertex 4: Color 1
Chromatic number used: 3.

---

### Features and Limitations

* **Simplicity**: The greedy algorithm is easy to understand and implement.
* **Speed**: It is generally fast, especially for sparse graphs.
* **Not Always Optimal**: The greedy algorithm does not always find the minimum number of colors (the chromatic number of the graph). The quality of the coloring can depend heavily on the order in which vertices are colored. The "Largest First" strategy is a heuristic that often provides better results than an arbitrary order but is still not guaranteed to be optimal.
* **Approximation**: The number of colors used by the greedy algorithm is at most $\Delta(G) + 1$, where $\Delta(G)$ is the maximum degree of any vertex in the graph.

---

### Applications

* **Scheduling**: Assigning time slots to tasks such that no two conflicting tasks are scheduled at the same time.
* **Register Allocation**: In compilers, assigning variables to a limited number of CPU registers such that variables needed at the same time are in different registers.
* **Frequency Assignment**: Assigning frequencies to radio stations such that nearby stations do not interfere.
* **Map Coloring**: Coloring regions on a map such that no two adjacent regions have the same color.