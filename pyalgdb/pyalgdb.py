import sqlite3

from execution_tree_creator import ExecTreeCreator


# BEGIN windows only 
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# END windows only


CURSOR = sqlite3.connect('C:/Users/linha/Desktop/ws/py-scripts-examples/script-simples2/.noworkflow/db.sqlite').cursor()




def main():
      creator = ExecTreeCreator()
      exec_tree = creator.create_exec_tree(CURSOR)


if __name__ == "__main__":
    main()

