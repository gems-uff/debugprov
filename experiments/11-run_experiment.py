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
from experiment_lib import ExperimentLib
import time
import sqlite3
import copy
import os
import pandas as pd
import logging
import traceback

logging.basicConfig(filename='experiment_log.log', filemode='w',level=logging.INFO, format='%(asctime)s - %(message)s')
SCRIPTS_DIRECTORY = 'scripts'
os.chdir(SCRIPTS_DIRECTORY)

programs = [
           '02-bisection',
           '03-intersection',
           '04-lu_decomposition',
           '05-newton_method',
        ]


for program in programs:
    os.chdir(program)
    try:
        print("{} - Running experiments from {}".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f'),program))
        experiment = ExperimentLib()
        experiment.configure()
        experiment.initialize_variables()
        experiment.run()
        experiment.export_experiment_data()
        print("{} - Done".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
    except Exception as e:
        print("{} - Something went wrong".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
        print(e)
        traceback.print_exc()
    os.chdir('..')

logging.info('finished.')