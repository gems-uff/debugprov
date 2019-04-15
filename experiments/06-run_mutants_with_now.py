import os
import subprocess
import shutil
from config import Config

TIMEOUT_LIMIT = 90

config = Config()
config.go_to_scripts_path()


def run_mutants_with_now(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
        print(directory)
        os.chdir(directory)
        os.chdir(config.mutants_with_wrong_result)
        for content in os.listdir():
            os.chdir(content)
            for py_file in os.listdir():
                if py_file.endswith('.py'):
                    print(os.getcwd())
                    print("now run {}".format(py_file))
                    proc = subprocess.Popen(['now', 'run', py_file], cwd=os.getcwd(
                    ), env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    try:
                        stdout, stderr = proc.communicate(
                            timeout=TIMEOUT_LIMIT)
                        returncode = proc.returncode
                        if returncode == 0:
                            print("Success running {}".format(py_file))
                        else:
                            print(stderr)
                            import sys
                            sys.exit("Something wrong happened...")
                        proc.kill()
                    except:
                        proc.kill()
                        import sys
                        sys.exit("EXCEPT Something wrong happened...")
            os.chdir('..')
        os.chdir('../..')

run_mutants_with_now(config.target_scripts)