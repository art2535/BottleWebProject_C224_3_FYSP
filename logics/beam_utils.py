from datetime import datetime
from methods.beam_search_spanning_tree import beam_search_spanning_tree  # ������ ��������� ���������� ��������� ������
from logics.json_utils import save_algorithm_record  # ������ ������� ��� ���������� ������� � JSON

# ������� ��� ���������� ������ � �����
def get_data(request):
    # ������������� ������� ��� �������� �������� ������������� ������ �����
    form_data = {'n': '', 'adjacency': [], 'weights': []}
    result = None                 # ��������� ���������� ���������
    result_is_error = False      # ����, �����������, ���� �� ������ ��� ����������

    # ��������, ���� �� ���������� ����� ������� POST
    if request.method == 'POST':
        try:
            # �������� ���������� ������ �����
            n = int(request.forms.get('n'))
            form_data['n'] = str(n)

            # ��������� ������� ��������� �� �����
            adjacency = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'adjacency_{i}_{j}'  # ���� ����� ��� ������ ������
                    value = int(request.forms.get(key, 0))  # ���� �� ������� � �� ��������� 0
                    row.append(value)
                adjacency.append(row)
            form_data['adjacency'] = adjacency

            # ��������� ������� ����� �� �����
            weights = []
            for i in range(n):
                row = []
                for j in range(n):
                    key = f'weights_{i}_{j}'
                    value = int(request.forms.get(key, 0))
                    row.append(value)
                weights.append(row)
            form_data['weights'] = weights

            # ������������� ��������� ��� ��������� Beam Search
            start = 0           # ��������� ������� (�� ��������� � 0)
            beam_width = 2      # ������ ���� � ����� ������� �������������

            # ��������� �������� ���������� ��������� ������
            tree_result = beam_search_spanning_tree(n, adjacency, weights, start, beam_width)

            # ���������, ��������� �� ������ (������������ ������ � ����������)
            result_is_error = isinstance(tree_result, str)
            result = tree_result

            # ��������� ���� � ��������� � JSON (���� ��� ������)
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
            # ���� ��������� ������ � ��������� ���������
            result = f"Error: {e}"
            result_is_error = True

            # ���� ��� ������ ��������� ������ � JSON ��� �������
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

    # ���������� ��� ������ ��� ����������� � ������� (�����, ���������, ���� ������)
    return form_data, result, result_is_error