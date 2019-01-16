import unittest
import sys
import sqlite3

from pyalgdb.execution_tree_creator import ExecTreeCreator
from pyalgdb.node import Node
from pyalgdb.validity import Validity

class ExecTreeCreatorTest(unittest.TestCase):

    DB_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/pyalgdb/pyalgdb/tests/db.sqlite'
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

        self.assertEqual(root.id, ev_id)
        self.assertEqual(root.code_component_id, cc_id)
        self.assertEqual(root.retrn, ev_repr)
        self.assertEqual(root.name, cc_name)
        self.assertEqual(root.validity, Validity.UNKNOWN)

if __name__ == '__main__':
    unittest.main()