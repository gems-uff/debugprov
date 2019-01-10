from code_component import CodeComponent

class DependencyRel:

      def __init__(self, source:CodeComponent, target:CodeComponent):
            self.source = source
            self.target = target
      
      def to_csv(self):
            return ("{},{},{},{},{},{}".format(self.source.id,self.source.name,self.source.typeof,
            self.target.id,self.target.name,self.target.typeof))

      def to_graphviz(self):
            source_name = self.source.name.replace("\"", "")
            target_name = self.target.name.replace("\"", "")
            return ("\"{}\" -> \"{}\"".format(source_name,target_name))
