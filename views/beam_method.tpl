<!DOCTYPE html>
<html lang="en">
% rebase('layout.tpl', title='Beam Search', year=year)

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beam Search</title>
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>

<body>
<div class="card-bm">
    <!-- Theory Section -->
    <h2 class="h2-bm">Theory on Beam Search Algorithm</h2>
    <div class="theory-container">
        <div class="theory-header">
            <span>Theory: Spanning Tree Construction using Beam Search</span>
        </div>
        <div class="theory-content" id="theoryContent" style="display: none;">
            {{! theory_text }}
        </div>
    </div>
    <div class="toggle-arrow" onclick="toggleTheory()">&#x25BC;</div>

    <!-- Practical Application Section -->
    <section class="practical-application">
        <h2 class="h2-bm">Practical Application of the Algorithm</h2>
        <form method="post" id="matrix-form">
            <div class="graph-section">
                <!-- Input Parameters and Matrices -->
                <div class="matrix-card">
                    <h3>Input Parameters and Matrices</h3>
                    <div class="controls">
                        <button type="submit" class="btn">Build Spanning Tree</button>
                        <button type="button" class="btn" onclick="generateRandomMatrices()">Generate Random Matrices</button>
                        <button type="button" class="btn" onclick="clearFields()">Clear Fields</button>
                    </div>
                    <div class="input-group">
                        <div class="input-item">
                            <label for="n-vertices">Number of Vertices:</label>
                            <input type="number" name="n" id="n-vertices" class="input-field" min="2" max="7" required value="{{ form_data['n'] }}">
                        </div>
                    </div>
                    <div class="adjacency-matrix">
                        <h3>Adjacency Matrix</h3>
                        <table class="compact-matrix" id="adjacency-table">
                            <tr>
                                <td class="matrix-header"></td>
                                % for j in range(int(form_data['n'])):
                                    <td class="matrix-header">{{ j + 1 }}</td>
                                % end
                            </tr>
                            % for i in range(int(form_data['n'])):
                                <tr>
                                    <td class="matrix-header">{{ i + 1 }}</td>
                                    % for j in range(int(form_data['n'])):
                                        <td>
                                            <input type="number" name="adjacency_{{ i }}_{{ j }}" min="0" max="1" value="{{ form_data['adjacency'][i][j] }}" class="matrix-input">
                                        </td>
                                    % end
                                </tr>
                            % end
                        </table>
                    </div>
                    <div class="adjacency-matrix">
                        <h3>Weight Matrix</h3>
                        <table class="compact-matrix" id="weights-table">
                            <tr>
                                <td class="matrix-header"></td>
                                % for j in range(int(form_data['n'])):
                                    <td class="matrix-header">{{ j + 1 }}</td>
                                % end
                            </tr>
                            % for i in range(int(form_data['n'])):
                                <tr>
                                    <td class="matrix-header">{{ i + 1 }}</td>
                                    % for j in range(int(form_data['n'])):
                                        <td>
                                            <input type="number" name="weights_{{ i }}_{{ j }}" min="0" max="100" value="{{ form_data['weights'][i][j] }}" class="matrix-input">
                                        </td>
                                    % end
                                </tr>
                            % end
                        </table>
                    </div>
                </div>
                <!-- Graph and Result -->
                <div class="graph-card">
                    <h3>Graph and Result</h3>
                    % if result:
                        % if result_is_error:
                            <p class="error">{{ result }}</p>
                        % else:
                            <div class="tree-matrix">
                                <h3>Resulting Tree Matrix</h3>
                                <table class="compact-matrix">
                                    <tr>
                                        <td class="matrix-header"></td>
                                        % for j in range(len(result)):
                                            <td class="matrix-header">{{ j + 1 }}</td>
                                        % end
                                    </tr>
                                    % for i, row in enumerate(result):
                                        <tr>
                                            <td class="matrix-header">{{ i + 1 }}</td>
                                            % for val in row:
                                                <td>{{ val }}</td>
                                            % end
                                        </tr>
                                    % end
                                </table>
                            </div>
                            <div class="graph-plot">
                                <h3>Tree Visualization</h3>
                                <img src="/static/dynamic/graphs/spanning_tree.png?{{ year }}" alt="Spanning Tree">
                            </div>
                        % end
                    % else:
                        <p class="placeholder">Enter parameters and click "Build Spanning Tree" to see results.</p>
                    % end
                </div>
            </div>
        </form>
    </section>
</div>
<script src="/static/scripts/beam-method-script.js"></script>
</body>
</html>