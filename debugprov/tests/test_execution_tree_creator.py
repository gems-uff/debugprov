import unittest
import sys
import sqlite3

from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.node import Node
from debugprov.validity import Validity

class ExecTreeCreatorTest(unittest.TestCase):

    DB_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/debugprov/debugprov/tests/db.sqlite'
    CURSOR = sqlite3.connect(DB_SQLITE_PATH).cursor()

    def setUp(self):
        self.execTreeCreator = ExecTreeCreator(self.CURSOR)

    def test_get_root(self):
        root = self.execTreeCreator.get_root()
        query = ("select EV.id, CC.id, EV.repr, CC.name "
                 "from evaluation EV "
                 "natural join activation ACT "
                 "join code_component CC on EV.code_component_id = CC.id "
                 "where activation_id = ? ")
        
        for tupl in self.CURSOR.execute(query, [0]):
            ev_id = tupl[0]
            cc_id = tupl[1]
            ev_repr = tupl[2] 
            cc_name = tupl[3]

        self.assertEqual(root.ev_id, ev_id)
        self.assertEqual(root.code_component_id, cc_id)
        self.assertEqual(root.retrn, ev_repr)
        self.assertEqual(root.name, cc_name)
        self.assertEqual(root.validity, Validity.UNKNOWN)

    def test_create_exec_tree(self):
        exec_tree = self.execTreeCreator.create_exec_tree()
        root_node = exec_tree.root_node
        self.assertEqual(root_node.ev_id,1)
        self.assertEqual(root_node.code_component_id,1)
        self.assertEqual(root_node.name, 'script-simples.py')
        self.assertIsNone(root_node.parent)
        self.assertEqual(len(root_node.childrens), 5)
        self.assertIsNone(exec_tree.buggy_node)
        self.assertIsNone(exec_tree.node_under_evaluation)
        self.assertFalse(exec_tree.is_prov_enhanced)
        self.assertIsNone(exec_tree.dependencies)
        childrens_ids = [9,31,37,42,49]
        idx = 0
        for c in root_node.childrens:
            self.assertEquals(c.ev_id, childrens_ids[idx])
            idx += 1
        
if __name__ == '__main__':
    unittest.main()