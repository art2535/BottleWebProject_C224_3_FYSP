import os
import json
from datetime import datetime

def save_algorithm_record(algorithm, input_data, result_matrix, error_message):
    """
    Save a record for a specific algorithm to the JSON file.

    Args:
        algorithm (str): Algorithm name (e.g., 'bfs', 'dfs', 'beam', 'coloring').
        input_data (dict): Raw input form data.
        result_matrix (list or None): Resulting matrix or None if failed.
        error_message (str or None): Error message or None if success.
    """
    json_path = 'static/dynamic/logos/input_data.json'
    
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Определяем название алгоритма как ключ
    algorithm_key = algorithm.lower()
    if algorithm_key not in ['bfs', 'dfs', 'beam', 'coloring']:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # Подготовка входных данных в зависимости от алгоритма
    if algorithm_key in ['bfs', 'dfs']:
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'adjacency_matrix': input_data.get('adjacency_matrix'),
            'start_vertex': input_data.get('start_vertex')
        }
    elif algorithm_key == 'beam':
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'weight_matrix': input_data.get('weight_matrix')
        }
    elif algorithm_key == 'coloring':
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'adjacency_matrix': input_data.get('adjacency_matrix')
        }
    else:
        filtered_input = input_data

    # Подготовка записи
    record = {
        'input_data': filtered_input,
        'result_matrix': result_matrix,
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'error_message': error_message
    }

    # Загрузка существующего JSON или инициализация нового
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
    except json.JSONDecodeError:
        data = {}

    # Убедимся, что ключ алгоритма есть
    if algorithm_key not in data:
        data[algorithm_key] = []

    # Добавляем новую запись
    data[algorithm_key].append(record)

    # Сохраняем обратно в файл
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)