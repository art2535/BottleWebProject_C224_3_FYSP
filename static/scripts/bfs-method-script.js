// Функция для показа/скрытия теоретического блока с изменением стрелки
function toggleTheory() {
    const content = document.getElementById('theoryContent'); // Блок с теорией
    const arrow = document.querySelector('.arrow'); // Элемент стрелки (▲ или ▼)

    // Переключаем отображение: если блок скрыт, показываем его и наоборот
    content.style.display = content.style.display === 'none' ? 'block' : 'none';

    // Изменяем символ стрелки в зависимости от состояния
    arrow.textContent = content.style.display === 'none' ? '▼' : '▲';
}

// Функция для обновления таблицы смежности при изменении количества вершин
function updateMatrixTable(n) {
    const adjacencyTable = document.getElementById('adjacency-table'); // Таблица смежности
    adjacencyTable.innerHTML = ''; // Очищаем текущее содержимое таблицы

    if (n >= 1) {
        // Создаём заголовок таблицы с номерами столбцов (вершин)
        let headerRow = document.createElement('tr');
        headerRow.innerHTML = '<td></td>'; // Пустая ячейка слева
        for (let j = 0; j < n; j++) {
            headerRow.innerHTML += `<td>${j}</td>`; // Номера вершин по горизонтали
        }
        adjacencyTable.appendChild(headerRow); // Добавляем строку в таблицу

        // Создаём строки таблицы с инпутами для ввода ребёр
        for (let i = 0; i < n; i++) {
            let row = document.createElement('tr');
            row.innerHTML = `<td>${i}</td>`; // Номер вершины по вертикали

            for (let j = 0; j < n; j++) {
                let cell = document.createElement('td');
                let input = document.createElement('input');
                input.type = 'number'; // Тип поля — число
                input.name = `edge_${i}_${j}`; // Уникальное имя для каждой пары вершин
                input.min = '0';
                input.max = '1';
                input.value = '0'; // Значение по умолчанию — 0 (нет ребра)
                input.required = true; // Обязательное поле
                cell.appendChild(input); // Добавляем поле в ячейку
                row.appendChild(cell); // Добавляем ячейку в строку
            }

            adjacencyTable.appendChild(row); // Добавляем строку в таблицу
        }
    }
}

// Функция для генерации случайной матрицы смежности
function generateRandomMatrix() {
    const n = parseInt(document.getElementById('num_vertices').value); // Получаем число вершин
    if (isNaN(n) || n < 1) {
        alert('Please enter a valid number of vertices (at least 1).');
        return;
    }

    // Сначала создаём пустую таблицу с нулями
    updateMatrixTable(n);

    // Используем setTimeout, чтобы DOM успел отрисовать инпуты
    setTimeout(() => {
        for (let i = 0; i < n; i++) {
            for (let j = i; j < n; j++) {
                const value = i === j ? 0 : Math.floor(Math.random() * 2); // Генерируем 0 или 1, 0 по диагонали
                document.querySelector(`input[name="edge_${i}_${j}"]`).value = value;
                document.querySelector(`input[name="edge_${j}_${i}"]`).value = value; // Симметрия
            }
        }
    }, 0);
}

// Функция для очистки всех полей формы и сброса на начальное состояние
function clearFields() {
    const form = document.getElementById('graphForm'); // Получаем форму по ID
    form.reset(); // Сброс значений формы до начальных

    const numVerticesInput = document.getElementById('num_vertices');
    numVerticesInput.value = '3'; // Устанавливаем значение по умолчанию (3 вершины)

    updateMatrixTable(3); // Перестраиваем таблицу для 3 вершин
}

// Обработчик изменения значения поля "число вершин"
document.getElementById('num_vertices').addEventListener('input', function () {
    const n = parseInt(this.value); // Получаем введённое число
    if (!isNaN(n) && n >= 1) {
        updateMatrixTable(n); // Обновляем таблицу, если число корректное
    } else {
        updateMatrixTable(0); // Иначе очищаем таблицу
    }
});

// При загрузке страницы инициализируем таблицу с текущим числом вершин (или 3 по умолчанию)
document.addEventListener('DOMContentLoaded', function () {
    const n = parseInt(document.getElementById('num_vertices').value) || 3;
    updateMatrixTable(n);
});
