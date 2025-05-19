import os
import json
from datetime import datetime

def save_algorithm_record(algorithm, input_data, result_matrix, error_message):
    """
    Save a record for an algorithm build to the JSON file.
    
    Args:
        algorithm (str): Algorithm name (e.g., 'bfs', 'beam').
        input_data (dict): Input form data (num_vertices, adjacency_matrix, start_vertex).
        result_matrix (list or None): Resulting matrix or None if build failed.
        error_message (str or None): Error message or None if successful.
    """
    json_path = 'static/dynamic/logos/input_data.json'
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    # Initialize record
    record = {
        'input_data': input_data,
        'result_matrix': result_matrix,
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'error_message': error_message
    }
    
    # Load existing JSON or initialize
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
    except json.JSONDecodeError:
        data = {}
    
    # Initialize algorithm key if not present
    if algorithm not in data:
        data[algorithm] = []
    
    # Append record
    data[algorithm].append(record)
    
    # Save to JSON
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)