import logging
from datetime import datetime
from debugprov.node import Node

class NavigationLogger:

    def __init__(self):
        file_name = datetime.now().strftime('experiment_logs/%Y_%m_%d %H-%M-%S.%f.log')
        self.file = open(file_name,'w') 
        #logging.basicConfig(filename=datetime.now().strftime('logs/%Y_%m_%d %H-%M-%S.log'),
        #level=logging.INFO,
        #format='%(asctime)s %(message)s')
    
    def log(self, message):
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
        self.file.write(time_str + message + "\n")

    def log_node(self, node, sequence_num):
        seq_num = " {} ".format(str(sequence_num))
        self.log(seq_num + "-------------------------")
        self.log(seq_num + "Evaluating node {}".format(node.name))
        self.log(seq_num + "Name: {}".format(node.name))
        self.log(seq_num + "Evaluation_id: {}".format(node.ev_id))
        self.log(seq_num + "Code_component_id: {}".format(node.code_component_id))
        self.log(seq_num + "Parameters: name | value ")
        for p in node.params:
            self.log(seq_num + " {} | {} ".format(p.name, p.value))
        self.log(seq_num + "Returns: {}".format(node.retrn))