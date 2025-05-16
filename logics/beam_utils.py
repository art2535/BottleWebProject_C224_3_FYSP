from methods.beam_search_spanning_tree import beam_search_spanning_tree

def get_data(request):
    form_data = {'n': '', 'adjacency': [], 'weights': []}
    result = None
    result_is_error = False

    if request.method == 'POST':
        try:
            n = int(request.forms.get('n'))
            form_data['n'] = str(n)

            adjacency = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'adjacency_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                adjacency.append(row)
            form_data['adjacency'] = adjacency

            weights = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'weights_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                weights.append(row)
            form_data['weights'] = weights

            start = 0
            beam_width = 2

            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)
            result_is_error = isinstance(tree_result, str)
            result = tree_result

        except Exception as e:
            result = f"Error: {e}"
            result_is_error = True

    return form_data, result, result_is_error