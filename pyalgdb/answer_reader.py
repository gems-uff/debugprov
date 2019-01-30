import csv
from pyalgdb.validity import Validity

class AnswerReader:

    def __init__(self, answer_file = 'aux_files/answers.csv'):
        self.file_name = answer_file

    def read_answers(self):
        answers = {}
        myfile = open(self.file_name)
        with myfile as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    if row[1] == 'valid':
                        answers[int(row[0])] = Validity.VALID
                    elif row[1] == 'invalid':
                        answers[int(row[0])] = Validity.INVALID
                    else:
                        raise Exception('Error reading answer csv file')
                line_count += 1
        myfile.close()
        return answers
