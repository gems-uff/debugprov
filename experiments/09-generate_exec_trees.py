SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil
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

scripts = ['02-bisection/bisection.py',
           '03-intersection/intersection.py',
           '04-lu_decomposition/lu_decomposition.py',
           '05-newton_method/newton_method.py',
           '06-md5/hashmd5.py',
           '07-basic_binary_tree/basic_binary_tree.py',
           '08-edit_distance/edit_distance.py',
           '09-dijkstra_algorithm/dijkstra_algorithm.py',
           '11-brute_force_caesar_cipher/brute_force_caesar_cipher.py',
           '12-basic_maths/basic_maths.py',
           '13-merge_sort/merge_sort.py',
           '15-decision_tree/decision_tree.py',
           '16-math_parser/math_parser.py',
           '17-merge_intervals/merge_intervals.py',
           '18-graph_find_path/find_path.py',
           '19-binary_search/binary_search.py',
           '20-permute/permute.py',
           '21-longest_common_subsequence/lcs.py',
           '22-catalan/catalan.py',
           '23-longest_increasing_subsequence/lis.py',
           '24-bubblesort/bubblesort.py',
           '25-quicksort/quicksort.py',
           '26-heapsort/heapsort.py',
           '28-knn/knn.py',
           '29-string_permutation/stringpermutation.py']

def generate_exec_trees(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
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
            
os.chdir(SCRIPTS_DIRECTORY)
generate_exec_trees(scripts)