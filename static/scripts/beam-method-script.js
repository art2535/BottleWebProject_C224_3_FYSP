// Функция для переключения отображения блока с теорией
function toggleTheory() {
    const content = document.getElementById('theoryContent');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

// Функция для динамического обновления таблиц смежности и весов
function updateMatrixTables(n) {
    const adjacencyTable = document.getElementById('adjacency-table');
    const weightsTable = document.getElementById('weights-table');

    // Очищаем таблицы
    adjacencyTable.innerHTML = '';
    weightsTable.innerHTML = '';

    // Проверяем допустимое значение n (3–7)
    if (n >= 3 && n <= 7) {
        // Создаём шапку (горизонтальная нумерация)
        let headerRowAdj = document.createElement('tr');
        let headerRowWgt = document.createElement('tr');
        headerRowAdj.appendChild(document.createElement('th')); // Пустая угловая ячейка
        headerRowWgt.appendChild(document.createElement('th'));
        for (let j = 0; j < n; j++) {
            let thAdj = document.createElement('th');
            let thWgt = document.createElement('th');
            thAdj.textContent = j + 1;
            thWgt.textContent = j + 1;
            headerRowAdj.appendChild(thAdj);
            headerRowWgt.appendChild(thWgt);
        }
        adjacencyTable.appendChild(headerRowAdj);
        weightsTable.appendChild(headerRowWgt);

        // Создаём строки с вертикальной нумерацией
        for (let i = 0; i < n; i++) {
            let adjRow = document.createElement('tr');
            let weightRow = document.createElement('tr');
            let thAdj = document.createElement('th');
            let thWgt = document.createElement('th');
            thAdj.textContent = i + 1;
            thWgt.textContent = i + 1;
            adjRow.appendChild(thAdj);
            weightRow.appendChild(thWgt);

            for (let j = 0; j < n; j++) {
                // Матрица смежности
                let adjCell = document.createElement('td');
                let adjInput = document.createElement('input');
                adjInput.type = 'number';
                adjInput.name = `adjacency_${i}_${j}`;
                adjInput.min = '0';
                adjInput.max = '1';
                adjInput.required = true;
                adjInput.value = '0';
                adjCell.appendChild(adjInput);
                adjRow.appendChild(adjCell);

                // Матрица весов
                let weightCell = document.createElement('td');
                let weightInput = document.createElement('input');
                weightInput.type = 'number';
                weightInput.name = `weights_${i}_${j}`;
                weightInput.min = '0';
                weightInput.required = true;
                weightInput.value = '0';
                weightCell.appendChild(weightInput);
                weightRow.appendChild(weightCell);
            }
            adjacencyTable.appendChild(adjRow);
            weightsTable.appendChild(weightRow);
        }
    }
}

// Генерация случайных значений для матриц
function generateRandomMatrices() {
    const n = parseInt(document.getElementById('n-vertices').value);
    if (isNaN(n) || n < 3 || n > 7) {
        alert('Please enter a valid number of vertices (from 3 to 7).');
        return;
    }

    updateMatrixTables(n);
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            document.querySelector(`input[name="adjacency_${i}_${j}"]`).value = Math.floor(Math.random() * 2);
            document.querySelector(`input[name="weights_${i}_${j}"]`).value = Math.floor(Math.random() * 10);
        }
    }
}

// Очистка формы и таблиц
function clearFields() {
    document.getElementById('matrix-form').reset();
    updateMatrixTables(0);
}

// Слушатель для обновления таблиц при изменении числа вершин
document.getElementById('n-vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 3 && n <= 7) {
        updateMatrixTables(n);
    } else {
        updateMatrixTables(3); // По умолчанию 3x3
    }
});

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('n-vertices').value) || 3;
    updateMatrixTables(n);
});