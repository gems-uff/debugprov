import sys
import os
import subprocess

SCRIPTS_DIRECTORY = 'scripts'
MUTANTS_SUBDIR = 'mutants'

os.chdir(SCRIPTS_DIRECTORY)

scripts = ['04-lu_decomposition/lu_decomposition.py']

def generate_mutants(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        try:
            os.chdir(directory)
            print(os.getcwd())
            print("mutate {} --mutantDir mutants.all".format(script))
            proc = subprocess.Popen("mutate {} --mutantDir mutants.all".format(script), cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            print(stdout.decode('utf-8'))
            logfile = open('mutant_generation.log','w') 
            logfile.write(stdout.decode('utf-8'))
            logfile.close()
        except:
            print("#### "+script)
            print('#### something went very very wrong')
        os.chdir('..')

if (sys.version_info > (3, 0)): # IF PYTHON 3
    print("RUN THIS WITH PYTHON 2.7")
    sys.exit()
else: # PYTHON 2
    print("UNIVERSALMUTATOR HAVE TO BE INSTALLED")
    ans = raw_input("TYPE OK TO RUN \n")
    if ans == 'ok':
        generate_mutants(scripts)