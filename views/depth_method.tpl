<!DOCTYPE html>
<html lang="ru">
<!-- Template string for setting dynamic values like the title and year. -->
% rebase('layout.tpl', title='DFS', year=year)
<head>
    <!-- Set the character encoding to support Russian text -->
    <meta charset="UTF-8">
    
    <!-- Set the viewport meta tag for responsive design on mobile devices -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Title of the page that appears in the browser tab -->
    <title>Depth-First Search Algorithm</title>
    
    <!-- Link to an external CSS stylesheet to style the page -->
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>

    <!-- Container card for the theory section of the Depth-First Search algorithm -->
    <div class="card-dfs">
        <h2 class="h2-dfs">Theory on Depth-First Search Algorithm</h2>
        
        <!-- Container for the theoretical explanation of the DFS algorithm -->
        <div class="theory-container">
            <div class="theory-header">
                <!-- Header for the theory section explaining spanning tree construction using DFS -->
                <span>Theory: Spanning Tree Construction using Depth-First Search</span>
            </div>
            <!-- Content of the theory, initially hidden -->
            <div class="theory-content" id="theoryContent" style="display: none;">
                <!-- Dynamic content for the theory will be inserted here -->
                {{! theory_text }}
            </div>
        </div>

        <!-- Button for toggling the visibility of the theory content -->
        <div class="toggle-arrow" onclick="toggleTheory()">
            <span class="arrow">&#x25BC;</span>
        </div>

        <!-- Section for the practical application of the algorithm -->
        <section class="practical-application">
            <h2 class="h2-dfs">Practical Application of the Algorithm</h2>

            <div class="graph-section">
                <!-- Card for the adjacency matrix and graph controls -->
                <div class="matrix-card">
                    <h3>Adjacency Matrix and Graph Controls</h3>
                    <div class="controls">
                        <!-- Buttons to control the graph-building process -->
                        <button class="btn" onclick="buildGraph()">Build Graph</button>
                        <button class="btn">Generate Adjacency Matrix</button>
                        <button class="btn">Reset Graph</button>
                    </div>
                   
                    <!-- Input group for the number of vertices and the starting vertex -->
                    <div class="input-group">
                        <div class="input-item">
                            <label for="vertices">Number of Vertices:</label>
                            <input type="number" id="vertices" class="input-field">
                        </div>
    
                        <div class="input-item">
                            <label for="start-node">Starting Vertex:</label>
                            <input type="number" id="start-node" class="input-field">
                        </div>
                    </div>

                    <!-- Adjacency matrix section where user can input values -->
                    <div class="adjacency-matrix">
                        <h3>Adjacency Matrix of Vertices</h3>
                        <table class="compact-matrix">
                            <!-- Table for the adjacency matrix, where users can input connections between nodes -->
                            <tr>
                                <td></td>
                                <td>0</td>
                                <td>1</td>
                                <td>2</td>
                            </tr>
                            <tr>
                                <td>0</td>
                                <td><input type="number" name="edge_0_0" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_0_1" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_0_2" min="0" max="1" value="0"></td>
                            </tr>
                            <tr>
                                <td>1</td>
                                <td><input type="number" name="edge_1_0" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_1_1" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_1_2" min="0" max="1" value="0"></td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td><input type="number" name="edge_2_0" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_2_1" min="0" max="1" value="0"></td>
                                <td><input type="number" name="edge_2_2" min="0" max="1" value="0"></td>
                            </tr>
                        </table>
                    </div>
                </div>

                <!-- Card for displaying the graph -->
                <div class="graph-card">
                    <h3>Graph</h3>
                    <div class="graph-plot">
                        <!-- Placeholder text for the graph display area -->
                        <p>Graph will be displayed here after processing.</p>
                    </div>

                    <!-- Matrix for displaying the resulting tree after DFS -->
                    <div class="tree-matrix" id="treeMatrix" style="display: none;">
                        <h3>Matrix of the Resulting Tree</h3>
                        <table class="compact-matrix-ready">
                            <!-- Table for the matrix of the tree created by DFS -->
                            <tr>
                                <td></td>
                                <td>0</td>
                                <td>1</td>
                                <td>2</td>
                            </tr>
                            <tr>
                                <td>0</td>
                                <td>0</td>
                                <td>1</td>
                                <td>0</td>
                            </tr>
                            <tr>
                                <td>1</td>
                                <td>1</td>
                                <td>0</td>
                                <td>1</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>0</td>
                                <td>1</td>
                                <td>0</td>
                            </tr>
                        </table>
                        <!-- Information about which vertices form the spanning tree -->
                        <p><strong>Vertices from which the spanning tree was obtained:</strong> 0, 1, 2</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- External JavaScript file to handle dynamic functionality like building the graph -->
    <script src="/static/scripts/work-elements.js"></script>
</body>
</html>
