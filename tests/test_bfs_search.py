import unittest
from methods.bfs_spanning_tree import bfs_spanning_tree


class TestBFS(unittest.TestCase):
    def count_edges(self, matrix):
        """Подсчет количества рёбер в неориентированной матрице смежности."""
        return sum(sum(row) for row in matrix) // 2 if matrix else 0

    def test_bfsSpanningTree_3x3FullyConnected_ReturnsMinimumSpanningTree(self):
        # Проверка построения минимального остовного дерева на полностью связном графе из 3 узлов.
        adj = [
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 0]
        ]
        result, tree_vertices, edges = bfs_spanning_tree(3, adj, 0)
        self.assertEqual(self.count_edges(result), 2)
        self.assertEqual(sorted(tree_vertices), [0, 1, 2])
        self.assertEqual(len(edges), 2)

    def test_bfsSpanningTree_4x4DisconnectedGraph_ReturnsErrorMessage(self):
        # Проверка поведения функции при разрозненном графе — остовное дерево не может быть построено.
        adj = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ]
        result, tree_vertices, edges = bfs_spanning_tree(4, adj, 0)
        self.assertIsInstance(result, str)
        self.assertIn("not built", result)
        self.assertIsNone(tree_vertices)
        self.assertIsNone(edges)

    def test_bfsSpanningTree_SingleVertexGraph_ReturnsEmptyTree(self):
        # Проверка корректной обработки графа из одной вершины — остовное дерево пустое.
        adj = [[0]]
        result, tree_vertices, edges = bfs_spanning_tree(1, adj, 0)
        self.assertEqual(self.count_edges(result), 0)
        self.assertEqual(tree_vertices, [0])
        self.assertEqual(edges, [])

    def test_bfsSpanningTree_LineGraph_ReturnsLinearSpanningTree(self):
        # Проверка корректного построения остовного дерева на линейном графе (цепочке).
        adj = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        result, tree_vertices, edges = bfs_spanning_tree(4, adj, 0)
        self.assertEqual(self.count_edges(result), 3)
        self.assertEqual(sorted(tree_vertices), [0, 1, 2, 3])
        self.assertEqual(len(edges), 3)

    def test_bfsSpanningTree_FullyConnected4VerticesGraph_ReturnsValidSpanningTree(self):
        # Проверка построения остовного дерева на полном графе с 4 вершинами.
        n = 4
        adj = [[1 if i != j else 0 for j in range(n)] for i in range(n)]
        result, tree_vertices, edges = bfs_spanning_tree(n, adj, 0)
        self.assertEqual(self.count_edges(result), n - 1)
        self.assertEqual(sorted(tree_vertices), list(range(n)))
        self.assertEqual(len(edges), n - 1)

    def test_bfsSpanningTree_TwoDisconnectedComponents_ReturnsErrorMessage(self):
        # Проверка поведения при графе, содержащем две несвязанные компоненты — дерево не построится.
        adj = [
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]
        result, tree_vertices, edges = bfs_spanning_tree(5, adj, 0)
        self.assertIsInstance(result, str)
        self.assertIn("not built", result)
        self.assertIsNone(tree_vertices)
        self.assertIsNone(edges)

    def test_bfsSpanningTree_LinearChain5Vertices_ReturnsTreeWithoutCycles(self):
        # Проверка корректной обработки цепочки из 5 узлов — результатом будет дерево из 4 рёбер.
        adj = [
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ]
        result, tree_vertices, edges = bfs_spanning_tree(5, adj, 0)
        self.assertEqual(self.count_edges(result), 4)
        self.assertEqual(sorted(tree_vertices), [0, 1, 2, 3, 4])
        self.assertEqual(len(edges), 4)

    def test_bfsSpanningTree_SameGraphDifferentStartNodes_ReturnsSameSpanningTreeStructure(self):
        # Проверка устойчивости результата BFS остовного дерева при разных стартовых вершинах на одном графе.
        adj = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]
        result1, vertices1, edges1 = bfs_spanning_tree(4, adj, 0)
        result2, vertices2, edges2 = bfs_spanning_tree(4, adj, 2)
        self.assertEqual(self.count_edges(result1), 3)
        self.assertEqual(self.count_edges(result2), 3)
        self.assertEqual(sorted(vertices1), [0, 1, 2, 3])
        self.assertEqual(sorted(vertices2), [0, 1, 2, 3])
        self.assertEqual(len(edges1), 3)
        self.assertEqual(len(edges2), 3)


if __name__ == '__main__':
    unittest.main()
