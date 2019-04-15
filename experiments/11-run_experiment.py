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
import traceback

import logging
logging.basicConfig(filename='experiment_log.log', filemode='w',level=logging.INFO, format='%(asctime)s - %(message)s')

from config import Config

config = Config()
config.go_to_scripts_path()


for script_path in config.target_scripts:
    directory = script_path.split('/')[0]    
    os.chdir(directory)
    try:
        print("{} - Running experiments from {}".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f'),program))
        experiment = ExperimentLib()
        experiment.configure()
        experiment.initialize_variables()
        experiment.run()
        experiment.export_experiment_data()
        print("{} - Done".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
    except Exception:
        print("{} - Something went wrong".format(datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')))
        traceback.print_exc()
    os.chdir('..')

logging.info('finished.')