import unittest

import sqlite3
from graphviz import Graph
from pyalgdb.validity import Validity 
from pyalgdb.node import Node
from pyalgdb.provenance_enhancement import ProvenanceEnhancement
from pyalgdb.execution_tree_creator import ExecTreeCreator
from pyalgdb.top_down import TopDown
from pyalgdb.heaviest_first import HeaviestFirst
from pyalgdb.visualization import Visualization
from pyalgdb.single_stepping import SingleStepping
from pyalgdb.divide_and_query import DivideAndQuery

class EndToEndTest(unittest.TestCase):

    def test_age_avg(self):
        ANSWER_FILE_PATH = 'aux_files/age-avg-answers.json'
        SQLITE_PATH = 'C:/Users/linha/Desktop/ws/py-scripts-examples/age-avg/.noworkflow/db.sqlite'
        CURSOR = sqlite3.connect(SQLITE_PATH).cursor()
        creator = ExecTreeCreator(CURSOR)
        navs = [SingleStepping, TopDown, HeaviestFirst, DivideAndQuery] 
        results = []
        for nav in navs:
            exec_tree = None
            exec_tree = creator.create_exec_tree()
            nav_instance = nav(exec_tree, True, ANSWER_FILE_PATH)
            nav_instance.navigate()
            vis = Visualization(exec_tree)
            vis.generate_exec_tree()
            results.append(str(vis.graph))
            
        SS_FILE = 'pyalgdb/tests/test_files/age-avg-ss.gv'
        TD_FILE = 'pyalgdb/tests/test_files/age-avg-td.gv'
        HF_FILE = 'pyalgdb/tests/test_files/age-avg-hf.gv'
        DQ_FILE = 'pyalgdb/tests/test_files/age-avg-dq.gv'
        
        result_files = [SS_FILE,TD_FILE,HF_FILE,DQ_FILE]
        idx = 0
        for idx,val in enumerate(result_files):
            with open(val, 'r') as myfile:
                content = myfile.read()
                self.assertEquals(content,results[idx])
        
if __name__ == '__main__':
    unittest.main()