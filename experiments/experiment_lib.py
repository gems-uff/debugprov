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
import copy
import os
import pandas as pd
import logging

MUTANTS_WRONG_RESULT_DIR = 'mutants.wrong_result'
ORACLE_FILENAME = 'oracle.json'
SQLITE_DB_PATH = '.noworkflow/db.sqlite'

class ExperimentLib:

    def configure(self):
        self.generate_trees = False
        self.run_1st_experiment = True
        self.run_2nd_experiment = False
        self.run_3rd_experiment = True

    def initialize_variables(self):
        self.subjects = []
        self.timestamps = []
        self.cwds = []

        self.single_stepping_results = []
        self.top_down_results = []
        self.heaviest_first_results = []
        self.divide_and_query_results = []

        self.single_stepping_prov_results = []
        self.top_down_prov_results = []
        self.heaviest_first_prov_results = []
        self.divide_and_query_prov_results = []

    def export_experiment_data(self, output_filename='output'):
        data_frame = pd.DataFrame({
            'Subject': self.subjects,
            'Timestamp': self.timestamps,
            'Cwd': self.cwds,
            'Single Stepping': self.single_stepping_results,
            'Top Down': self.top_down_results,
            'Heaviest First': self.heaviest_first_results, 
            'Divide and Query': self.divide_and_query_results,
            'Single Stepping PROV': self.single_stepping_prov_results,
            'Top Down PROV': self.top_down_prov_results,
            'Heaviest First PROV': self.heaviest_first_prov_results, 
            'Divide and Query PROV': self.divide_and_query_prov_results
        })
        data_frame.to_excel("{}.xlsx".format(output_filename)) 

    def run(self):
        os.chdir(MUTANTS_WRONG_RESULT_DIR)
        for directory in os.listdir():
            if os.path.isfile("{}/{}".format(directory,ORACLE_FILENAME)):
                timestamp = datetime.now().strftime('%Y_%m_%d %H-%M-%S.%f')
                print(timestamp)
                print("Subject: "+directory)
                logging.info("Subject: "+directory)
                self.subjects.append(directory)
                self.timestamps.append(timestamp)
                self.cwds.append(os.getcwd())
                NOW2_SQLITE_PATH = "{}/{}".format(directory,SQLITE_DB_PATH)
                ANSWER_FILE_PATH = "{}/{}".format(directory,ORACLE_FILENAME)
                CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()
                creator = ExecTreeCreator(CURSOR)

                #################################
                # FIRST EXPERIMENT
                # COMPARING NAVIGATION STRATEGIES WITHOUT PROVENANCE
                if self.run_1st_experiment:
                    original_exec_tree = creator.create_exec_tree() 
                    ##################
                    # Single Stepping
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        single_stepping = SingleStepping(exec_tree, True, ANSWER_FILE_PATH)          
                        single_stepping.navigate()
                        print("SingleStepping experiment finished: " +
                                str(single_stepping.sequence_num)+" steps.")
                        logging.info("SingleStepping experiment finished: " +
                                        str(single_stepping.sequence_num)+" steps.")
                        if self.generate_trees:
                                vis = Visualization(exec_tree)
                                vis.view_exec_tree(str(id(exec_tree)))
                        self.single_stepping_results.append(single_stepping.sequence_num)
                    except Exception as e:
                        self.single_stepping_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                    ############
                    # Top Down #
                    ############
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        top_down = TopDown(exec_tree, True, ANSWER_FILE_PATH)          
                        top_down.navigate()
                        print("TopDown experiment finished: " +
                                str(top_down.sequence_num)+" steps.")
                        logging.info("TopDown experiment finished: " +
                                        str(top_down.sequence_num)+" steps.")
                        if self.generate_trees:
                                vis = Visualization(exec_tree)
                                vis.view_exec_tree(str(id(exec_tree)))
                        self.top_down_results.append(top_down.sequence_num)
                    except Exception as e:
                        self.top_down_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                    
                    ###########
                    # Heaviest First
                    ###########
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        heaviest_first = HeaviestFirst(exec_tree, True, ANSWER_FILE_PATH)          
                        heaviest_first.navigate()
                        print("HeaviestFirst experiment finished: " +
                                str(heaviest_first.sequence_num)+" steps.")
                        logging.info("HeaviestFirst experiment finished: " +
                                        str(heaviest_first.sequence_num)+" steps.")
                        if self.generate_trees:
                                vis = Visualization(exec_tree)
                                vis.view_exec_tree(str(id(exec_tree)))
                        self.heaviest_first_results.append(top_down.sequence_num)
                    except Exception as e:
                        self.heaviest_first_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))

                    ###########
                    # Divide and Query
                    ###########
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        divide_and_query = DivideAndQuery(exec_tree, True, ANSWER_FILE_PATH)          
                        divide_and_query.navigate()
                        print("DivideAndQuery experiment finished: " +
                                str(divide_and_query.sequence_num)+" steps.")
                        logging.info("DivideAndQuery experiment finished: " +
                                        str(divide_and_query.sequence_num)+" steps.")
                        if self.generate_trees:
                                vis = Visualization(exec_tree)
                                vis.view_exec_tree(str(id(exec_tree)))
                        self.divide_and_query_results.append(divide_and_query.sequence_num)
                    except Exception as e:
                        self.divide_and_query_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))



                #################################
                # SECOND EXPERIMENT
                # COMPARING NAVIGATION STRATEGIES WITH PROVENANCE PRUNE, BUT WITHOUT ASKING WHICH OUTPUT DATA IS WRONG
                #navs = [SingleStepping, TopDown, HeaviestFirst, DivideAndQuery]
                #if RUN_2ND_EXPERIMENT:
                #    for nav in navs:
                #        exec_tree = None
                #        exec_tree = creator.create_exec_tree()
                #        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                #        prov.enhance_all()
                #        nav_instance = nav(exec_tree, True, ANSWER_FILE_PATH)
                #        nav_instance.provenance_prune()
                #        nav_instance.navigate()
                #        print(nav_instance.__class__.__name__+" experiment finished: " +
                #            str(nav_instance.sequence_num)+" steps.")
                #        if GENERATE_TREES:
                #            vis = Visualization(exec_tree)
                #            vis.view_exec_tree(str(id(exec_tree)))

                #################################
                # THIRD EXPERIMENT
                # COMPARING NAVIGATION STRATEGIES WITH PROVENANCE PRUNE, ASKING WHICH OUTPUT DATA IS WRONG
                if self.run_3rd_experiment:
                    original_exec_tree = creator.create_exec_tree() 
                    ##################
                    # Single Stepping
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        single_stepping = SingleStepping(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = single_stepping.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        single_stepping.provenance_prune()
                        single_stepping.navigate()
                        print("SingleStepping experiment finished: " +
                                str(single_stepping.sequence_num)+" steps.")
                        logging.info("SingleStepping experiment finished: " +
                                        str(single_stepping.sequence_num)+" steps.")
                        self.single_stepping_prov_results.append(single_stepping.sequence_num)
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                    except Exception as e:
                        self.single_stepping_prov_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))


                    ##################
                    # Top Down
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        top_down = TopDown(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = top_down.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        top_down.provenance_prune()
                        top_down.navigate()
                        print("TopDown experiment finished: " +
                                str(top_down.sequence_num)+" steps.")
                        logging.info("TopDown experiment finished: " +
                                        str(top_down.sequence_num)+" steps.")
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                        self.top_down_prov_results.append(top_down.sequence_num)
                    except Exception as e:
                        self.top_down_prov_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))

                    ##################
                    # Heaviest First
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        heaviest_first = HeaviestFirst(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = heaviest_first.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        heaviest_first.provenance_prune()
                        heaviest_first.navigate()
                        print("HeaviestFirst experiment finished: " +
                                str(heaviest_first.sequence_num)+" steps.")
                        logging.info("HeaviestFirst experiment finished: " +
                                        str(heaviest_first.sequence_num)+" steps.")
                        self.heaviest_first_prov_results.append(top_down.sequence_num)
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                    except Exception as e:
                        self.heaviest_first_prov_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))

                    ##################
                    # Divide and Query
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        divide_and_query = DivideAndQuery(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = divide_and_query.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        divide_and_query.provenance_prune()
                        divide_and_query.navigate()
                        print("DivideAndQuery experiment finished: " +
                                str(divide_and_query.sequence_num)+" steps.")
                        logging.info("DivideAndQuery experiment finished: " +
                                        str(divide_and_query.sequence_num)+" steps.")
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                        self.divide_and_query_prov_results.append(top_down.sequence_num)
                    except:
                        self.divide_and_query_prov_results.append(None)
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
        os.chdir('..')
