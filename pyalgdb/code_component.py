class CodeComponent:

      def __init__(self, id, name, typeof):
            self.id = id
            self.name = name
            self.typeof = typeof
      
      def __repr__(self):
            return "{} {} {}".format(str(self.id), self.name, self.typeof)