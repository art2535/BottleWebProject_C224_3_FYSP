from methods.graph_coloring_algorithm import greedy_graph_coloring, draw_colored_graph
from logics.json_utils import save_algorithm_record
import matplotlib.pyplot as plt
import matplotlib.colors

def get_data(request):
    """
    Similar to beam_utils.get_data, but tailored for greedy graph coloring.
    Returns a tuple containing:
      form_data (dict), coloring_result_table (list of dicts),
      graph_image_base64 (str), num_colors_used_info (str), error_message (str or None)
    """
    default_n = 3
    # Initialize form_data for GET requests with default number of vertices and empty adjacency matrix
    form_data = {
        'num_vertices': str(default_n),
        'adjacency_matrix': [[0]*default_n for _ in range(default_n)]
    }

    # Initialize output variables
    coloring_result_table = None
    graph_image_base64 = None
    num_colors_used_info = None
    error_message = None

    if request.method == 'POST':
        # Data structure for logging purposes
        input_for_log = {}

        try:
            # Parse and validate number of vertices
            n_str = request.forms.get('num_vertices', str(default_n)).strip()
            n = int(n_str)
            if n < 1 or n > 8:
                raise ValueError("Number of vertices must be between 1 and 8.")
            form_data['num_vertices'] = n_str
            input_for_log['num_vertices'] = n

            # Read the adjacency matrix from the form data
            adjacency = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    val = request.forms.get(f'edge_{i}_{j}', '0').strip()
                    adjacency[i][j] = int(val) if val in ('0', '1') else 0
            form_data['adjacency_matrix'] = adjacency
            input_for_log['adjacency_matrix'] = adjacency

            # Execute the greedy graph coloring algorithm
            coloring_result, num_colors_used, _ = greedy_graph_coloring(adjacency)

            # Generate color palette for visual representation
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
                        matplotlib.colors.to_hex(
                            cmap(i / (num_colors_used - 1 if num_colors_used > 1 else 1))
                        )
                        for i in range(num_colors_used)
                    ]
                # Extend palette in case the colormap has fewer distinct colors than needed
                while len(palette) < num_colors_used:
                    palette.append(matplotlib.colors.to_hex(cmap(len(palette) % cmap.N)))

            # Prepare the result table for displaying vertex-color mapping
            coloring_result_table = []
            for vertex, color_id in sorted(coloring_result.items()):
                hex_color = "#808080"  # Default grey color
                if color_id > 0 and (color_id - 1) < len(palette):
                    hex_color = palette[color_id - 1]
                elif color_id > 0:
                    hex_color = palette[(color_id - 1) % len(palette)]
                coloring_result_table.append({
                    'vertex': vertex,
                    'color_id': color_id,
                    'hex_color': hex_color
                })

            # Compose user-friendly color usage information
            num_colors_used_info = f"Number of colors used: {num_colors_used}"

            # Generate a Base64 image of the colored graph for display
            graph_image_base64 = draw_colored_graph(adjacency, coloring_result, num_colors_used)

            # Log the successful algorithm execution
            save_algorithm_record(
                algorithm='coloring',
                input_data=input_for_log,
                result_matrix=list(coloring_result.values()),
                error_message=None
            )

        except ValueError as ve:
            # Handle input validation errors and log them
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
            # Handle unexpected errors and log them
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
