SCRIPTS_DIRECTORY = 'scripts'
NOWORKFLOW_DIR = '.noworkflow'
PY_CACHE_DIR = '__pycache__'
MUTANTS_SUBDIR = 'mutants'
TIMEOUT_LIMIT = 30

import os
import subprocess
import shutil

scripts = ['01-compression_analysis/psnr.py',
           '02-bisection/bisection.py',
           '03-intersection/intersection.py',
           '04-lu_decomposition/lu_decomposition.py',
           '05-newton_method/newton_method.py',
           '06-md5/hashmd5.py',
           '07-basic_binary_tree/basic_binary_tree.py',
           '08-edit_distance/edit_distance.py',
           '09-dijkstra_algorithm/dijkstra_algorithm.py',
           '10-caesar_cipher/caesar_cipher.py',
           '11-brute_force_caesar_cipher/brute_force_caesar_cipher.py',
           '12-basic_maths/basic_maths.py',
           '13-merge_sort/merge_sort.py',
           '14-rsa_cipher/rsa_cipher.py',
           '15-decision_tree/decision_tree.py',
           '16-math_parser/math_parser.py',
           '17-merge_intervals/merge_intervals.py'
           '19-binary_search/binary_search.py',
           '21-longest_common_subsequence/lcs.py',
           '24-bubblesort/bubblesort.py',
           '25-quicksort/quicksort.py',
           '27-generate_parenthesis/generate_parenthesis.py']

def run_scripts(scripts,save_log=False):
    for script_path in scripts:
        c += 1
        print("$ python "+script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        try:
            os.chdir(directory)
            proc = subprocess.Popen(['python',script], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            print(stdout.decode('utf-8'))
            if save_log:
                logfile = open(script+'.log','w') 
                logfile.write(stdout.decode('utf-8'))
                logfile.close()
            os.chdir('..')
        except:
            print("#### "+script)
            print('#### something went very very wrong')
            os.chdir('..')
    
os.chdir(SCRIPTS_DIRECTORY)
run_scripts(scripts,True)