# Graph Theory Fundamentals and Vertex Coloring

## Introduction to Graph Theory

Graph theory is a branch of mathematics and computer science that studies **graphs**, which are abstract structures used to model pairwise relations between objects. A graph in this context is made up of **vertices** (also called nodes or points) which are connected by **edges** (also called links or lines).

### Undirected Graphs

An **undirected graph** is a graph in which edges have no orientation. The edge $(u, v)$ is identical to the edge $(v, u)$. This means that the relationship between two vertices connected by an edge is mutual.

**Key Concepts for Undirected Graphs:**

* **Vertices (Nodes)**: The fundamental units of a graph, often representing objects or entities. Denoted as $V$.
* **Edges (Links)**: Connections between pairs of vertices, representing a relationship. Denoted as $E$.
* **Adjacency**: Two vertices are **adjacent** if there is an edge connecting them.
* **Degree of a Vertex**: The number of edges incident to a vertex. For a vertex $v$, it's denoted as $deg(v)$ or $d(v)$.
* **Path**: A sequence of vertices such that from each of its vertices there is an edge to the next vertex in the sequence.
* **Cycle**: A path that starts and ends at the same vertex, and which does not revisit any other vertex.
* **Connected Graph**: A graph where there is a path between every pair of distinct vertices.
* **Subgraph**: A graph whose vertices and edges are subsets of another graph.
* **Matrix Representation**:
    * **Adjacency Matrix**: An $n \times n$ square matrix (where $n$ is the number of vertices) where the entry $A_{ij}$ is 1 if there is an edge between vertex $i$ and vertex $j$, and 0 otherwise. For an undirected graph, this matrix is symmetric ($A_{ij} = A_{ji}$).
    * **Incidence Matrix**: Relates vertices to edges.
    * **Adjacency List**: For each vertex, a list of its adjacent vertices. This is often more efficient for sparse graphs.

---

## Graph Coloring

**Vertex coloring** is a fundamental problem in graph theory. It involves assigning a "color" (usually represented by an integer) to each vertex of a graph such_that no two adjacent vertices share the same color. The primary goal is often to minimize the total number of distinct colors used.

* **Proper Coloring**: A coloring where no two adjacent vertices have the same color.
* **k-Coloring**: A proper coloring that uses at most $k$ colors.
* **Chromatic Number ($\chi(G)$)**: The minimum number of colors needed for a proper vertex coloring of a graph $G$. Finding the chromatic number is an NP-hard problem in general.

### Why is Graph Coloring Important?

Graph coloring has numerous practical applications, including:

* **Scheduling and Timetabling**: Assigning time slots to classes or exams, where vertices are tasks and edges connect conflicting tasks. Colors represent time slots.
* **Register Allocation in Compilers**: Assigning variables to a limited number of CPU registers. Variables that are "live" at the same time are connected by an edge, and colors represent registers.
* **Frequency Assignment**: Assigning frequencies to radio transmitters (e.g., cell towers) such that nearby transmitters do not interfere.
* **Map Coloring**: Coloring regions on a map so that no two adjacent regions have the same color (famously solvable with 4 colors for planar graphs).
* **Resource Allocation**: Assigning resources to processes where conflicting processes (vertices) cannot use the same resource (color).
* **Sudoku Puzzles**: Can be modeled as a graph coloring problem.

---

## Greedy Algorithm for Graph Coloring

Since finding the optimal chromatic number is computationally hard, heuristic algorithms are often used to find a "good enough" coloring. The **greedy algorithm** is one such approach.

**General Idea:**
The greedy algorithm iterates through the vertices of the graph in some predefined order. For each vertex, it assigns the smallest available color that is not currently used by any of its already-colored neighbors.

**The choice of vertex ordering significantly impacts the quality of the coloring (number of colors used).**

### Largest First Strategy (Welsh-Powell Algorithm based)

The **Largest First strategy** (often associated with the Welsh-Powell algorithm) is a common and often effective heuristic for ordering vertices in the greedy coloring algorithm.

**Steps:**

1.  **Calculate Degrees**: For each vertex in the graph $G$, calculate its degree (the number of edges connected to it).
2.  **Sort Vertices**: Create a list of all vertices and sort them in descending order of their degrees. If two vertices have the same degree, their relative order can be arbitrary (e.g., based on their original index).
3.  **Coloring Process**:
    * Initialize all vertices as uncolored.
    * Iterate through the sorted list of vertices. For each vertex `v`:
        * Examine the set of colors already assigned to the neighbors of `v` (i.e., vertices adjacent to `v` that have already been processed and colored).
        * Assign the smallest positive integer color to `v` that is **not** present in the set of its neighbors' colors.
        * The first color is typically 1, then 2, and so on.

**Example Walkthrough (Largest First):**

Consider a graph $G=(V, E)$ with vertices $V=\{A, B, C, D\}$ and edges $E=\{(A,B), (A,C), (B,C), (B,D), (C,D)\}$.

1.  **Degrees**:
    * $deg(A) = 2$ (neighbors: B, C)
    * $deg(B) = 3$ (neighbors: A, C, D)
    * $deg(C) = 3$ (neighbors: A, B, D)
    * $deg(D) = 2$ (neighbors: B, C)

2.  **Sorted Vertices (by degree, then by label for ties)**: B, C, A, D (or C, B, A, D, etc.)
    Let's use the order: B, C, A, D.

3.  **Coloring**:
    * **Vertex B**: No colored neighbors. Assign Color 1. `color(B) = 1`.
    * **Vertex C**: Neighbors of C: {A, B, D}.
        * B is colored (Color 1).
        * Smallest color not used by colored neighbors of C (only B is colored with 1): Color 2.
        * `color(C) = 2`.
    * **Vertex A**: Neighbors of A: {B, C}.
        * B is Color 1.
        * C is Color 2.
        * Colors used by neighbors: {1, 2}. Smallest available color: Color 3.
        * `color(A) = 3`.
    * **Vertex D**: Neighbors of D: {B, C}.
        * B is Color 1.
        * C is Color 2.
        * Colors used by neighbors: {1, 2}. Smallest available color: Color 3.
        * `color(D) = 3`.

**Resulting Colors**: {B:1, C:2, A:3, D:3}. Number of colors used: 3.
The chromatic number for this specific graph ($K_4$ minus an edge) is indeed 3.

---

### Characteristics of Greedy Coloring:

* **Simplicity & Efficiency**: The algorithm is straightforward to implement and computationally efficient (polynomial time, often $O(V+E)$ or $O(V^2)$ depending on graph representation and sorting).
* **Sub-optimality**: It does not guarantee finding the minimum number of colors (the true chromatic number $\chi(G)$). The result can be worse than optimal.
* **Bound**: The number of colors used by the greedy algorithm is at most $\Delta(G) + 1$, where $\Delta(G)$ is the maximum degree of any vertex in the graph. This provides an upper bound on its performance. For some graphs (like complete graphs or odd cycles), it finds the optimal coloring.
* **Order Dependence**: The choice of vertex ordering is crucial. Different orderings can lead to different numbers of colors. The Largest First strategy is just one heuristic; others include Smallest Last, random ordering, etc.

### Further Considerations:

* **NP-Hardness**: Finding the true chromatic number of a graph is an NP-hard problem, meaning no known polynomial-time algorithm exists for all graphs. This is why heuristic algorithms like greedy coloring are valuable.
* **Special Graph Classes**: For certain classes of graphs (e.g., bipartite graphs can be colored with 2 colors, planar graphs with 4 colors), more specific theorems and algorithms apply.

This theoretical background provides context for the practical implementation of the greedy graph coloring algorithm.