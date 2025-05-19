import unittest
from methods.bfs_spanning_tree import bfs_spanning_tree  # Замените на актуальный путь к вашей функции


class TestBFS(unittest.TestCase):
    def count_edges(self, matrix):
        """Подсчет количества рёбер в неориентированной матрице смежности."""
        return sum(sum(row) for row in matrix) // 2 if matrix else 0

    def test_bfs_3x3_simple_tree(self):
        """Проверка на простом связанном графе 3x3."""
        adj = [
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 0]
        ]
        result, order = bfs_spanning_tree(3, adj, 0)
        self.assertEqual(self.count_edges(result), 2)
        self.assertEqual(sorted(order), [0, 1, 2])

    def test_bfs_4x4_disconnected(self):
        """Проверка на несвязном графе — должно вернуть сообщение об ошибке."""
        adj = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]
        result, order = bfs_spanning_tree(4, adj, 0)
        self.assertIsInstance(result, str)
        self.assertIn("not built", result)
        self.assertIsNone(order)

    def test_bfs_single_vertex(self):
        """Граф с одной вершиной — пустое дерево."""
        adj = [[0]]
        result, order = bfs_spanning_tree(1, adj, 0)
        self.assertEqual(self.count_edges(result), 0)
        self.assertEqual(order, [0])

    def test_bfs_line_graph(self):
        """Проверка на графе-цепочке."""
        adj = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        result, order = bfs_spanning_tree(4, adj, 0)
        self.assertEqual(self.count_edges(result), 3)
        self.assertEqual(sorted(order), [0, 1, 2, 3])

    def test_bfs_full_graph(self):
        """Полносвязный граф на 4 вершины — должен быть построен корректный остов."""
        n = 4
        adj = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
        result, order = bfs_spanning_tree(n, adj, 0)
        self.assertEqual(self.count_edges(result), n - 1)
        self.assertEqual(sorted(order), list(range(n)))

    def test_bfs_multiple_components(self):
        """Граф из двух несвязных компонентов — ожидается ошибка."""
        adj = [
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]
        result, order = bfs_spanning_tree(5, adj, 0)
        self.assertIsInstance(result, str)
        self.assertIn("not built", result)
        self.assertIsNone(order)

    def test_bfs_tree_structure_check(self):
        """Проверка, что граф без циклов остаётся деревом после BFS."""
        adj = [
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ]
        result, order = bfs_spanning_tree(5, adj, 0)
        self.assertEqual(self.count_edges(result), 4)
        self.assertEqual(sorted(order), [0, 1, 2, 3, 4])

    def test_bfs_different_start_nodes(self):
        """Проверка, что при разных стартовых вершинах дерево корректно перестраивается."""
        adj = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]
        result1, order1 = bfs_spanning_tree(4, adj, 0)
        result2, order2 = bfs_spanning_tree(4, adj, 2)
        self.assertEqual(self.count_edges(result1), 3)
        self.assertEqual(self.count_edges(result2), 3)
        self.assertEqual(sorted(order1), [0, 1, 2, 3])
        self.assertEqual(sorted(order2), [0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()

