from code_component import CodeComponent

# Defines a dependency relation between two code components
class DependencyRel:

      def __init__(self, source:CodeComponent, target:CodeComponent):
            self.source = source
            self.target = target
      