import os
import subprocess
import shutil

from config import Config

config = Config()
config.go_to_scripts_path()

os.chdir('..')
os.chdir('excel_processing')
os.mkdir('excel_files')
os.chdir('excel_files')

dest = os.getcwd()

os.chdir('../..')
os.chdir('scripts')

def arrange_mutants(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
        print(directory)
        os.chdir(directory)
        cwd = os.getcwd()
        os.rename('output.xlsx',"{}.xlsx".format(directory))
        shutil.move("{}/{}.xlsx".format(cwd,directory), dest)
        os.chdir('..')

arrange_mutants(config.target_scripts)