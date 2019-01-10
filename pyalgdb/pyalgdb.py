import sqlite3

from execution_tree_creator import ExecTreeCreator
from top_down import TopDown
from heaviest_first import HeaviestFirst
from visualization import Visualization
from provenance_navigation import ProvenanceNavigation

# BEGIN windows only 
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# END windows only


NOW2_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/py-scripts-examples/age-avg/.noworkflow/db.sqlite'

CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()


def main():
      creator = ExecTreeCreator(CURSOR)
      exec_tree = creator.create_exec_tree()
      exec_tree.validity = False # invalidate root
      nav = ProvenanceNavigation(exec_tree, CURSOR)
      result_tree = nav.navigate()
      Visualization().view_exec_tree_prov(result_tree, nav.DEPENDENCIES)
      # Visualization().view_exec_tree(result_tree)

if __name__ == "__main__":
    main()

