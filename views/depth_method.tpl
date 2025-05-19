<!DOCTYPE html>
<html lang="ru">
<!-- Rebase layout from template and pass dynamic title and year -->
% rebase('layout.tpl', title='DFS', year=year)
<head>
    <!-- Meta information -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Page title -->
    <title>Depth-First Search Algorithm</title>
    
    <!-- External stylesheet -->
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>

    <!-- DFS Algorithm Container -->
    <div class="card-dfs">
        <h2 class="h2-dfs">Theory on Depth-First Search Algorithm</h2>

        <!-- Theory Section -->
        <div class="theory-container">
            <div class="theory-header">
                <span>Theory: Spanning Tree Construction using Depth-First Search</span>
            </div>
            <div class="theory-content" id="theoryContent" style="display: none;">
                {{! theory_text }}
            </div>
        </div>

        <!-- Toggle Button -->
        <div class="toggle-arrow" onclick="toggleTheory()">
            <span class="arrow">&#x25BC;</span>
        </div>

        <!-- Practical Application Section -->
        <section class="practical-application">
            <h2 class="h2-dfs">Practical Application of the Algorithm</h2>

            <div class="graph-section">
                <!-- Matrix and Controls -->
                <div class="matrix-card">
                    <h3>Adjacency Matrix and Graph Controls</h3>

                    <!-- Graph Form -->
                    <form method="POST" id="dfsForm" class="form-container">
                        <div class="controls">
                            <button class="btn" type="submit" name="action" value="build">Build Graph</button>
                            <button class="btn" type="submit" name="action" value="generate">Generate Adjacency Matrix</button>
                            <button class="btn" type="button" onclick="resetForm()">Reset Graph</button>
                        </div>

                        <!-- Inputs for vertices -->
                        <div class="input-group">
                            <div class="input-item">
                                <label for="vertices">Number of Vertices:</label>
                                <input type="number" id="vertices" name="vertices" class="input-field" 
                                       value="{{vertices}}" min="1" max="8" onchange="updateMatrix()">
                            </div>
                            <div class="input-item">
                                <label for="start_vertex">Starting Vertex:</label>
                                <input type="number" id="start_vertex" name="start_vertex" class="input-field" 
                                       value="{{start_vertex}}" min="1">
                            </div>
                        </div>

                        <!-- Adjacency Matrix Table -->
                        <div class="adjacency-matrix">
                            <h3>Adjacency Matrix of Vertices</h3>
                            <table class="compact-matrix" id="matrixTable">
                                <tr>
                                    <td class="matrix-header"></td>
                                    % for i in range(vertices):
                                        <td class="matrix-header">{{i + 1}}</td>
                                    % end
                                </tr>

                                % for i in range(vertices):
                                    <tr>
                                        <td class="matrix-header">{{i + 1}}</td>
                                        % for j in range(vertices):
                                            <td>
                                                <input type="number" name="edge_{{i + 1}}_{{j + 1}}" 
                                                       min="0" max="1" value="{{adj_matrix[i][j]}}">
                                            </td>
                                        % end
                                    </tr>
                                % end

                            </table>
                        </div>
                    </form>
                </div>

                <!-- Graph Visualization -->
                <div class="graph-card">
                    <h3>Graph</h3>
                    <div class="graph-plot">
                        % if error:
                            <p class="error">{{error}}</p>
                        % elif graph_path:
                            <img src="/{{graph_path}}" alt="Spanning Tree">
                        % else:
                            <p>Graph will be displayed here after processing.</p>
                        % end
                    </div>

                    <!-- Resulting Spanning Tree Matrix -->
                    % if tree_matrix:
                        <div class="tree-matrix">
                            <h3>Matrix of the Resulting Tree</h3>
                            <table class="compact-matrix-ready">
                                <tr>
                                    <td class="matrix-header"></td>
                                    % for i in range(vertices):
                                        <td class="matrix-header">{{i + 1}}</td>
                                    % end
                                </tr>

                                % for i in range(vertices):
                                    <tr>
                                        <td class="matrix-header">{{i + 1}}</td>
                                        % for j in range(vertices):
                                            <td>
                                                <input type="number" name="edge_{{i + 1}}_{{j + 1}}" 
                                                       min="0" max="1" value="{{adj_matrix[i][j]}}">
                                            </td>
                                        % end
                                    </tr>
                                % end

                            </table>
                            <p><strong>Vertices from which the spanning tree was obtained:</strong> 
                               {{', '.join(map(str, vertices_list))}}</p>
                        </div>
                    % end
                </div>
            </div>
        </section>
    </div>

    <!-- External JavaScript for interactivity -->
    <script src="/static/scripts/work-elements.js"></script>
</body>
</html>