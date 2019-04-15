import os
import subprocess
from config import Config

config = Config()

config.go_to_scripts_path()

def run_scripts(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        print(os.getcwd())
        try:
            os.chdir(directory)
            proc = subprocess.Popen(['python',script], cwd=os.getcwd(), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            print(stdout.decode('utf-8'))
            logfile = open(script+'.log','w') 
            logfile.write(stdout.decode('utf-8'))
            logfile.close()
        except:
            print('#### something went wrong: ')
            print("#### "+script)
        os.chdir('..')

run_scripts(config.target_scripts)
config.go_back_to_current_path()