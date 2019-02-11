import unittest

from debugprov.answer_reader import AnswerReader
from debugprov.validity import Validity

class AnswerReaderTest(unittest.TestCase):

    FILE_NAME = 'aux_files/age-avg-answers.json'
    WRONG_NODE_ID = 280
    INVALID_NODES = [1,20,262,265]

    def test_answer_reader(self):
        ans_reader = AnswerReader(self.FILE_NAME)
        self.assertEqual(ans_reader.file_name, self.FILE_NAME)
        
    def test_read_answers(self):
        ans_reader = AnswerReader(self.FILE_NAME)
        data = ans_reader.read_answers()
        self.assertEqual(data['wrong_node_id'],self.WRONG_NODE_ID)
        answers = data['answer_dict']
        for key in answers:
            value = answers[key]
            if key in self.INVALID_NODES:
                self.assertEqual(value,Validity.INVALID)
            else:
                self.assertEqual(value,Validity.VALID)

if __name__ == '__main__':
    unittest.main()