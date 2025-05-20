# logics/greedy_utils.py

from methods.graph_coloring_algorithm import greedy_graph_coloring, draw_colored_graph
from logics.json_utils import save_algorithm_record
import matplotlib.pyplot as plt
import matplotlib.colors

def get_data(request):
    """
    Processes an HTTP request related to the greedy coloring algorithm
    and returns a tuple containing:
        - form_data (dict): number of vertices and adjacency matrix
        - coloring_result_table (list of dicts): result for display
        - graph_image_base64 (str): image of the graph (base64 format)
        - num_colors_used_info (str): text info on number of colors used
        - error_message (str or None): error message if one occurred
    """
    default_n = 3  # Default number of vertices if not specified

    # Initial form state (used for rendering form fields)
    form_data = {
        'num_vertices': str(default_n),
        'adjacency_matrix': [[0] * default_n for _ in range(default_n)]
    }

    # Variables for the result and error display
    coloring_result_table = None
    graph_image_base64 = None
    num_colors_used_info = None
    error_message = None

    # Only handle logic if request is POST (form submission)
    if request.method == 'POST':
        input_for_log = {}  # Data to be saved in logs

        try:
            # Read and validate number of vertices
            n_str = request.forms.get('num_vertices', str(default_n)).strip()
            n = int(n_str)

            if n < 1 or n > 8:
                raise ValueError("Number of vertices must be between 1 and 8.")

            form_data['num_vertices'] = n_str
            input_for_log['num_vertices'] = n

            # Parse the adjacency matrix from the form
            adjacency = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    key = f'edge_{i}_{j}'
                    val = request.forms.get(key, '0').strip()
                    adjacency[i][j] = int(val) if val in ('0', '1') else 0

            form_data['adjacency_matrix'] = adjacency
            input_for_log['adjacency_matrix'] = adjacency

            # Run the greedy coloring algorithm
            coloring_result, num_colors_used, _ = greedy_graph_coloring(adjacency)

            # Build the color palette (HEX strings) based on number of colors used
            palette = []
            if num_colors_used > 0:
                if num_colors_used <= 10:
                    cmap = plt.cm.get_cmap('tab10')
                    palette = [matplotlib.colors.to_hex(cmap(i)) for i in range(num_colors_used)]
                elif num_colors_used <= 20:
                    cmap = plt.cm.get_cmap('tab20')
                    palette = [matplotlib.colors.to_hex(cmap(i)) for i in range(num_colors_used)]
                else:
                    cmap = plt.cm.get_cmap('viridis')
                    palette = [
                        matplotlib.colors.to_hex(cmap(i / (num_colors_used - 1 if num_colors_used > 1 else 1)))
                        for i in range(num_colors_used)
                    ]

                # Ensure the palette has enough colors (as a fallback)
                while len(palette) < num_colors_used:
                    palette.append(matplotlib.colors.to_hex(cmap(len(palette) % cmap.N)))

            # Build a table of results to display in the HTML
            coloring_result_table = []
            for vertex, color_id in sorted(coloring_result.items()):
                hex_color = "#808080"  # Default to grey if something goes wrong
                if color_id > 0:
                    idx = (color_id - 1) % len(palette) if palette else 0
                    hex_color = palette[idx]

                coloring_result_table.append({
                    'vertex': vertex,
                    'color_id': color_id,
                    'hex_color': hex_color
                })

            # Info text about total number of colors used
            num_colors_used_info = f"Number of colors used: {num_colors_used}"

            # Generate graph image
            graph_image_base64 = draw_colored_graph(adjacency, coloring_result, num_colors_used)

            # Save the run to a log for tracking / audit purposes
            save_algorithm_record(
                algorithm='coloring',
                input_data=input_for_log,
                result_matrix=[
                    {'vertex': v, 'color_id': c}
                    for v, c in sorted(coloring_result.items())
                ],
                error_message=None
            )

        except ValueError as ve:
            # Handle invalid user input (e.g., wrong number of vertices)
            error_message = str(ve)
            save_algorithm_record(
                algorithm='coloring',
                input_data=form_data,
                result_matrix=None,
                error_message=error_message
            )
            coloring_result_table = None
            graph_image_base64 = None
            num_colors_used_info = None

        except Exception as ex:
            # Handle unexpected errors (e.g., internal logic failures)
            error_message = f"An unexpected server error occurred: {ex}"
            save_algorithm_record(
                algorithm='coloring',
                input_data=form_data,
                result_matrix=None,
                error_message=error_message
            )
            coloring_result_table = None
            graph_image_base64 = None
            num_colors_used_info = None

    return form_data, coloring_result_table, graph_image_base64, num_colors_used_info, error_message
