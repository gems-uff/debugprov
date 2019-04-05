from debugprov.evaluation import Evaluation

# Defines a dependency relation between two evalautions
class DependencyRel:

      def __init__(self, source:Evaluation, target:Evaluation):
            self.source = source
            self.target = target
      