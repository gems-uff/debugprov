import os
import difflib

SCRIPTS_DIRECTORY = 'scripts'
os.chdir(SCRIPTS_DIRECTORY)

programs = ['08-edit_distance']

def view_diffs(scripts):
    for script_path in scripts:
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        original_file = open(script) 
        original_file_content = original_file.readlines()
        original_file.close()
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            mutant_file = open("{}.py".format(mutant_dir))
            diff = difflib.ndiff(original_file_content, mutant_file.readlines())
            mutant_file.close()
            diff_file = open(mutant_dir+'.diff','w')
            for idx,d in enumerate(diff):
                diff_file.write(d,)
            diff_file.close()
            os.chdir('..')
        os.chdir('../..')
            
store_diffs(programs)