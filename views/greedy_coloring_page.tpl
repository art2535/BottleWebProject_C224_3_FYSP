<!DOCTYPE html>
<html lang="en">
% rebase('layout.tpl', title=title, year=year)
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>

    <div class="card-gr">
        <h2 class="h2-gr">Theory on Greedy Graph Coloring</h2>

        <div class="theory-container">
            <div class="theory-header">
                <span>Theory: Graph Coloring using Greedy Algorithm (Largest First)</span>
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
            <h2 class="h2-gr">Practical Application of the Algorithm</h2>

            % if error_message:
            <p class="error-message">{{ error_message }}</p>
            % end

            <form method="POST" action="/greedy_coloring" id="graphForm">
                <div class="graph-section">
                    <div class="matrix-card">
                        <h3>Adjacency Matrix and Graph Controls</h3>
                        <div class="controls">
                            <button type="submit" class="btn" onclick="return validateAndSubmit();">Color Graph</button>
                            <button type="button" class="btn" onclick="makeSymmetric()">Make Symmetric</button>
                            <button type="button" class="btn" onclick="generateRandomValues()">Random Values</button>
                        </div>

                        <div class="input-group">
                            <div class="input-item">
                                <label for="num_vertices">Number of Vertices (min 1):</label>
                                <input type="number" id="num_vertices" name="num_vertices" class="input-field" value="{{ form_data.get('num_vertices', 3) }}" min="1" onchange="updateAdjacencyMatrixTable()">
                            </div>
                        </div>

                        <div class="adjacency-matrix">
                            <h3>Adjacency Matrix (0 or 1)</h3>
                            <table class="compact-matrix" id="adjacencyMatrixTable">
                                </table>
                        </div>
                         </div>

                    <div class="graph-card">
                        <h3>Graph Visualization</h3>
                        <div class="graph-plot">
                            % if graph_image_base64:
                                <img src="{{ graph_image_base64 }}" alt="Colored Graph">
                            % else:
                                <p>Graph will be displayed here after processing.</p>
                            % end
                        </div>

                        % if coloring_result_table:
                        <div class="vertex-colors-result" id="vertexColorsResult" style="margin-top: 20px;">
                            <h3>Vertex Colors</h3>
                            % if num_colors_used_info:
                                <p><strong>{{ num_colors_used_info }}</strong></p>
                            % end
                            <table class="colors-table">
                                <thead>
                                    <tr>
                                        <th>Vertex</th>
                                        <th>Assigned Color ID</th>
                                        <th>Color Sample</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % for item in coloring_result_table:
                                    <tr>
                                        <td>{{ item['vertex'] }}</td>
                                        <td>{{ item['color_id'] }}</td>
                                        <td>
                                            <div class="color-cell" style="background-color: {{ item['hex_color'] }};"></div>
                                        </td>
                                    </tr>
                                    % end
                                </tbody>
                            </table>
                        </div>
                        % end
                    </div>
                </div>
            </form>
        </section>
    </div>

    <script src="/static/scripts/greedy_coloring_script.js"></script>
</body>
</html>