from datetime import datetime
from methods.beam_search_spanning_tree import beam_search_spanning_tree  # Импорт алгоритма построения остовного дерева
from logics.json_utils import save_algorithm_record  # Импорт функции для сохранения истории в JSON

# Функция для считывания данных с формы
def get_data(request):
    # Инициализация словаря для хранения введённых пользователем данных формы
    form_data = {'n': '', 'adjacency': [], 'weights': []}
    result = None                 # Результат выполнения алгоритма
    result_is_error = False      # Флаг, указывающий, была ли ошибка при выполнении

    # Проверка, была ли отправлена форма методом POST
    if request.method == 'POST':
        try:
            # Получаем количество вершин графа
            n = int(request.forms.get('n'))
            form_data['n'] = str(n)

            # Считываем матрицу смежности из формы
            adjacency = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'adjacency_{i}_{j}'  # Ключ формы для каждой ячейки
                    value = int(request.forms.get(key, 0))  # Если не указано — по умолчанию 0
                    row.append(value)
                adjacency.append(row)
            form_data['adjacency'] = adjacency

            # Считываем матрицу весов из формы
            weights = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'weights_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                weights.append(row)
            form_data['weights'] = weights

            # Устанавливаем параметры для алгоритма Beam Search
            start = 0           # Начальная вершина (по умолчанию — 0)
            beam_width = 2      # Ширина луча — можно сделать настраиваемой

            # Выполняем алгоритм построения остовного дерева
            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)

            # Проверяем, произошла ли ошибка (возвращается строка с сообщением)
            result_is_error = isinstance(tree_result, str)
            result = tree_result

            # Сохраняем ввод и результат в JSON (если нет ошибки)
            save_algorithm_record(
                algorithm='beam',
                input_data={
                    'num_vertices': n,
                    'adjacency_matrix': adjacency,
                    'weight_matrix': weights
                },
                result_matrix=None if result_is_error else result,
                error_message=result if result_is_error else None
            )

        except Exception as e:
            # Если произошла ошибка — формируем сообщение
            result = f"Error: {e}"
            result_is_error = True

            # Даже при ошибке сохраняем данные в JSON для истории
            save_algorithm_record(
                algorithm='beam',
                input_data={
                    'num_vertices': form_data['n'],
                    'adjacency_matrix': form_data['adjacency'],
                    'weight_matrix': form_data['weights']
                },
                result_matrix=None,
                error_message=result
            )

    # Возвращаем все данные для отображения в шаблоне (форма, результат, флаг ошибки)
    return form_data, result, result_is_error