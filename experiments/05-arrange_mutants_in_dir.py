SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

directories = ['02-bisection',
           '03-intersection',
           '04-lu_decomposition',
           '05-newton_method',
           '06-md5',
           '07-basic_binary_tree',
           '08-edit_distance',
           '09-dijkstra_algorithm',
           '10-caesar_cipher',
           '11-brute_force_caesar_cipher',
           '12-basic_maths',
           '13-merge_sort',
           '15-decision_tree',
           '16-math_parser',
           '17-merge_intervals',
           '18-graph_find_path',
           '19-binary_search',
           '20-permute',
           '21-longest_common_subsequence',
           '22-catalan',
           '23-longest_increasing_subsequence',
           '24-bubblesort',
           '25-quicksort',
           '26-heapsort',
           '28-knn',
           '29-string_permutation']

def run_mutants(directories):
    for directory in directories:
        print(directory)
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for py_file in os.listdir():
            if py_file.endswith('.py'):
                dir_name = py_file[:-3]
                os.mkdir(dir_name)
                cwd = os.getcwd()
                shutil.move("{}/{}".format(cwd,py_file), "{}/{}/{}".format(cwd,dir_name,py_file))
                print("{}/{}".format(cwd,py_file) + ' -> ' + "{}/{}/{}".format(cwd,dir_name,py_file))
                logfile = "{}{}".format(py_file,'.log')
                shutil.move("{}/{}".format(cwd,logfile), "{}/{}/{}".format(cwd,dir_name,logfile))
                print("{}/{}".format(cwd,logfile) + ' -> ' + "{}/{}/{}".format(cwd,dir_name,logfile))
        os.chdir('../..')
os.chdir(SCRIPTS_DIRECTORY)
run_mutants(directories)