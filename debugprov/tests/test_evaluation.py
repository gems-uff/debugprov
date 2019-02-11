import unittest

from debugprov.evaluation import Evaluation

class EvaluationTest(unittest.TestCase):

    def test_evaluation(self):
        evaluation_id = 300
        code_component_id = 301
        code_component_typeof = "300#CodeComponentTypeof"
        code_component_name = "300#CodeComponentName"
        evl = Evaluation(evaluation_id, code_component_id, code_component_typeof,code_component_name)
        
        self.assertEqual(evl.ev_id, evaluation_id)
        self.assertEqual(evl.code_component_id, code_component_id)
        self.assertEqual(evl.code_component_type, code_component_typeof)
        self.assertEqual(evl.code_component_name, code_component_name)

        
if __name__ == '__main__':
    unittest.main()