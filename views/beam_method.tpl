<!DOCTYPE html>
<html lang="ru">
% rebase('layout.tpl', title='Beam Search', year=year)
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beam Search</title>
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>
<body>

<div class="card">
    <header>
        <h1>Theory on Beam Search Algorithm</h1>
    </header>

    <div class="theory-container">
        <div class="theory-header">
            <span>Theory: Spanning Tree Construction using Beam Search</span>
        </div>
        <div class="theory-content" id="theoryContent" style="display: none;">
            {{! theory_text }}
        </div>
    </div>

    <div class="toggle-arrow" onclick="toggleTheory()">&#x25BC;</div>

    <section class="practical-application">
        <h2>Practical Application of the Algorithm</h2>

        <form method="post" id="matrix-form">
            <div class="graph-section">
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
                            <input type="number" name="n" id="n-vertices" class="input-field" min="3" required value="{{ form_data.get('n', '') }}">
                        </div>
                    </div>

                    <div class="adjacency-matrix">
                        <h3>Adjacency Matrix</h3>
                        <table class="compact-matrix" id="adjacency-table">
                            % if form_data.get('n') and form_data.get('adjacency'):
                                % n = int(form_data.get('n', 0))
                                % for i in range(n):
                                    <tr>
                                        % for j in range(n):
                                            <td><input type="number" name="adjacency_{{i}}_{{j}}" value="{{ form_data['adjacency'][i][j] }}" min="0" max="1" required></td>
                                        % end
                                    </tr>
                                % end
                            % end
                        </table>
                    </div>

                    <div class="adjacency-matrix">
                        <h3>Weight Matrix</h3>
                        <table class="compact-matrix" id="weights-table">
                            % if form_data.get('n') and form_data.get('weights'):
                                % n = int(form_data.get('n', 0))
                                % for i in range(n):
                                    <tr>
                                        % for j in range(n):
                                            <td><input type="number" name="weights_{{i}}_{{j}}" value="{{ form_data['weights'][i][j] }}" min="0" required></td>
                                        % end
                                    </tr>
                                % end
                            % end
                        </table>
                    </div>
                </div>

                <div class="graph-card">
                    <h3>Graph and Result</h3>

                    % if result:
                        % if result_is_error:
                            <p class="error">{{ result }}</p>
                        % else:
                            <div class="tree-matrix">
                                <h3>Resulting Tree Matrix</h3>
                                <pre>
% for row in result:
{{ ' '.join([str(x) for x in row]) }}
% end
                                </pre>
                            </div>
                            <div class="graph-plot">
                                <h3>Tree Visualization</h3>
                                <img src="/static/dynamic/graphs/spanning_tree.png?{{ year }}" alt="Spanning Tree">
                            </div>
                        % end
                    % end
                </div>
            </div>
        </form>
    </section>
</div>

<script src="/static/scripts/beam-method-script.js"/>

</body>
</html>