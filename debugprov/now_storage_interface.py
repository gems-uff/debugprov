from debugprov.trial import Trial

import sqlite3

class NowStorageInterface:

    GET_TRIALS_QUERY = ("SELECT * FROM TRIAL ")

    def __init__(self):
        self.conn = None

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
