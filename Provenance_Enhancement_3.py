#!/usr/bin/env python
# coding: utf-8

# ### The following cells presents an execution tree enhanced with provenance.
# ### In this view, the wrong Evaluation is asked, and the provenance DAG is built based on the slice of the wrong evaluation. 

# In[1]:


# Imports
import sqlite3

from graphviz import Graph

from debugprov.validity import Validity
from debugprov.node import Node
from debugprov.execution_tree import ExecutionTree
from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.top_down import TopDown
from debugprov.heaviest_first import HeaviestFirst
from debugprov.visualization import Visualization
from debugprov.provenance_enhancement import ProvenanceEnhancement 
from debugprov.single_stepping import SingleStepping
from debugprov.divide_and_query import DivideAndQuery


# In[2]:


class CustomVisualization(Visualization):

    # CUSTOM ATTRIBUTES
    PROVENANCE_NODE_COLOR = 'lightblue'
    
    def generate_exec_tree(self, graph_name = 'exec_tree'):
        file_name = "{}.gv".format(graph_name)
        self.graph = Graph(graph_name, filename=file_name)
        self.graph.attr('node', shape='box')
        self.graph.attr('graph', ordering='out')
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.ev_id), root_node.get_name(), fillcolor=self.INVALID_COLOR, style='filled') # root node
        self.navigate(root_node)
        eval_node = self.exec_tree.node_under_evaluation
        if eval_node is not None:
            self.graph.node(str(eval_node.ev_id), str(eval_node.get_name()), fillcolor=self.NODE_IN_EVALUATION, style='filled')
        buggy_node = self.exec_tree.buggy_node
        if buggy_node is not None:
            self.graph.node(str(buggy_node.ev_id), str(buggy_node.get_name()), fillcolor=self.BUGGY_NODE_COLOR, style='filled')
        if self.exec_tree.dependencies is not None:
            count = 0
            for d in self.exec_tree.dependencies: # this loop draws the provenance links between nodes
                count += 1
                print(" # {} ".format(count),end='')
                self.graph.edge(str(d.dependent.ev_id), str(d.influencer.ev_id), None, color=self.PROVENANCE_EDGE_COLOR, dir='forward')
                ## BEGIN customization
                self.graph.node(str(d.dependent.ev_id), None, fillcolor=self.PROVENANCE_NODE_COLOR, style='filled')
                self.graph.node(str(d.influencer.ev_id), None, fillcolor=self.PROVENANCE_NODE_COLOR, style='filled')
                ## END customization
    
    


# In[3]:


NOW2_SQLITE_PATH = 'experiments/selected_mutants/bisection.mutant.124/.noworkflow/db.sqlite'


# In[4]:


CURSOR = sqlite3.connect(NOW2_SQLITE_PATH).cursor()


# In[5]:


creator = ExecTreeCreator(CURSOR)
exec_tree = creator.create_exec_tree()


# In[6]:


prov = ProvenanceEnhancement(exec_tree, CURSOR)


# In[7]:


wrong_data = prov.ask_wrong_data()


# In[8]:


wrong_data


# In[9]:


prov.enhance(wrong_data)


# In[ ]:


len(exec_tree.dependencies)


# In[ ]:


vis = Visualization(prov.exec_tree)


# In[ ]:


vis.view_exec_tree('exec_tree_p3')


# In[ ]:


######################################################################################################################


# In[ ]:




