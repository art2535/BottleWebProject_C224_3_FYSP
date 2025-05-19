# Импорт функции построения остовного дерева методом Beam Search
from methods.beam_search_spanning_tree import beam_search_spanning_tree

# Функция обработки данных из формы и выполнения алгоритма
def get_data(request):
    # Инициализация словаря с пустыми значениями
    form_data = {'n': '', 'adjacency': [], 'weights': []}
    result = None  # Переменная для хранения результата алгоритма
    result_is_error = False  # Флаг, указывающий, является ли результат ошибкой

    # Проверка, был ли отправлен POST-запрос (т.е. форма отправлена)
    if request.method == 'POST':
        try:
            # Получение количества вершин из формы
            n = int(request.forms.get('n'))
            form_data['n'] = str(n)  # Сохраняем в form_data для отображения в шаблоне

            # Считывание матрицы смежности из формы
            adjacency = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'adjacency_{i}_{j}'  # Ключ для получения значения из формы
                    value = int(request.forms.get(key, 0))  # Значение по умолчанию — 0
                    row.append(value)
                adjacency.append(row)
            form_data['adjacency'] = adjacency  # Сохраняем в form_data для повторного вывода

            # Считывание матрицы весов из формы
            weights = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'weights_{i}_{j}'  # Ключ для получения значения из формы
                    value = int(request.forms.get(key, 0))  # Значение по умолчанию — 0
                    row.append(value)
                weights.append(row)
            form_data['weights'] = weights  # Сохраняем в form_data для повторного вывода

            # Задаем параметры алгоритма
            start = 0          # Начальная вершина (по умолчанию — вершина 0)
            beam_width = 2     # Ширина луча для Beam Search

            # Выполняем алгоритм построения остовного дерева
            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)

            # Проверяем, вернул ли алгоритм строку (ошибку)
            result_is_error = isinstance(tree_result, str)
            result = tree_result  # Сохраняем результат (или ошибку)

        except Exception as e:
            # В случае исключения сохраняем сообщение об ошибке
            result = f"Error: {e}"
            result_is_error = True

    # Возвращаем все данные для использования в шаблоне
    return form_data, result, result_is_error