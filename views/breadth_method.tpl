<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Our Awesome App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .navbar {
            background-color: #b3cde0;
            padding: 10px;
            text-align: center;
            border-radius: 20px;
            margin: 10px;
        }
        .navbar a {
            color: black;
            text-decoration: none;
            margin: 0 20px;
        }
        .content {
            padding: 20px;
            text-align: center;
        }
        .matrix-input {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 20px;
            margin: 20px auto;
            width: 300px;
            text-align: center;
        }
        .matrix-input textarea {
            width: 100%;
            height: 100px;
            margin-bottom: 10px;
        }
        .matrix-input button {
            margin: 5px;
            padding: 5px 10px;
            background-color: #b3cde0;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        #graphImage {
            max-width: 100%;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="#">Home</a>
        <a href="#">Section 1</a>
        <a href="#">Section 2</a>
        <a href="#">Section 3</a>
        <a href="#">Section 4</a>
    </div>
    <div class="content">
        <h2>Описание теории</h2>
        <p style="text-align: center;">
            Алгоритм поиска в ширину (BFS, Breadth-First Search) — это метод обхода графа, который начинается с заданной вершины и исследует все соседние вершины на текущем уровне, прежде чем перейти к следующему уровню. BFS использует очередь для хранения вершин, которые нужно посетить. Этот алгоритм гарантирует, что вершины обрабатываются в порядке их расстояния от начальной вершины, что делает его полезным для нахождения кратчайших путей в невзвешенных графах. В контексте построения остовного дерева BFS может быть использован для создания минимального остовного дерева в невзвешенном графе, где дерево охватывает все вершины с минимальным количеством рёбер.
        </p>
        <div class="matrix-input">
            <textarea id="matrixInput" placeholder="Введите матрицу смежности (например, 0 1 0\n1 0 1\n0 1 0)">0 1 0
1 0 1
0 1 0</textarea>
            <button onclick="generateGraph()">Создать граф</button>
            <button onclick="randomizeMatrix()">Сгенерировать случайные числа</button>
        </div>
        <img id="graphImage" src="" alt="Graph Visualization">
    </div>

    <script>
        function parseMatrix(input) {
            const rows = input.trim().split('\n').map(row => row.trim().split(/\s+/).map(Number));
            return rows;
        }

        function randomizeMatrix() {
            const size = 3;
            let matrix = [];
            for (let i = 0; i < size; i++) {
                let row = [];
                for (let j = 0; j < size; j++) {
                    row.push(i === j ? 0 : Math.floor(Math.random() * 2));
                }
                matrix.push(row);
            }
            document.getElementById('matrixInput').value = matrix.map(row => row.join(' ')).join('\n');
        }

        async function generateGraph() {
            const matrixInput = document.getElementById('matrixInput').value;
            const matrix = parseMatrix(matrixInput);
            try {
                const response = await fetch('http://localhost:5555/generate_graph', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'matrix=' + encodeURIComponent(matrix.map(row => row.join(' ')).join('\n'))
                });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    document.getElementById('graphImage').src = url + '?t=' + new Date().getTime();
                } else {
                    console.error('Failed to fetch graph:', response.statusText);
                    alert('Ошибка при генерации графа: ' + response.statusText);
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('Ошибка при обращении к серверу: ' + error.message);
            }
        }
    </script>
</body>
</html>