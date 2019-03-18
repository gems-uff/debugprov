SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

scripts = ['02-bisection/bisection.py.log',
           '03-intersection/intersection.py.log',
           '04-lu_decomposition/lu_decomposition.py.log',
           '05-newton_method/newton_method.py.log',
           '06-md5/hashmd5.py.log',
           '07-basic_binary_tree/basic_binary_tree.py.log',
           '08-edit_distance/edit_distance.py.log',
           '09-dijkstra_algorithm/dijkstra_algorithm.py.log',
           '10-caesar_cipher/caesar_cipher.py.log',
           '11-brute_force_caesar_cipher/brute_force_caesar_cipher.py.log',
           '12-basic_maths/basic_maths.py.log',
           '13-merge_sort/merge_sort.py.log',
           '15-decision_tree/decision_tree.py.log',
           '16-math_parser/math_parser.py.log',
           '17-merge_intervals/merge_intervals.py.log',
           '18-graph_find_path/find_path.py.log',
           '19-binary_search/binary_search.py.log',
           '20-permute/permute.py.log',
           '21-longest_common_subsequence/lcs.py.log',
           '22-catalan/catalan.py.log',
           '23-longest_increasing_subsequence/lis.py.log',
           '24-bubblesort/bubblesort.py.log',
           '25-quicksort/quicksort.py.log',
           '26-heapsort/heapsort.py.log',
           '28-knn/knn.py.log',
           '29-string_permutation/stringpermutation.py.log']

def run_mutants(scripts):
    for script_path in scripts:
        muts_with_correct_results = []
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        original_log_file = open(script) 
        original_result = original_log_file.read()
        original_log_file.close()
        os.chdir('mutants.wrong_result')
        for a_file in os.listdir():
            if a_file.endswith('.log'):
                logfile = open(a_file,'r')
                content = logfile.read()
                logfile.close()
                if content == original_result:
                    muts_with_correct_results.append(a_file)
        print('len muts_with_correct_results ')
        print(len(muts_with_correct_results))
        for mut in muts_with_correct_results:
            os.remove(mut[:-4])
            os.remove(mut)
        os.chdir('../..')
        muts_with_correct_results = []
        print()

os.chdir(SCRIPTS_DIRECTORY)
run_mutants(scripts)