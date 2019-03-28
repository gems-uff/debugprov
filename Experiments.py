#!/usr/bin/env python
# coding: utf-8

# Experiment Configs
from debugprov.validity import Validity
from debugprov.divide_and_query import DivideAndQuery
from debugprov.single_stepping import SingleStepping
from debugprov.visualization import Visualization
from debugprov.heaviest_first import HeaviestFirst
from debugprov.top_down import TopDown
from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.provenance_enhancement import ProvenanceEnhancement
from debugprov.node import Node
from datetime import datetime
from graphviz import Graph
import time
import sqlite3
GENERATE_TREES = False
RUN_1ST_EXPERIMENT = True
RUN_2ND_EXPERIMENT = False
RUN_3RD_EXPERIMENT = True

# Imports


subjects = [
    'experiments/selected_mutants/bisection.mutant.19', # 02-bisection
    'experiments/selected_mutants/bisection.mutant.108', # 02-bisection
    
    'experiments/selected_mutants/intersection.mutant.81', # 03-intersection

    'experiments/selected_mutants/lu_decomposition.mutant.84', # 04-lu_decomposition

    'experiments/selected_mutants/newton_method.mutant.35', # 05-newton_method

    'experiments/selected_mutants/basic_binary_tree.mutant.56', # 07-basic_binary_tree
    
    # Skipping 08-edit_distance
    # Skipping 09-dijkstra_algorithm
    # Skipping 10-caesar_cipher
    # Skipping 11-caesar_cipher
    # 'experiments/selected_mutants/basic_maths.mutant.117', stuck in infinite loop
    'experiments/selected_mutants/merge_sort.mutant.3', # 13-merge_sort
    # 'experiments/selected_mutants/math_parser.mutant.213', # 16-math_parser
    'experiments/selected_mutants/merge_intervals.mutant.206', # 17-merge_intervals
    'experiments/selected_mutants/binary_search.mutant.15',
    # 'experiments/selected_mutants/permute.mutant.119', # 20-permute
    'experiments/selected_mutants/lcs.mutant.101', # 21-longest_common_subsequence

    'experiments/selected_mutants/lis.mutant.88', # 23-longest_increasing_subsequence


 
    #'experiments/selected_mutants/heapsort.mutant.151',
    #'experiments/selected_mutants/quicksort.mutant.5'
]

for subject in subjects:
    print(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f'))
    print("Subject: "+subject)
    NOW2_SQLITE_PATH = "{}/.noworkflow/db.sqlite".format(subject)
    ANSWER_FILE_PATH = "{}/answers.json".format(subject)
    CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()
    creator = ExecTreeCreator(CURSOR)

    #################################
    # FIRST EXPERIMENT
    # COMPARING NAVIGATION STRATEGIES WITHOUT PROVENANCE
    navs = [SingleStepping, TopDown, HeaviestFirst, DivideAndQuery]
    if RUN_1ST_EXPERIMENT:
        for nav in navs:
            exec_tree = None
            exec_tree = creator.create_exec_tree()
            nav_instance = nav(exec_tree, True, ANSWER_FILE_PATH)
            nav_instance.navigate()
            print(nav_instance.__class__.__name__+" experiment finished: " +
                  str(nav_instance.sequence_num)+" steps.")
            if GENERATE_TREES:
                vis = Visualization(exec_tree)
                vis.view_exec_tree(str(id(exec_tree)))

    #################################
    # SECOND EXPERIMENT
    # COMPARING NAVIGATION STRATEGIES WITH PROVENANCE PRUNE, BUT WITHOUT ASKING WHICH OUTPUT DATA IS WRONG
    navs = [SingleStepping, TopDown, HeaviestFirst, DivideAndQuery]
    if RUN_2ND_EXPERIMENT:
        for nav in navs:
            exec_tree = None
            exec_tree = creator.create_exec_tree()
            prov = ProvenanceEnhancement(exec_tree, CURSOR)
            prov.enhance_all()
            nav_instance = nav(exec_tree, True, ANSWER_FILE_PATH)
            nav_instance.provenance_prune()
            nav_instance.navigate()
            print(nav_instance.__class__.__name__+" experiment finished: " +
                  str(nav_instance.sequence_num)+" steps.")
            if GENERATE_TREES:
                vis = Visualization(exec_tree)
                vis.view_exec_tree(str(id(exec_tree)))

    #################################
    # THIRD EXPERIMENT
    # COMPARING NAVIGATION STRATEGIES WITH PROVENANCE PRUNE, ASKING WHICH OUTPUT DATA IS WRONG
    navs = [SingleStepping, TopDown, HeaviestFirst, DivideAndQuery]
    if RUN_3RD_EXPERIMENT:
        for nav in navs:
            exec_tree = None
            exec_tree = creator.create_exec_tree()
            nav_instance = nav(exec_tree, True, ANSWER_FILE_PATH)
            prov = ProvenanceEnhancement(exec_tree, CURSOR)
            wrong_node_ev = exec_tree.search_by_ev_id(
                nav_instance.wrong_node_id)
            prov.enhance(wrong_node_ev)
            nav_instance.provenance_prune()
            nav_instance.navigate()
            print(nav_instance.__class__.__name__+" experiment finished: " +
                  str(nav_instance.sequence_num)+" steps.")
            if GENERATE_TREES:
                vis = Visualization(exec_tree)
                vis.view_exec_tree(str(id(exec_tree)))
