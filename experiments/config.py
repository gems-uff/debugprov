import os

class Config:

    def __init__(self):
        self.all_mutants_dir = 'mutants.all'
        self.running_mutants_dir = 'mutants.running'
        self.mutants_with_wrong_result = 'mutants.wrong_result'

    def all_scripts(self):
        return ['01-compression_analysis/psnr.py',
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
                '27-generate_parenthesis/generate_parenthesis.py',
                '28-knn/knn.py',
                '29-string_permutation/stringpermutation.py',
                '30-linear_regression/demo.py',
                '31-bfs/bfs.py']

    @property
    def target_scripts(self):
        return ['31-bfs/bfs.py']

    # ../../debugprov-experimentdata/scripts
    def go_to_scripts_path(self):
        self.current_path = os.getcwd()
        os.chdir('..')
        os.chdir('..')
        os.chdir('debugprov-experimentdata')
        os.chdir('scripts')
        

    def go_back_to_current_path(self):
        os.chdir(self.current_path)