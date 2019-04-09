import os
import sqlite3

from graphviz import Graph
from debugprov.validity import Validity
from debugprov.node import Node
from debugprov.execution_tree import ExecutionTree
from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.top_down import TopDown
from debugprov.heaviest_first import HeaviestFirst
from debugprov.visualization import Visualization
from debugprov.provenance_enhancement import ProvenanceEnhancement 
from debugprov.single_stepping import SingleStepping
from debugprov.divide_and_query import DivideAndQuery

SCRIPTS_DIRECTORY = 'scripts'

os.chdir(SCRIPTS_DIRECTORY)

programs = ['04-lu_decomposition']

def generate_exec_trees(programs):
    for program in programs:
        print(program)
        os.chdir(program)
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            now2_sqlite_path = os.getcwd() + '/.noworkflow/db.sqlite'
            cursor = sqlite3.connect(now2_sqlite_path).cursor()
            exec_tree = ExecTreeCreator(cursor).create_exec_tree()
            vis = Visualization(exec_tree)
            vis.generate_exec_tree()
            vis.graph.render(filename='exec_tree',format='pdf')
            print('Rendering: '+os.getcwd()+'/exec_tree.pdf')
            os.chdir('..')
        os.chdir('../..')
            
generate_exec_trees(programs)