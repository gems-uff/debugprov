from navgiation_strategy import NavigationStrategy

class TopDown(NavigationStrategy):

    def navigate(self, exec_tree):
        chds = exec_tree.childrens
        for node in chds:
            nd = self.evaluate(node)
            if (nd.validity is True):
                print("Nothing to do here, just go to next node.. ->>")
            else:
                self.navigate(nd)
