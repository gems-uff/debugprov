import os
import difflib

SCRIPTS_DIRECTORY = 'scripts'

os.chdir(SCRIPTS_DIRECTORY)

scripts = [
           '02-bisection/bisection.py',
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
           '29-string_permutation/stringpermutation.py'
        ]

def process_inline_diff(oneline,otherline,outputfile):
    oneline = oneline.rstrip()
    otherline = otherline.rstrip()
    outputfile.write('{} ==> {}\n\n'.format(oneline,otherline))
    for i,s in enumerate(difflib.ndiff(oneline,otherline)):
        if s[0]==' ': continue
        elif s[0]=='-':
            outputfile.write('Delete "{}" from position {}\n'.format(s[-1],i))
        elif s[0]=='+':
            outputfile.write('Add "{}" to position {}\n'.format(s[-1],i))

def generate_aboutdiff(scripts):
    for script_path in scripts:
        print(script_path)
        directory = script_path.split('/')[0]
        script = script_path.split('/')[1]
        os.chdir(directory)
        os.chdir('mutants.wrong_result')
        for mutant_dir in os.listdir():
            os.chdir(mutant_dir)
            print(os.getcwd())
            diff_file = open("{}.diff".format(mutant_dir))
            diff_file_content = diff_file.readlines()
            diff_file.close()
            removes = 0
            insertions = 0
            count = 0
            for line in diff_file_content:
                if line.startswith('+'):
                    first_insertion = count
                    insertions += 1
                elif line.startswith('-'):
                    first_removal = count
                    removes += 1
                count += 1
            if removes == 1 and insertions == 1:
                aboutdiff = open('about-diff.txt','w')
                aboutdiff.write("line {}\n".format(str(first_removal+1)))
                rm_line = diff_file_content[first_removal].replace('-',' ',1)
                add_line = diff_file_content[first_insertion].replace('+',' ',1)
                process_inline_diff(rm_line, add_line, aboutdiff)
                aboutdiff.close()
                print('generated about-diff.txt file')
            elif removes == 0 and insertions == 1:
                aboutdiff = open('about-diff.txt','w')
                aboutdiff.write("line {}\n".format(str(first_removal+1)))
                aboutdiff.write(" ==> {}".format(diff_file_content[first_insertion].rstrip().replace('+',' ',1)))
                aboutdiff.close()
                print('generated about-diff.txt file')
            else:
                print('It was not possible to process this mutant diff')
            os.chdir('..')
        os.chdir('../..')

generate_aboutdiff(scripts)