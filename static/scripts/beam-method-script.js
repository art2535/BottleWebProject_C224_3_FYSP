// Функция для переключения отображения блока с теорией (показать/скрыть)
function toggleTheory() {
    const content = document.getElementById('theoryContent');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

// Функция для динамического обновления таблиц смежности и весов в зависимости от числа вершин
function updateMatrixTables(n) {
    const adjacencyTable = document.getElementById('adjacency-table');
    const weightsTable = document.getElementById('weights-table');

    // Очищаем старые таблицы
    adjacencyTable.innerHTML = '';
    weightsTable.innerHTML = '';

    // Проверяем допустимое значение n (число вершин)
    if (n >= 3 && n <= 6) {
        for (let i = 0; i < n; i++) {
            let adjRow = document.createElement('tr');     // Строка таблицы смежности
            let weightRow = document.createElement('tr');  // Строка таблицы весов

            for (let j = 0; j < n; j++) {
                // Создание ячейки и поля ввода для матрицы смежности
                let adjCell = document.createElement('td');
                let adjInput = document.createElement('input');
                adjInput.type = 'number';
                adjInput.name = `adjacency_${i}_${j}`;
                adjInput.min = '0';
                adjInput.max = '1';
                adjInput.required = true;
                adjCell.appendChild(adjInput);
                adjRow.appendChild(adjCell);

                // Создание ячейки и поля ввода для матрицы весов
                let weightCell = document.createElement('td');
                let weightInput = document.createElement('input');
                weightInput.type = 'number';
                weightInput.name = `weights_${i}_${j}`;
                weightInput.min = '0';
                weightInput.required = true;
                weightCell.appendChild(weightInput);
                weightRow.appendChild(weightCell);
            }

            // Добавляем строки в таблицы
            adjacencyTable.appendChild(adjRow);
            weightsTable.appendChild(weightRow);
        }
    }
}

// Генерация случайных значений для матриц смежности и весов
function generateRandomMatrices() {
    const n = parseInt(document.getElementById('n-vertices').value);

    // Проверка корректности числа вершин
    if (isNaN(n) || n < 3 || n > 6) {
        alert('Please enter a valid number of vertices (at least 3).');
        return;
    }

    // Создание структуры таблиц
    updateMatrixTables(n);

    // Заполнение ячеек случайными значениями: 0 или 1 для смежности, 0–9 для весов
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            document.querySelector(`input[name="adjacency_${i}_${j}"]`).value = Math.floor(Math.random() * 2);
            document.querySelector(`input[name="weights_${i}_${j}"]`).value = Math.floor(Math.random() * 10);
        }
    }
}

// Очистка формы и таблиц
function clearFields() {
    // Сброс всех полей формы
    document.getElementById('matrix-form').reset();
    // Удаление таблиц
    updateMatrixTables(0);
}

// Слушатель событий: при изменении числа вершин обновляем таблицы
document.getElementById('n-vertices').addEventListener('input', function () {
    const n = parseInt(this.value);
    if (!isNaN(n) && n >= 3 && n <= 6) {
        updateMatrixTables(n);
    } else {
        updateMatrixTables(0); // При некорректном значении очищаем таблицы
    }
});

// При загрузке страницы автоматически создаём таблицы, если данные не были восстановлены
document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('n-vertices').value);

    // Проверка: если таблицы не созданы, но значение n есть — создаём их
    const adjInputs = document.querySelectorAll('input[name^="adjacency_"]');
    const weightInputs = document.querySelectorAll('input[name^="weights_"]');

    if ((adjInputs.length === 0 || weightInputs.length === 0) && !isNaN(n) && n >= 3 && n <= 6) {
        updateMatrixTables(n);
    }
});