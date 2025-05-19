from datetime import datetime
from methods.beam_search_spanning_tree import beam_search_spanning_tree
from logics.json_utils import save_algorithm_record

def get_data(request):
    """
    Function: get_data
    Description:
        Processes an HTTP request containing input data for constructing a graph and
        running the Beam Search Spanning Tree algorithm on it.
        Extracts and validates form inputs, builds adjacency and weight matrices,
        executes the algorithm, handles possible errors,
        and saves the input and result (or error) using save_algorithm_record.

    Parameters:
        request (object): The HTTP request object containing form data with fields:
            - 'n' (str): Number of vertices (expected between 3 and 7).
            - 'adjacency_i_j' (str): Adjacency matrix entries (0 or 1) for each i, j.
            - 'weights_i_j' (str): Weight matrix entries (non-negative integers) for each i, j.

    Returns:
        tuple:
            form_data (dict): Parsed and validated form data with keys:
                - 'n' (str): Number of vertices as string.
                - 'adjacency' (list of lists of int): Adjacency matrix.
                - 'weights' (list of lists of int): Weight matrix.
            result (object): Algorithm result (matrix or error message string).
            result_is_error (bool): True if result is an error message, False otherwise.
    """
    # Default number of vertices if the user does not specify one
    default_n = 3
    
    # Initialize the form_data dictionary with default values for the form fields
    form_data = {
        'n': str(default_n),
        'adjacency': [[0] * default_n for _ in range(default_n)],
        'weights': [[0] * default_n for _ in range(default_n)]
    }
    
    # Initialize variables to hold the algorithm result and error status
    result = None
    result_is_error = False

    # Process the input only if the HTTP method is POST (form submission)
    if request.method == 'POST':
        try:
            # Retrieve and validate the number of vertices from form input
            n_str = request.forms.get('n', str(default_n)).strip()
            n = int(n_str)
            # Enforce a valid range of vertices between 3 and 7
            if n < 3 or n > 7:
                raise ValueError("Number of vertices must be between 3 and 7")
            form_data['n'] = n_str

            # Initialize adjacency and weight matrices with zeros according to n
            adjacency = [[0] * n for _ in range(n)]
            weights = [[0] * n for _ in range(n)]

            # Fill adjacency matrix with values from the form input
            for i in range(n):
                for j in range(n):
                    key = f'adjacency_{i}_{j}'
                    val_str = request.forms.get(key, '0').strip()
                    try:
                        value = int(val_str)
                        # Only allow 0 or 1 in adjacency matrix
                        if value not in [0, 1]:
                            value = 0
                    except ValueError:
                        value = 0
                    adjacency[i][j] = value
            form_data['adjacency'] = adjacency

            # Fill weight matrix with values from the form input
            for i in range(n):
                for j in range(n):
                    key = f'weights_{i}_{j}'
                    val_str = request.forms.get(key, '0').strip()
                    try:
                        value = int(val_str)
                        # Weights must be non-negative integers
                        if value < 0:
                            value = 0
                    except ValueError:
                        value = 0
                    weights[i][j] = value
            form_data['weights'] = weights

            # Define fixed start vertex and beam width for the algorithm
            start = 0
            beam_width = 2
            # Execute the beam search spanning tree algorithm
            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)

            # Determine if the result is an error (string) or valid output (matrix)
            result_is_error = isinstance(tree_result, str)
            result = tree_result

            # Save the input and result or error message to a JSON record
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
            # Handle exceptions, prepare an error message, and mark as error
            result = f"Error: {e}"
            result_is_error = True

            # Save the error and last known input data for logging
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

    # Return the form data, the algorithm's output or error, and the error flag
    return form_data, result, result_is_error