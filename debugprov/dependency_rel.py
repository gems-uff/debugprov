from debugprov.evaluation import Evaluation

# Defines a dependency relation between two evalautions
class DependencyRel:

      def __init__(self, influencer:Evaluation, dependent:Evaluation):
            self.influencer = influencer
            self.dependent = dependent
      