<!DOCTYPE html>
<html lang="ru">
% rebase('layout.tpl', title='BFS', year=year)

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Breadth-First Search Algorithm</title>
    <!-- Подключение CSS-стилей -->
    <link rel="stylesheet" href="/static/content/style-algorithm.css">
</head>

<body>

    <!-- Основная карточка для всего содержимого BFS -->
    <div class="card-bfs">

        <!-- Заголовок раздела с теорией -->
        <h2 class="h2-bfs">Theory on Breadth-First Search</h2>

        <!-- Контейнер с теоретической частью -->
        <div class="theory-container">
            <div class="theory-header">
                <span>Theory: Spanning Tree Construction using Breadth-First Search</span>
            </div>

            <!-- Скрываемый блок с содержимым теории -->
            <div class="theory-content" id="theoryContent" style="display: none;">
                % if theory_text:
                    {{! theory_text }}  <!-- Вставка Markdown-текста из файла -->
                % else:
                    <p>Theory content could not be loaded.</p>
                % end
            </div>
        </div>

        <!-- Кнопка-секция для разворачивания/сворачивания теории -->
        <div class="toggle-arrow" onclick="toggleTheory()">
            <span class="arrow">▼</span>
        </div>

        <!-- Раздел с практической частью -->
        <section class="practical-application">
            <h2 class="h2-bfs">Practical Application of the Algorithm</h2>

            <!-- Вывод сообщения об ошибке при наличии -->
            % if error_message:
                <p class="error-message">{{ error_message }}</p>
            % end

            <!-- Форма для отправки данных графа -->
            <form method="POST" action="/bfs" id="graphForm">

                <!-- Секция, содержащая таблицу смежности и визуализацию графа -->
                <div class="graph-section">

                    <!-- Карточка с матрицей смежности и элементами управления -->
                    <div class="matrix-card">
                        <h3>Adjacency Matrix and Graph Controls</h3>

                        <!-- Кнопки управления графом -->
                        <div class="controls">
                            <button type="submit" class="btn">Build Graph</button>
                            <button type="button" class="btn" onclick="generateRandomMatrix()">Generate Random Matrix</button>
                            <button type="button" class="btn" onclick="clearFields()">Reset</button>
                        </div>

                        <!-- Поля для ввода количества вершин и стартовой вершины -->
                        <div class="input-group">
                            <div class="input-item">
                                <label for="num_vertices">Number of Vertices:</label>
                                <input type="number" id="num_vertices" name="num_vertices" class="input-field"
                                    value="{{ form_data.get('num_vertices', 3) }}" min="1" max="8" onchange="updateMatrixTable(this.value)">
                            </div>

                            <div class="input-item">
                                <label for="start_vertex">Starting Vertex:</label>
                                <input type="number" id="start_vertex" name="start_vertex" class="input-field"
                                       value="{{ form_data.get('start_vertex', 1) }}" min="1">
                            </div>
                        </div>

                        <!-- Таблица ввода матрицы смежности -->
                        <div class="adjacency-matrix">
                            <h3>Adjacency Matrix (0 or 1)</h3>
                            <table class="compact-matrix" id="adjacency-table">
                                % if form_data.get('num_vertices') and form_data.get('adjacency_matrix'):
                                    <!-- Заголовок таблицы -->
                                    <tr>
                                        <td class="matrix-header"></td>
                                        % for j in range(int(form_data['num_vertices'])):
                                            <td class="matrix-header">{{ j + 1 }}</td>
                                        % end
                                    </tr>
                                    % for i in range(int(form_data['num_vertices'])):
                                        <tr>
                                            <td>{{ i + 1 }}</td>
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

                    <!-- Карточка для визуализации графа и вывода результата -->
                    <div class="graph-card">
                        <h3>Graph Visualization</h3>
                        <div class="graph-plot">
                            % if graph_image_path:
                                <!-- Изображение построенного графа -->
                                <img src="{{ graph_image_path }}" alt="Graph">
                            % else:
                                <p>Graph will be displayed here after processing.</p>
                            % end
                        </div>

                        <!-- Вывод остовного дерева в виде матрицы -->
                        % if result_matrix:
                        <div class="tree-matrix" id="treeMatrix" style="margin-top: 20px;">
                            <h3>Matrix of the Resulting Tree</h3>
                            <table class="compact-matrix-ready">
                                <tr>
                                    <td class="matrix-header"></td>
                                    % for i in range(int(form_data['num_vertices'])):
                                        <td class="matrix-header">{{ i + 1 }}</td>
                                    % end
                                </tr>
                                % for i in range(int(form_data['num_vertices'])):
                                    <tr>
                                        <td class="matrix-header">{{ i + 1 }}</td>
                                        % for j in range(int(form_data['num_vertices'])):
                                            <td>{{ result_matrix[i][j] }}</td>
                                        % end
                                    </tr>
                                % end
                            </table>
                            <!-- Список вершин, включённых в остовное дерево -->
                            <p><strong>Vertices from which the spanning tree was obtained:</strong> {{ ', '.join(map(str, tree_vertices)) }}</p>
                        </div>
                        % end
                    </div>
                </div>
            </form>
        </section>
    </div>

    <!-- Подключение JS-скрипта -->
    <script src="/static/scripts/bfs-method-script.js"></script>
</body>
</html>