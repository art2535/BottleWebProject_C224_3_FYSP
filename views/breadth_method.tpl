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

    <div class="card-bfs">
        <h2 class="h2-bfs">Theory on Breadth-First Search</h2>

        <div class="theory-container">
            <div class="theory-header">
                <span>Theory: Spanning Tree Construction using Breadth-First Search</span>
            </div>
            <div class="theory-content" id="theoryContent" style="display: none;">
                % if theory_text:
                    {{! theory_text }}
                % else:
                    <p>Theory content could not be loaded.</p>
                % end
            </div>
        </div>

        <div class="toggle-arrow" onclick="toggleTheory()">
            <span class="arrow">&#x25BC;</span>
        </div>

        <section class="practical-application">
            <h2 class="h2-bfs">Practical Application of the Algorithm</h2>

            % if error_message:
                <p class="error-message">{{ error_message }}</p>
            % end

            <form method="POST" action="/bfs" id="graphForm">
                <div class="graph-section">
                    <div class="matrix-card">
                        <h3>Adjacency Matrix and Graph Controls</h3>

                        <div class="controls">
                            <button type="submit" class="btn">Build Graph</button>
                            <button type="button" class="btn" onclick="generateRandomMatrix()">Generate Random Matrix</button>
                            <button type="button" class="btn" onclick="clearFields()">Reset</button>
                        </div>

                        <div class="input-group">
                            <div class="input-item">
                                <label for="num_vertices">Number of Vertices:</label>
                                <input type="number" id="num_vertices" name="num_vertices" class="input-field"
                                       value="{{ form_data.get('num_vertices', 3) }}" min="1" onchange="updateAdjacencyMatrixTable()">
                            </div>

                            <div class="input-item">
                                <label for="start_vertex">Starting Vertex:</label>
                                <input type="number" id="start_vertex" name="start_vertex" class="input-field"
                                       value="{{ form_data.get('start_vertex', 0) }}" min="0">
                            </div>
                        </div>

                        <div class="adjacency-matrix">
                            <h3>Adjacency Matrix (0 or 1)</h3>
                            <table class="compact-matrix" id="adjacency-table">
                                % if form_data.get('num_vertices') and form_data.get('adjacency_matrix'):
                                    % for i in range(int(form_data['num_vertices'])):
                                        <tr>
                                            % for j in range(int(form_data['num_vertices'])):
                                                <td>
                                                    <input type="number" name="edge_{{ i }}_{{ j }}"
                                                           min="0" max="1"
                                                           value="{{ form_data['adjacency_matrix'][i][j] }}" required>
                                                </td>
                                            % end
                                        </tr>
                                    % end
                                % end
                            </table>
                        </div>
                    </div>

                    <div class="graph-card">
                        <h3>Graph Visualization</h3>
                        <div class="graph-plot">
                            % if graph_image_path:
                                <img src="{{ graph_image_path }}" alt="Graph">
                            % else:
                                <p>Graph will be displayed here after processing.</p>
                            % end
                        </div>

                        % if result_matrix:
                        <div class="tree-matrix" id="treeMatrix" style="margin-top: 20px;">
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
            </form>
        </section>
    </div>

    <script src="/static/scripts/bfs-method-script.js"></script>
</body>
</html>
