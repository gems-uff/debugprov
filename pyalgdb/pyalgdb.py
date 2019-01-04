import sqlite3

from execution_tree_creator import ExecTreeCreator
from top_down import TopDown

# BEGIN windows only 
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# END windows only


NOW2_SQLITE_PATH = 'C:/Users/linha/Desktop/ws/py-scripts-examples/script-simples2/.noworkflow/db.sqlite'

CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()


def main():
      creator = ExecTreeCreator()
      exec_tree = creator.create_exec_tree(CURSOR)
      td = TopDown()
      td.navigate(exec_tree)


if __name__ == "__main__":
    main()

