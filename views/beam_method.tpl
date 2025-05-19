<!DOCTYPE html>
<html lang="ru">
<!-- Rebase this page on the layout.tpl template, passing title and current year -->
% rebase('layout.tpl', title='Beam Search', year=year)

<head>
    <!-- Basic meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beam Search</title>
    <!-- Link to the CSS styles specific for this algorithm page -->
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>

<body>

<!-- Main card container for theory and practice sections -->
<div class="card-bm">

    <!-- Title for the theory section -->
    <h2 class="h2-bm">Theory on Depth-First Search Algorithm</h2>

    <!-- Theory block -->
    <div class="theory-container">
        <!-- Theory header title -->
        <div class="theory-header">
            <span>Theory: Spanning Tree Construction using Beam Search</span>
        </div>
        <!-- Theory content area (initially hidden) -->
        <div class="theory-content" id="theoryContent" style="display: none;">
            {{! theory_text }} <!-- Inject theory text from the variable -->
        </div>
    </div>

    <!-- Arrow button to toggle theory visibility -->
    <div class="toggle-arrow" onclick="toggleTheory()">&#x25BC;</div>

    <!-- Practical application section -->
    <section class="practical-application">
        <h2 class="h2-bm">Practical Application of the Algorithm</h2>

        <!-- Form to submit input data -->
        <form method="post" id="matrix-form">
            <div class="graph-section">

                <!-- Card for input parameters -->
                <div class="matrix-card">
                    <h3>Input Parameters and Matrices</h3>

                    <!-- Action buttons -->
                    <div class="controls">
                        <button type="submit" class="btn">Build Spanning Tree</button>
                        <button type="button" class="btn" onclick="generateRandomMatrices()">Generate Random Matrices</button>
                        <button type="button" class="btn" onclick="clearFields()">Clear Fields</button>
                    </div>

                    <!-- Input field for number of vertices -->
                    <div class="input-group">
                        <div class="input-item">
                            <label for="n-vertices">Number of Vertices:</label>
                            <input type="number" name="n" id="n-vertices" class="input-field" min="3" max="7" required value="{{ form_data.get('n', '') }}">
                        </div>
                    </div>

                    <!-- Adjacency matrix input table -->
                    <div class="adjacency-matrix">
                        <h3>Adjacency Matrix</h3>
                        <table class="compact-matrix" id="adjacency-table">
                            % if form_data.get('n') and form_data.get('adjacency'):
                                % n = int(form_data.get('n', 0))
                                % for i in range(n):
                                    <tr>
                                        % for j in range(n):
                                            <td>
                                                <input type="number" name="adjacency_{{i}}_{{j}}" value="{{ form_data['adjacency'][i][j] }}" min="0" max="1" required>
                                            </td>
                                        % end
                                    </tr>
                                % end
                            % end
                        </table>
                    </div>

                    <!-- Weight matrix input table -->
                    <div class="adjacency-matrix">
                        <h3>Weight Matrix</h3>
                        <table class="compact-matrix" id="weights-table">
                            % if form_data.get('n') and form_data.get('weights'):
                                % n = int(form_data.get('n', 0))
                                % for i in range(n):
                                    <tr>
                                        % for j in range(n):
                                            <td>
                                                <input type="number" name="weights_{{i}}_{{j}}" value="{{ form_data['weights'][i][j] }}" min="0" required>
                                            </td>
                                        % end
                                    </tr>
                                % end
                            % end
                        </table>
                    </div>
                </div>

                <!-- Card for showing results -->
                <div class="graph-card">
                    <h3>Graph and Result</h3>

                    <!-- Result display if available -->
                    % if result:
                        % if result_is_error:
                            <!-- Display error message if spanning tree was not built -->
                            <p class="error">{{ result }}</p>
                        % else:
                            <!-- Display the resulting spanning tree matrix -->
                            <div class="tree-matrix">
                                <h3>Resulting Tree Matrix</h3>
                                <pre>
% for row in result:
{{ ' '.join([str(x) for x in row]) }}
% end
                                </pre>
                            </div>
                            <!-- Display the image visualization of the resulting tree -->
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

<!-- Include JavaScript to handle buttons and theory toggling -->
<script src="/static/scripts/beam-method-script.js"/>
</body>
</html>