import unittest
import sys
import sqlite3

from pyalgdb.src.execution_tree_creator import ExecTreeCreator
from pyalgdb.src.node import Node


class ExecTreeCreatorTest(unittest.TestCase):

    DB_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/pyalgdb/pyalgdb/tests/db.sqlite'

    def setUp(self):
        cursor = sqlite3.connect(self.DB_SQLITE_PATH).cursor()
        self.execTreeCreator = ExecTreeCreator(cursor)

    def test_get_root(self):
        root = self.execTreeCreator.get_root()
        self.assertEqual(root.id, 1)
        self.assertEqual(root.code_component_id, 1)
        self.assertEqual(root.name, 'script-simples.py')
        self.assertEqual(root.validity, False)

if __name__ == '__main__':
    unittest.main()