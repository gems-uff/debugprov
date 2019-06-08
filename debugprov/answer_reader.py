import json
from debugprov.validity import Validity

class AnswerReader:

    def __init__(self, file_name):
        self.file_name = file_name

    def read_answers(self):
        with open(self.file_name) as json_data:
            data = json.load(json_data)
        answer_dict = {}
        node_with_wrong_data_id = int(data['node_with_wrong_data'])
        invalid_nodes = list(data['invalid_nodes'])
        obj = {
            "invalid_nodes": invalid_nodes,
            "node_with_wrong_data_id": node_with_wrong_data_id
        }
        return obj
