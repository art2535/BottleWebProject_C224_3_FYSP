import os
import json
from datetime import datetime

# Function: save_algorithm_record
# Description:
#     Saves the input and result of a specific algorithm execution (such as BFS, DFS, Beam Search, or Graph Coloring)
#     into a JSON file for logging and history tracking purposes.
#     Handles creation of directories if missing, filters input data per algorithm,
#     timestamps the record, appends it to existing JSON data, and writes it back.
#
# Parameters:
#     algorithm (str): The name of the algorithm (e.g., 'bfs', 'dfs', 'beam', 'coloring').
#     input_data (dict): The raw input data used for the algorithm execution.
#     result_matrix (list or None): The result of the algorithm (usually a matrix or list), or None if there was an error.
#     error_message (str or None): Error message if an error occurred, otherwise None.
#
# Returns:
#     None
def save_algorithm_record(algorithm, input_data, result_matrix, error_message):
    # Path to the JSON file where records will be saved
    json_path = 'static/dynamic/logos/input_data.json'
    
    # Ensure the directory for the JSON file exists, create if necessary
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Normalize algorithm name to lowercase for consistent keys
    algorithm_key = algorithm.lower()
    # Validate algorithm key to accept only known algorithms
    if algorithm_key not in ['bfs', 'dfs', 'beam', 'coloring']:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # Filter input data fields according to the algorithm type
    if algorithm_key in ['bfs', 'dfs']:
        # BFS and DFS expect num_vertices, adjacency_matrix, and start_vertex
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'adjacency_matrix': input_data.get('adjacency_matrix'),
            'start_vertex': input_data.get('start_vertex')
        }
    elif algorithm_key == 'beam':
        # Beam search expects num_vertices and weight_matrix (note: adjacency_matrix is omitted here)
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'weight_matrix': input_data.get('weight_matrix')
        }
    elif algorithm_key == 'coloring':
        # Graph coloring expects num_vertices and adjacency_matrix
        filtered_input = {
            'num_vertices': input_data.get('num_vertices'),
            'adjacency_matrix': input_data.get('adjacency_matrix')
        }
    else:
        # Fallback: save input data as is
        filtered_input = input_data

    # Prepare the record dictionary with input, result, timestamp and error
    record = {
        'input_data': filtered_input,
        'result_matrix': result_matrix,
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'error_message': error_message
    }

    # Try loading existing JSON data from file or start a new dictionary if fails
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
    except json.JSONDecodeError:
        # If JSON is invalid, overwrite with fresh dictionary
        data = {}

    # Ensure there is a list to hold records for the current algorithm
    if algorithm_key not in data:
        data[algorithm_key] = []

    # Append the new record to the list for this algorithm
    data[algorithm_key].append(record)

    # Write the updated data dictionary back to the JSON file with pretty formatting
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)