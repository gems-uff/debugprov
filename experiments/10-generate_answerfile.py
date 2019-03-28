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
import pickle
import json
import sqlite3
import shutil
import subprocess
import os
SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30


scripts = [
     '02-bisection/bisection.py',
     '03-intersection/intersection.py',
     '04-lu_decomposition/lu_decomposition.py',
     '05-newton_method/newton_method.py',
     '06-md5/hashmd5.py',
     '07-basic_binary_tree/basic_binary_tree.py',
     '08-edit_distance/edit_distance.py',
     '09-dijkstra_algorithm/dijkstra_algorithm.py',
     '11-brute_force_caesar_cipher/brute_force_caesar_cipher.py',
     '12-basic_maths/basic_maths.py',
     '13-merge_sort/merge_sort.py',
     '15-decision_tree/decision_tree.py',
     '16-math_parser/math_parser.py',
     '17-merge_intervals/merge_intervals.py',
     '18-graph_find_path/find_path.py',
     '19-binary_search/binary_search.py',
     '20-permute/permute.py',
     '21-longest_common_subsequence/lcs.py',
     '22-catalan/catalan.py',
     '23-longest_increasing_subsequence/lis.py',
     '24-bubblesort/bubblesort.py',
     '25-quicksort/quicksort.py',
     '26-heapsort/heapsort.py',
     '28-knn/knn.py',
     '29-string_permutation/stringpermutation.py'
]


def discover_changed_lines(filename):
    mutant = open(filename)
    content = mutant.readlines()
    mutant.close()
    removes = 0
    insertions = 0
    count = 0
    for line in content:
        count += 1
        if line.startswith('+'):
            first_insertion = count
            insertions += 1
        elif line.startswith('-'):
            first_removal = count
            removes += 1
    if removes == 1 and insertions == 1:
        return first_removal
    elif removes == 0 and insertions == 1:
        return first_insertion
    else:
        raise Exception('It was not possible to process this mutant diff')

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

    print(name)

    query_2 = ("select e.code_component_id from activation a "
               "natural join evaluation e "
               "where a.code_block_id = ? ")

    cursor.execute(query_2, [name])
    result = cursor.fetchall()
    if len(result) != 1:
        raise Exception("More than one activation associated with code_component_id. code_component_id: "+str(name))

    for tupl in cursor.execute(query_2, [name]):
        print(tupl[0])
        return tupl[0]


def invalidate_node_and_parents(node):
    while(node.parent is not None):
        node.validity = Validity.INVALID
        node = node.parent


def format_answers(exec_tree):
    answers = []
    node_list = exec_tree.get_all_nodes()
    for n in node_list:
        if n.validity == Validity.INVALID:
            node_validity = 'invalid'
        else:
            node_validity = 'valid'
            obj = {
                str(n.ev_id): node_validity 
            }
        #answers[n.ev_id] = node_validity
        answers.append(obj)
    return_obj = {
        "wrong_node_id": "$FILL",
        "answers": answers
    }
    return return_obj


def process_mutant(mutant_dir):
    os.chdir(mutant_dir)
    print(os.getcwd())
    FAULTY_LINE = discover_changed_lines(mutant_dir+".diff")
    now2_sqlite_path = os.getcwd() + '/.noworkflow/db.sqlite'
    cursor = sqlite3.connect(now2_sqlite_path).cursor()
    exec_tree = ExecTreeCreator(cursor).create_exec_tree()
    exec_tree.root_node.validity = Validity.INVALID
    faulty_code_component_id = get_faulty_cc_id(FAULTY_LINE, cursor)
    #print('faulty code_component_id: ' + str(faulty_code_component_id))
    search_result = exec_tree.search_by_ccid(faulty_code_component_id)

    if len(search_result) != 1:
        raise Exception("More than one node in ET associated with faulty code_component_id. CC id: " +
             str(faulty_code_component_id))

    buggy_node = search_result.pop()
    invalidate_node_and_parents(buggy_node)
    ansfile = open('answers.json','w')
    ansfile.write(json.dumps(format_answers(exec_tree)))
    ansfile.close()
    print('saving answerfile: '+os.getcwd()+'/answers.json')
    os.chdir('..')


def generate_answerfile(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
        # script = script_path.split('/')[1]
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


os.chdir(SCRIPTS_DIRECTORY)
generate_answerfile(scripts)
