from debugprov.trial import Trial
from debugprov.node import Node

import sqlite3

class NowStorageInterface:

    GET_TRIALS_QUERY = ("SELECT * FROM TRIAL ")

    GET_ROOT_NODE_QUERY = ("select EV.id, CC.id, EV.repr, CC.name "
                      "from evaluation EV "
                      "natural join activation ACT "
                      "join code_component CC on EV.code_component_id = CC.id "
                      "where activation_id = 0 "
                      "and EV.trial_id = ?")

    def __init__(self):
        self.conn = None
        self.trial_id = None

    def connect(self,path):
        self.conn = sqlite3.connect(path)

    def get_trials(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(self.GET_TRIALS_QUERY)
            results = cursor.fetchall()
            trials = []
            for row in results:
                trials.append(Trial(row[0],row[1],row[2],row[3],row[4],row[5]))
            return trials

    def get_root_node(self) -> Node:
        if self.conn is not None and self.trial_id is not None:
            cursor = self.conn.cursor()

            cursor.execute(self.GET_ROOT_NODE_QUERY, self.trial_id)
            result = cursor.fetchall()
            if len(result) != 1:
                raise ValueError(
                    "ValueError: Something wrong in database. {} root nodes found".format(len(result)))

            for tupl in cursor.execute(query, [0]):
                root = Node(tupl[0], tupl[1], tupl[2], tupl[3], None)
                return root
        else:
            if self.conn is None:
                raise Exception('Exception: Database connection (conn) must be defined in get_root_node')
            elif self.trial_id is None:
                raise Exception('Exception: trial_id must be defined in get_root_node')