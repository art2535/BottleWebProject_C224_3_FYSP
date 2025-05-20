// Функция для показа/скрытия теоретического блока с изменением стрелки
function toggleTheory() {
    const content = document.getElementById('theoryContent');
    const arrow = document.querySelector('.toggle-arrow .arrow');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
    arrow.textContent = content.style.display === 'none' ? '▼' : '▲';
}

// Функция для обновления таблицы смежности при изменении количества вершин
function updateMatrixTable(n) {
    const adjacencyTable = document.getElementById('adjacency-table');
    adjacencyTable.innerHTML = '';
    if (n > 8) n = 8;

    if (n >= 2) {
        // Создаём заголовок таблицы с номерами столбцов (1-based)
        let headerRow = document.createElement('tr');
        headerRow.innerHTML = '<td class="matrix-header"></td>';
        for (let j = 0; j < n; j++) {
            headerRow.innerHTML += `<td class="matrix-header">${j + 1}</td>`;
        }
        adjacencyTable.appendChild(headerRow);

        // Создаём строки таблицы с инпутами для ввода рёбер (1-based для отображения)
        for (let i = 0; i < n; i++) {
            let row = document.createElement('tr');
            row.innerHTML = `<td class="matrix-header">${i + 1}</td>`;
            for (let j = 0; j < n; j++) {
                let cell = document.createElement('td');
                let input = document.createElement('input');
                input.type = 'number';
                input.name = `edge_${i}_${j}`; // 0-based для backend
                input.min = '0';
                input.max = '1';
                input.value = '0';
                input.required = true;
                cell.appendChild(input);
                row.appendChild(cell);
            }
            adjacencyTable.appendChild(row);
        }

        // Обновляем стартовую вершину: устанавливаем 1, если выходит за пределы или меньше 1
        const startVertexInput = document.getElementById('start_vertex');
        if (isNaN(parseInt(startVertexInput.value)) || parseInt(startVertexInput.value) < 1 || parseInt(startVertexInput.value) > n) {
            startVertexInput.value = '1';
        }
    }
}

// Функция для генерации случайной матрицы смежности
function generateRandomMatrix() {
    const n = parseInt(document.getElementById('num_vertices').value);
    if (isNaN(n) || n < 2 || n > 8) {
        alert('Please enter a valid number of vertices (2 to 8).');
        return;
    }

    updateMatrixTable(n);

    // Используем setTimeout, чтобы DOM успел отрисовать инпуты
    setTimeout(() => {
        for (let i = 0; i < n; i++) {
            for (let j = i; j < n; j++) {
                const value = i === j ? 0 : Math.floor(Math.random() * 2);
                document.querySelector(`input[name="edge_${i}_${j}"]`).value = value;
                document.querySelector(`input[name="edge_${j}_${i}"]`).value = value;
            }
        }
    }, 0);
}

// Функция для очистки всех полей формы и сброса на начальное состояние
function clearFields() {
    const form = document.getElementById('graphForm');
    form.reset();

    // Сброс значений полей
    const numVerticesInput = document.getElementById('num_vertices');
    const startVertexInput = document.getElementById('start_vertex');
    numVerticesInput.value = '2';
    startVertexInput.value = '1';

    // Обновление таблицы смежности
    updateMatrixTable(2);

    // Очистка визуализации графа
    const graphPlot = document.querySelector('.graph-plot');
    if (graphPlot) {
        graphPlot.innerHTML = '<p>Graph will be displayed here after processing.</p>';
    }

    // Очистка результата остовного дерева
    const treeMatrix = document.getElementById('treeMatrix');
    if (treeMatrix) {
        treeMatrix.remove();
    }
}

// Обработчик изменения значения поля "число вершин"
document.getElementById('num_vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 2 && n <= 8) {
        updateMatrixTable(n);
    } else {
        updateMatrixTable(2);
    }
});

// При загрузке страницы инициализируем таблицу
document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('num_vertices').value) || 2;
    updateMatrixTable(n);
});
