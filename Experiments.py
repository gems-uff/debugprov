#!/usr/bin/env python
# coding: utf-8

# Experiment Configs
GENERATE_TREES = False
RUN_1ST_EXPERIMENT = True
RUN_2ND_EXPERIMENT = False
RUN_3RD_EXPERIMENT = True

# Imports
import sqlite3
import time

from graphviz import Graph
from datetime import datetime
from debugprov.validity import Validity 
from debugprov.node import Node
from debugprov.provenance_enhancement import ProvenanceEnhancement
from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.top_down import TopDown
from debugprov.heaviest_first import HeaviestFirst
from debugprov.visualization import Visualization
from debugprov.single_stepping import SingleStepping
from debugprov.divide_and_query import DivideAndQuery

subjects = [
#    'experiments/selected_mutants/bisection.mutant.19',
#   'experiments/selected_mutants/heapsort.mutant.151',
    'experiments/selected_mutants/intersection.mutant.81',
#    'experiments/selected_mutants/quicksort.mutant.5'
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
            print(nav_instance.__class__.__name__+" experiment finished: "+str(nav_instance.sequence_num)+" steps.")
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
            print(nav_instance.__class__.__name__+" experiment finished: "+str(nav_instance.sequence_num)+" steps.")
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
            wrong_node_ev = exec_tree.search_by_ev_id(nav_instance.wrong_node_id)
            prov.enhance(wrong_node_ev)    
            nav_instance.provenance_prune()
            nav_instance.navigate()
            print(nav_instance.__class__.__name__+" experiment finished: "+str(nav_instance.sequence_num)+" steps.")
            if GENERATE_TREES:
                vis = Visualization(exec_tree)
                vis.view_exec_tree(str(id(exec_tree)))
