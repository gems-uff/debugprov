import unittest

from pyalgdb.execution_tree import ExecutionTree
from pyalgdb.node import Node

class ExecutionTreeTest(unittest.TestCase):

    def test_create(self):
        root = Node(1, 1, None, 'a-script.py', None)

        childrens = []
        for i in range(2,10):
            childrens.append(Node(i, i, None, "Node #{}".format(str(i)), root))

        root.childrens = childrens
        exec_tree = ExecutionTree(root)
        self.assertEqual(exec_tree.root_node, root)
        
    def test_search_for_node_by_ccid(self):
        root = Node(1, 1, None, 'a-script.py', None)

        childrens = []
        for i in range(2,10):
            childrens.append(Node(i, i, None, "Node #{}".format(str(i)), root))

        root.childrens = childrens
        exec_tree = ExecutionTree(root)
        result = exec_tree.search_for_node_by_ccid(4)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].code_component_id, 4)
        

if __name__ == '__main__':
    unittest.main()