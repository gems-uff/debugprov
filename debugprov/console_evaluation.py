from debugprov.node import Node
from prompt_toolkit.shortcuts import confirm

class ConsoleEvaluation:

    def evaluate_node(node: Node):
        print("-------------------------")
        print("Evaluating node {} {}".format(str(node.ev_id),node.name))
        # print("Name: {}".format(node.name))
        # print("Evaluation_id: {}".format(node.ev_id))
        # print("Code_component_id: {}".format(node.code_component_id))
        print("Parameters: name | value ")
        for p in node.params:
            print (" {} | {} ".format(p.name, p.value))
        print("Returns: {}".format(node.retrn))
        answer = confirm('Is correct? ')
        return answer
