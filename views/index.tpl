% rebase('layout.tpl', title='Home', year=year)

<div class="main-container">
    <div class="description-container description-main">
        <h1 class="description-header">Web Application Description</h1>
        <p class="description-text">
            <strong>GRAFSYS</strong> is a web application that implements basic graph theory algorithms.
            The application allows traversing undirected graphs, constructing spanning trees, and
            performing graph coloring with the minimum number of colors. Users can input a graph via
            an adjacency matrix or a weight matrix and obtain results in the form of new matrices and visualizations.
            <br><br>
            The project was developed for educational purposes to reinforce knowledge in
            <em>"Elements of Graph Theory"</em>.
        </p>
    </div>

    <div class="cards-container">
        <div class="card">
            <h2>BFS</h2>
            <p>Breadth-First Search (BFS) is a graph traversal algorithm that explores all vertices at the current level before moving to the next. Using a queue, BFS is ideal for finding shortest paths in unweighted graphs and constructing minimum spanning trees.</p>
            <a href="/bfs" class="button">To Solution</a>
        </div>

        <div class="card">
            <h2>DFS</h2>
            <p>Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking. Using a stack or recursion, DFS is effective for finding cycles, connected components, and topological sorting.</p>
            <a href="/dfs" class="button">To Solution</a>
        </div>

        <div class="card">
            <h2>Beam Search</h2>
            <p>Beam Search is a heuristic search algorithm used in problems with large solution spaces. It explores a limited number of the best paths at each step, making it effective for tasks such as machine translation or planning.</p>
            <a href="/beam" class="button">To Solution</a>
        </div>

        <div class="card">
            <h2>Greedy Algorithm</h2>
            <p>The Greedy Algorithm is a method for solving problems by making the locally optimal choice at each step. It is simple to implement and effective for tasks such as constructing minimum spanning trees or task scheduling.</p>
            <a href="/greedy_coloring" class="button">To Solution</a>
        </div>
    </div>
</div>