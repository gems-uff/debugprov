import unittest

from pyalgdb.code_component import CodeComponent

class CodeComponentTest(unittest.TestCase):

    def test_code_component(self):
        code_component_id = 300
        code_component_name = "300#CodeComponentName"
        code_component_typeof = "300#CodeComponentTypeof"
        cc = CodeComponent(code_component_id, code_component_name, code_component_typeof)
        self.assertEqual(cc.id, code_component_id)
        self.assertEqual(cc.name, code_component_name)
        self.assertEqual(cc.typeof, code_component_typeof)

if __name__ == '__main__':
    unittest.main()