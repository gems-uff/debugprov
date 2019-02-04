import unittest
import sys

from pyalgdb.dependency_rel import DependencyRel
from pyalgdb.evaluation import Evaluation

class DependencyRelTest(unittest.TestCase):

    def test_dependency_rel(self):    
        influencer = Evaluation(100, 101, 'call', '#name-influencer')
        dependent = Evaluation(200, 201, 'variable', '#name-dependent')
        dep = DependencyRel(influencer, dependent)
        self.assertEqual(dep.influencer, influencer)
        self.assertEqual(dep.dependent, dependent)

if __name__ == '__main__':
    unittest.main()