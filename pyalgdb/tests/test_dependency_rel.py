import unittest
import sys

from pyalgdb.dependency_rel import DependencyRel
from pyalgdb.code_component import CodeComponent

class DependencyRelTest(unittest.TestCase):

    def test_dependency_rel(self):    
        one_cc = CodeComponent(100, "100#code_component_name", "100#code_component_typeof")
        other_cc = CodeComponent(200, "200#code_component_name", "200#code_component_typeof")
        dep = DependencyRel(one_cc, other_cc)
        self.assertEqual(dep.source, one_cc)
        self.assertEqual(dep.target, other_cc)

if __name__ == '__main__':
    unittest.main()