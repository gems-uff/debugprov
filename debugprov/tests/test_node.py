import unittest

from debugprov.node import Node

class NodeTest(unittest.TestCase):

    def test_node(self):
        node = Node(1, 100, "#1_return", "#1_name", None)
        self.assertEqual(node.ev_id, 1)
        self.assertEqual(node.code_component_id, 100)
        self.assertEqual(node.retrn, "#1_return")
        self.assertEqual(node.name, "#1_name")
        self.assertEqual(node.parent, None)
        child_node = Node(2, 200, "#2_return", "#2_name", node)
        self.assertEqual(child_node.parent, node)
        
        

if __name__ == '__main__':
    unittest.main()