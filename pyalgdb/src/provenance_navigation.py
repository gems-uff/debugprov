from navgiation_strategy import NavigationStrategy
from node import Node
from code_component import CodeComponent
from dependency_rel import DependencyRel
from validity import Validity
from execution_tree import ExecutionTree

class ProvenanceNavigation(NavigationStrategy):

    def __init__(self, exec_tree: ExecutionTree, cursor):
        super().__init__(root_node)
        self.cursor = cursor
        self.VISITED_CCs = []
        self.DEPENDENCIES =[]

    def ask_wrong_data(self):
        ans = input("Which output data is not correct? ")
        query = ("select CC.name, CC.id, CC.first_char_line "
                 "from evaluation EVAL "
                 "join code_component CC on EVAL.code_component_id = CC.id " 
                 "where EVAL.repr = ? ")
        code_components = []
        print("Select the invalid evaluation")
        i = 1
        for tupl in self.cursor.execute(query, [ans]):
            print(str(i)+". " + str(tupl[0])+ " = " + ans + " at line " + str(tupl[2]))
            i += 1
            code_components.append(tupl)
        invalid_eval = int(input()) - 1
        invalid_cc = code_components[invalid_eval]
        return CodeComponent(invalid_cc[1], invalid_cc[0], "STARTER")
        

    def add_dependency(self, source, target):
        if (source.name != target.name):
                if not self.dependency_exists(source, target):
                    self.DEPENDENCIES.append(DependencyRel(source, target))


    def dependency_exists(self, source, target):
        for d in self.DEPENDENCIES:
                if (d.source.id == source.id and d.target.id == target.id):
                    return True
        return False


    def explore_codecomponent(self, cc):
        if not (int(cc.id) in self.VISITED_CCs):   
                self.VISITED_CCs.append(cc.id)
                influencers = self.find_influencers(cc)
                for i in influencers:
                    if i.typeof == 'call':
                            self.add_dependency(cc,i)
                            self.explore_codecomponent(i)
                    else:
                            func_deps = self.get_func_dependencies_of(i)
                            for f in func_deps:
                                self.add_dependency(cc, f)
                                self.explore_codecomponent(f)
            

    def get_func_dependencies_of(self, cc:CodeComponent):
        func_dependencies = []
        influencers = self.find_influencers(cc)
        for i in influencers:
                if i.typeof == 'call':
                    func_dependencies.append(i)
                else:
                    func_dependencies.extend(self.get_func_dependencies_of(i))
        return func_dependencies

    def find_influencers(self, cc:CodeComponent):
        query_id = ("select CC_INFLU.id, CC_INFLU.name, CC_INFLU.type "
        "from dependency D "
        "join evaluation EV_DEPEND on D.dependent_id = EV_DEPEND.id "
        "join evaluation EV_INFLU on D.dependency_id = EV_INFLU.id "
        "join code_component CC_DEPEND on EV_DEPEND.code_component_id = CC_DEPEND.id "
        "join code_component CC_INFLU on EV_INFLU.code_component_id = CC_INFLU.id "
        "where CC_DEPEND.id = ? "
        " and CC_INFLU.id != ?" )
        influencers = []
        for row in self.cursor.execute(query_id, [cc.id,cc.id]):
                influencers.append(CodeComponent(row[0],row[1],row[2]))
        return influencers

    
    def prune(self):
        for d in self.DEPENDENCIES:
            if d.source.typeof == 'STARTER':
                target_nodes = self.exec_tree.search_for_node_by_ccid(d.target.id)
                for tn in target_nodes:
                    tn.prov = True
            else:
                source_nodes = self.exec_tree.search_for_node_by_ccid(d.source.id)
                target_nodes = self.exec_tree.search_for_node_by_ccid(d.target.id)
                for sn in source_nodes:
                    for tn in target_nodes:
                        sn.prov = True
                        tn.prov = True

    def navigate(self):
        cc_start = self.ask_wrong_data()
        self.explore_codecomponent(cc_start)
        self.prune()
        self.recursive_navigate(self.exec_tree.root_node)
        return self.root_node

    def recursive_navigate(self, node: Node):
        if len(node.childrens) == 1:
            self.recursive_navigate(node.childrens[0])

        # Filtering only the childrens that are in provenance dag
        chds = []
        for n in node.childrens:
            if n.prov == True:
                chds.append(n)

        for n in chds:
            if n.validity is Validity.UNKNOWN:
                n = self.evaluate(n)
            if (n.validity is Validity.INVALID):
                for j in chds:
                    if j.validity is Validity.UNKNOWN:
                        j.validity = Validity.VALID
                # re-apply slicing and pruning (?)
                if (n.has_childrens()):
                    self.recursive_navigate(n)