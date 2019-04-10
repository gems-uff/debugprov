import json
import sqlite3
import os

from debugprov.provenance_enhancement import ProvenanceEnhancement
from debugprov.divide_and_query import DivideAndQuery
from debugprov.single_stepping import SingleStepping
from debugprov.visualization import Visualization
from debugprov.heaviest_first import HeaviestFirst
from debugprov.top_down import TopDown
from debugprov.execution_tree_creator import ExecTreeCreator
from debugprov.execution_tree import ExecutionTree
from debugprov.node import Node
from debugprov.validity import Validity
from graphviz import Graph

SCRIPTS_DIRECTORY = 'scripts'

os.chdir(SCRIPTS_DIRECTORY)

scripts = ['20-permute']

def discover_changed_lines(filename):
    mutant = open(filename)
    content = mutant.readlines()
    mutant.close()
    line_count = 0
    for line in content:
        line_count += 1
        if line.startswith('+'):
            return line_count
        elif line.startswith('-'):
            return line_count
    raise Exception("It was not possible to process this mutant diff")

def get_faulty_cc_id(faulty_line, cursor):
    query_1 = ("select CC.id "
               "from code_component CC "
               "where CC.type='function_def' "
               "and CC.first_char_line <= ? "
               "and CC.last_char_line >= ? ")

    cursor.execute(query_1, [faulty_line, faulty_line])
    result = cursor.fetchall()
    if len(result) != 1:
        raise Exception("More than one code_component associated with faulty line. Faulty line: "+str(faulty_line))

    for tupl in cursor.execute(query_1, [faulty_line, faulty_line]):
        name = tupl[0]

    query_2 = ("select e.code_component_id from activation a "
               "natural join evaluation e "
               "where a.code_block_id = ? ")

    cursor.execute(query_2, [name])
    result = cursor.fetchall()
    if len(result) != 1:
        raise Exception("More than one activation associated with code_component_id. code_component_id: "+str(name))

    for tupl in cursor.execute(query_2, [name]):
        return tupl[0]


def invalidate_node_and_parents(node):
    while(node.parent is not None):
        node.validity = Validity.INVALID
        node = node.parent

def format_answers(exec_tree,node_with_wrong_data):
    invalid_nodes = []
    node_list = exec_tree.get_all_nodes()
    for n in node_list:
        if n.validity == Validity.INVALID:
            invalid_nodes.append(n.ev_id)
    obj = {
        "invalid_nodes": list(set(invalid_nodes)),
        "node_with_wrong_data": node_with_wrong_data
    }
    return obj

def get_node_with_wrong_data(mutant_dir,cursor):
    query = ("select e.id from evaluation e "
             "join code_component cc on e.code_component_id = cc.id "
             "where cc.name like '%print%' and cc.type='call' "
             "order by cc.first_char_line DESC "
             "LIMIT 1 ")
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        raise Exception("Could not find print node")
    for tupl in cursor.execute(query):
        return tupl[0]

def process_mutant(mutant_dir):
    os.chdir(mutant_dir)
    print(os.getcwd())
    FAULTY_LINE = discover_changed_lines(mutant_dir+".diff")
    now2_sqlite_path = os.getcwd() + '/.noworkflow/db.sqlite'
    cursor = sqlite3.connect(now2_sqlite_path).cursor()
    exec_tree = ExecTreeCreator(cursor).create_exec_tree()
    exec_tree.root_node.validity = Validity.INVALID
    faulty_code_component_id = get_faulty_cc_id(FAULTY_LINE, cursor)
    search_result = exec_tree.search_by_ccid(faulty_code_component_id)

    if len(search_result) != 1:
        raise Exception("More than one node in ET associated with faulty code_component_id. CC id: " +
             str(faulty_code_component_id))

    buggy_node = search_result.pop()
    invalidate_node_and_parents(buggy_node)
    node_with_wrong_data = get_node_with_wrong_data(mutant_dir, cursor)
    ansfile = open('oracle.json','w')
    ansfile.write(json.dumps(format_answers(exec_tree,node_with_wrong_data)))
    ansfile.close()
    print('saving oracle.json file: '+os.getcwd()+'/oracle.json')
    vis = Visualization(exec_tree)
    vis.generate_exec_tree()
    vis.graph.render(filename='exec_tree',format='pdf')
    os.chdir('..')


def generate_answerfile(scripts):
    for script_path in scripts:
        directory = script_path
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            try:
                process_mutant(mutant_dir)
            except Exception as e:
                print("Error in "+mutant_dir)
                print(e)
                os.chdir('..')
        os.chdir('../..')

generate_answerfile(scripts)