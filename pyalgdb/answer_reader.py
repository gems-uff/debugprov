import csv
from pyalgdb.validity import Validity

class AnswerReader:

    FILE_NAME = 'aux_files/answers.csv'

    def read_answers(self):
        answers = {}
        myfile = open(self.FILE_NAME)
        with myfile as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    print(row[0])
                    if row[1] == 'valid':
                        answers[int(row[0])] = Validity.VALID
                    elif row[1] == 'invalid':
                        answers[int(row[0])] = Validity.INVALID
                    else:
                        raise Exception('Error reading answer csv file')
                line_count += 1
        print("Processed "+str(line_count)+" lines")
        return answers
