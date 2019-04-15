import sys
import os
import subprocess
from config import Config

config = Config()

def generate_mutants(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        try:
            os.chdir(directory)
            os.mkdir(config.all_mutants_dir)
            print("mutate {} --mutantDir {}".format(script,config.all_mutants_dir))
            proc = subprocess.Popen("mutate {} --mutantDir {}".format(script,config.all_mutants_dir), cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        config.go_to_scripts_path()
        generate_mutants(config.target_scripts)
        config.go_back_to_current_path()