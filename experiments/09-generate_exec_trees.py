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
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            now2_sqlite_path = os.getcwd() + '/.noworkflow/db.sqlite'
            cursor = sqlite3.connect(now2_sqlite_path).cursor()
            exec_tree = ExecTreeCreator(cursor).create_exec_tree()
            vis = CustomVisualization(exec_tree)
            vis.generate_exec_tree()
            os.chdir('..')
        os.chdir('../..')
            
os.chdir(SCRIPTS_DIRECTORY)
class CustomVisualization(Visualization):    
    def generate_exec_tree(self, graph_name = 'exec_tree'):
        file_name = "{}.gv".format(graph_name)
        print(os.getcwd())
        self.graph = Graph(graph_name, filename=file_name, directory=os.getcwd())
        self.graph.attr('node', shape='box')
        self.graph.attr('graph', ordering='out')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.ev_id), root_node.get_name(), fillcolor=self.INVALID_COLOR, style='filled') # root node
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.ev_id), str(eval_node.get_name()), fillcolor=self.NODE_IN_EVALUATION, style='filled')
        buggy_node = self.exec_tree.buggy_node
        if buggy_node is not None:
            self.graph.node(str(buggy_node.ev_id), str(buggy_node.get_name()), fillcolor=self.BUGGY_NODE_COLOR, style='filled')
        if self.exec_tree.dependencies is not None:
            for d in self.exec_tree.dependencies: # this loop draws the provenance links between nodes
                self.graph.edge(str(d.dependent.ev_id), str(d.influencer.ev_id), None, color=self.PROVENANCE_EDGE_COLOR, dir='forward')
        self.graph.render(filename='exec_tree',format='pdf')

generate_exec_trees(scripts)