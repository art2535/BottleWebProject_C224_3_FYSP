<!DOCTYPE html>
<html lang="ru">
% rebase('layout.tpl', title='DFS', year=year)
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Depth-First Search Algorithm</title>
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>

    <div class="card">
        <h2>Theory on Depth-First Search Algorithm</h2>
        
        <div class="theory-container">
            <div class="theory-header">
                <span>Theory: Spanning Tree Construction using Depth-First Search</span>
            </div>
            <div class="theory-content" id="theoryContent" style="display: none;">
                {{! theory_text }}
            </div>
        </div>

        <div class="toggle-arrow" onclick="toggleTheory()">
            <span class="arrow">&#x25BC;</span>
        </div>

        <section class="practical-application">
            <h2>Practical Application of the Algorithm</h2>

            <div class="graph-section">
                <div class="matrix-card">
                    <h3>Adjacency Matrix and Graph Controls</h3>
                    <div class="controls">
                        <button class="btn" onclick="buildGraph()">Build Graph</button>
                        <button class="btn">Generate Adjacency Matrix</button>
                        <button class="btn">Reset Graph</button>
                    </div>
                   
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

                    <div class="adjacency-matrix">
                        <h3>Adjacency Matrix of Vertices</h3>
                        <table class="compact-matrix">
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

                <div class="graph-card">
                    <h3>Graph</h3>
                    <div class="graph-plot">
                        <img src="/static/avatar.jpg" alt="Graph">
                    </div>
                    <div class="tree-matrix" id="treeMatrix" style="display: none;">
                        <h3>Matrix of the Resulting Tree</h3>
                        <table class="compact-matrix-ready">
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
                        <p><strong>Vertices from which the spanning tree was obtained:</strong> 0, 1, 2</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <script src="/static/scripts/work-elements.js"></script>
</body>
</html>

