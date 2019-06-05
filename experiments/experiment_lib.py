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
import sys

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

        self.expected_buggy_node = []

        self.single_stepping = {
            "single_stepping_results": [],
            "single_stepping_buggy_node_returned": [],
            "single_stepping_prov_results": [],
            "single_stepping_prov_buggy_node_returned": []
        }

        self.top_down = {
            "top_down_results": [],
            "top_down_buggy_node_returned": [],
            "top_down_prov_results": [],
            "top_down_prov_buggy_node_returned": []
        }

        self.heaviest_first = {
            "heaviest_first_results": [],
            "heaviest_first_buggy_node_returned": [],
            "heaviest_first_prov_results": [],
            "heaviest_first_prov_buggy_node_returned": []
        }

        self.divide_and_query = {
            "divide_and_query_results": [],
            "divide_and_query_buggy_node_returned": [],
            "divide_and_query_prov_results": [],
            "divide_and_query_prov_buggy_node_returned": []
        }



    def export_experiment_data(self, output_filename='output'):
        data_frame = pd.DataFrame({
            'Subject': self.subjects,
            'Timestamp': self.timestamps,
            'Cwd': self.cwds,
            'Expected Buggy Node': self.expected_buggy_node,
            'Single Stepping': self.single_stepping["single_stepping_results"],
            'Single Stepping Buggy Node Found': self.single_stepping["single_stepping_buggy_node_returned"],
            'Top Down': self.top_down["top_down_results"],
            'Top Down Buggy Node Found': self.top_down["top_down_buggy_node_returned"],
            'Heaviest First': self.heaviest_first["heaviest_first_results"], 
            'Heaviest First Buggy Node Found': self.heaviest_first["heaviest_first_buggy_node_returned"], 
            'Divide and Query': self.divide_and_query["divide_and_query_results"],
            'Divide and Query Buggy Node Found': self.divide_and_query["divide_and_query_buggy_node_returned"],
            'Single Stepping PROV': self.single_stepping["single_stepping_prov_results"],
            'Single Stepping PROV Buggy Node Found': self.single_stepping["single_stepping_prov_buggy_node_returned"],
            'Top Down PROV': self.top_down["top_down_prov_results"],
            'Top Down PROV Buggy Node Found': self.top_down["top_down_prov_buggy_node_returned"],
            'Heaviest First PROV': self.heaviest_first["heaviest_first_prov_results"], 
            'Heaviest First PROV Buggy Node Found': self.heaviest_first["heaviest_first_prov_buggy_node_returned"],
            'Divide and Query PROV': self.divide_and_query["divide_and_query_prov_results"],
            'Divide and Query PROV Buggy Node Found': self.divide_and_query["divide_and_query_prov_buggy_node_returned"],
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
                        self.expected_buggy_node.append(max(single_stepping.invalid_nodes))
                        self.single_stepping["single_stepping_results"].append(single_stepping.sequence_num)
                        if single_stepping.exec_tree.buggy_node is not None:
                            self.single_stepping["single_stepping_buggy_node_returned"].append(single_stepping.exec_tree.buggy_node.ev_id)
                        else:
                            self.single_stepping["single_stepping_buggy_node_returned"].append(None)
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()
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
                        self.top_down["top_down_results"].append(top_down.sequence_num)
                        if top_down.exec_tree.buggy_node is not None:
                            self.top_down["top_down_buggy_node_returned"].append(top_down.exec_tree.buggy_node.ev_id)
                        else:
                            self.single_stepping["top_down_buggy_node_returned"].append(None)
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()
                    
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
                        self.heaviest_first["heaviest_first_results"].append(heaviest_first.sequence_num)
                        if heaviest_first.exec_tree.buggy_node is not None:
                            self.heaviest_first["heaviest_first_buggy_node_returned"].append(heaviest_first.exec_tree.buggy_node.ev_id)
                        else:
                            self.heaviest_first["heaviest_first_buggy_node_returned"].append(None)                 
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()

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
                        self.divide_and_query["divide_and_query_results"].append(divide_and_query.sequence_num)
                        if divide_and_query.exec_tree.buggy_node is not None:
                            self.divide_and_query["divide_and_query_buggy_node_returned"].append(divide_and_query.exec_tree.buggy_node.ev_id)
                        else:
                            self.divide_and_query["divide_and_query_buggy_node_returned"].append(None)
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()



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
                        single_stepping.navigate()
                        print("SingleStepping PROV experiment finished: " +
                                str(single_stepping.sequence_num)+" steps.")
                        logging.info("SingleStepping experiment finished: " +
                                        str(single_stepping.sequence_num)+" steps.")

                        self.single_stepping["single_stepping_prov_results"].append(single_stepping.sequence_num)
                        if single_stepping.exec_tree.buggy_node is not None:
                            self.single_stepping["single_stepping_prov_buggy_node_returned"].append(single_stepping.exec_tree.buggy_node.ev_id)
                        else:
                            self.single_stepping["single_stepping_prov_buggy_node_returned"].append(None)
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()


                    ##################
                    # Top Down
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        top_down = TopDown(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = top_down.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        top_down.navigate()
                        print("TopDown PROV experiment finished: " +
                                str(top_down.sequence_num)+" steps.")
                        logging.info("TopDown experiment finished: " +
                                        str(top_down.sequence_num)+" steps.")
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                        self.top_down["top_down_prov_results"].append(top_down.sequence_num)
                        if top_down.exec_tree.buggy_node is not None:
                            self.top_down["top_down_prov_buggy_node_returned"].append(top_down.exec_tree.buggy_node.ev_id)
                        else:
                            self.top_down["top_down_prov_buggy_node_returned"].append(None)
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()

                    ##################
                    # Heaviest First
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        heaviest_first = HeaviestFirst(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = heaviest_first.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        heaviest_first.navigate()
                        print("HeaviestFirst PROV experiment finished: " +
                                str(heaviest_first.sequence_num)+" steps.")
                        logging.info("HeaviestFirst experiment finished: " +
                                        str(heaviest_first.sequence_num)+" steps.")
                        self.heaviest_first["heaviest_first_prov_results"].append(heaviest_first.sequence_num)
                        if heaviest_first.exec_tree.buggy_node is not None:
                            self.heaviest_first["heaviest_first_prov_buggy_node_returned"].append(heaviest_first.exec_tree.buggy_node.ev_id)
                        else:
                            self.heaviest_first["heaviest_first_prov_buggy_node_returned"].append(None)
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                    except Exception as e:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()

                    ##################
                    # Divide and Query
                    ##################
                    exec_tree = copy.deepcopy(original_exec_tree)
                    try:
                        divide_and_query = DivideAndQuery(exec_tree, True, ANSWER_FILE_PATH)
                        prov = ProvenanceEnhancement(exec_tree, CURSOR)
                        wrong_node_ev = divide_and_query.wrong_node_id
                        prov.enhance(wrong_node_ev)
                        divide_and_query.navigate()
                        print("DivideAndQuery PROV experiment finished: " +
                                str(divide_and_query.sequence_num)+" steps.")
                        logging.info("DivideAndQuery experiment finished: " +
                                        str(divide_and_query.sequence_num)+" steps.")
                        if self.generate_trees:
                            vis = Visualization(exec_tree)
                            vis.view_exec_tree(str(id(exec_tree)))
                        self.divide_and_query["divide_and_query_prov_results"].append(divide_and_query.sequence_num)
                        if divide_and_query.exec_tree.buggy_node is not None:
                            self.divide_and_query["divide_and_query_prov_buggy_node_returned"].append(divide_and_query.exec_tree.buggy_node.ev_id)
                        else:
                            self.divide_and_query["divide_and_query_prov_buggy_node_returned"].append(None)
                    except:
                        print("Exception: {}".format(e))
                        logging.info("Exception: {}".format(e))
                        sys.exit()
        os.chdir('..')
