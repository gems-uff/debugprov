SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil
import difflib

scripts = ['02-bisection/bisection.py',
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
           '29-string_permutation/stringpermutation.py']

def view_diffs(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        original_file = open(script) 
        original_file_content = original_file.readlines()
        original_file.close()
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            print(os.getcwd())
            print(mutant_dir)
            mutant_file = open("{}.py".format(mutant_dir))
            diff = difflib.ndiff(original_file_content, mutant_file.readlines())
            mutant_file.close()
            for idx,d in enumerate(diff):
                print("{} {}".format(idx,d),end='')
            input()
            os.chdir('..')
        os.chdir('../..')
            
os.chdir(SCRIPTS_DIRECTORY)
view_diffs(scripts)