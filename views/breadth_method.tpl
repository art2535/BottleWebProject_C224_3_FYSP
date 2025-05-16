<!DOCTYPE html>
<html lang="ru">
% rebase('layout.tpl', title='BFS', year=year)
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Breadth-First Search Algorithm</title>
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>
    <div class="card">
        <h2>Theory on Breadth-First Search Algorithm</h2>
        
        <div class="theory-container">
            <div class="theory-header" onclick="toggleTheory()">
                <span>Theory: Spanning Tree Construction using Breadth-First Search</span>
                <span class="arrow">▼</span>
            </div>
            <div class="theory-content" id="theoryContent" style="display: none;">
                {{! theory_text }}
            </div>
        </div>

        <section class="practical-application">
            <h2>Practical Application of the Algorithm</h2>
            % if error_message:
                <div class="error-message">
                    <p>{{ error_message }}</p>
                </div>
            % end

            <div class="graph-section">
                <div class="matrix-card">
                    <h3>Adjacency Matrix and Graph Controls</h3>
                    <form id="matrix-form" method="POST" action="/bfs">
                        <div class="controls">
                            <button type="submit" class="btn">Build Graph</button>
                            <button type="button" class="btn" onclick="generateRandomMatrix()">Generate Adjacency Matrix</button>
                            <button type="button" class="btn" onclick="clearFields()">Reset Graph</button>
                        </div>
                        
                        <div class="input-group">
                            <div class="input-item">
                                <label for="num_vertices">Number of Vertices:</label>
                                <input type="number" id="num_vertices" name="num_vertices" class="input-field" value="{{ form_data['num_vertices'] }}" min="1" required>
                            </div>
    
                            <div class="input-item">
                                <label for="start_vertex">Starting Vertex:</label>
                                <input type="number" id="start_vertex" name="start_vertex" class="input-field" value="{{ form_data['start_vertex'] }}" min="0" required>
                            </div>
                        </div>

                        <div class="adjacency-matrix">
                            <h3>Adjacency Matrix of Vertices</h3>
                            <table class="compact-matrix" id="adjacency-table">
                                % for i in range(int(form_data['num_vertices'])):
                                    <tr>
                                        <td>{{ i }}</td>
                                        % for j in range(int(form_data['num_vertices'])):
                                            <td>
                                                <input type="number" name="edge_{{ i }}_{{ j }}" min="0" max="1" value="{{ form_data['adjacency_matrix'][i][j] }}" required>
                                            </td>
                                        % end
                                    </tr>
                                % end
                            </table>
                        </div>
                    </form>
                </div>

                <div class="graph-card">
                    <h3>Graph</h3>
                    <div class="graph-plot">
                        <img src="{{ graph_image_path }}" alt="Graph">
                    </div>
                    % if result_matrix:
                        <div class="tree-matrix" id="treeMatrix">
                            <h3>Matrix of the Resulting Tree</h3>
                            <table class="compact-matrix-ready">
                                <tr>
                                    <td></td>
                                    % for i in range(int(form_data['num_vertices'])):
                                        <td>{{ i }}</td>
                                    % end
                                </tr>
                                % for i in range(int(form_data['num_vertices'])):
                                    <tr>
                                        <td>{{ i }}</td>
                                        % for j in range(int(form_data['num_vertices'])):
                                            <td>{{ result_matrix[i][j] }}</td>
                                        % end
                                    </tr>
                                % end
                            </table>
                            <p><strong>Vertices from which the spanning tree was obtained:</strong> {{ ', '.join(map(str, tree_vertices)) }}</p>
                        </div>
                    % end
                </div>
            </div>
        </section>
    </div>

    <script src="/static/scripts/bfs-method-script.js"></script>
</body>
</html>