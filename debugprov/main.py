import sqlite3

from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.top_down import TopDown
from debugprov.heaviest_first import HeaviestFirst
from debugprov.visualization import Visualization
from debugprov.provenance_enhancement import ProvenanceEnhancement
from debugprov.single_stepping import SingleStepping
from debugprov.divide_and_query import DivideAndQuery

# BEGIN windows only 
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# END windows only


NOW2_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/py-scripts-examples/age-avg/.noworkflow/db.sqlite'

CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()


def main():
      creator = ExecTreeCreator(CURSOR)
      exec_tree = creator.create_exec_tree()
      nav = TopDown(exec_tree)
      #nav = ProvenanceNavigation(exec_tree, CURSOR)
      result_tree = nav.navigate()
      vis = Visualization(result_tree)
      vis.view_exec_tree('exec_tree')
      #vis.view_exec_tree_prov('exec_tree',nav.DEPENDENCIES)
      #vis.view_exec_tree()

if __name__ == "__main__":
    main()
