import csv
import json
from debugprov.validity import Validity

class AnswerReader:

    def __init__(self, file_name):
        self.file_name = file_name

    
    def read_answers(self):
        with open(self.file_name) as json_data:
            data = json.load(json_data)
        answer_dict = {}
        wrong_node_id = int(data['wrong_node_id'])
        for ans in data['answers']:
            for k,v in ans.items():
                key = int(k)
                value = None
                if v == 'valid':
                    value = Validity.VALID
                elif v == 'invalid':
                    value = Validity.INVALID
                if value is None:
                    raise Exception('Error parsing JSON file')
                else:
                    answer_dict[key] = value
        obj = {
            "answer_dict": answer_dict,
            "wrong_node_id": wrong_node_id
        }
        return obj

