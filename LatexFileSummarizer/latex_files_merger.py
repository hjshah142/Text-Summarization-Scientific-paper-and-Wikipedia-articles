import re
import os
from pathlib import Path


class LatexFilesMerger:

    def __init__(self, latext_directory_name, main_latex_file_path):
        self.latext_directory_name = latext_directory_name
        self.main_latex_file_path = main_latex_file_path


    def latex_file_read_remove_comment(self, file_path):
        latex_text_list = open(file_path).readlines()
        latex_file_wo_comments = []
        # removal of comments in the latex files
        for line in latex_text_list:
            if not line.startswith("%"):
                latex_file_wo_comments.append(line)
        latex_text_wo_comments = "".join(latex_file_wo_comments)
        return latex_text_wo_comments

    def latex_extract_input_files(self, latex_text_cleaned):
        input_file_names = re.findall(r'\\input{(.*?)}', latex_text_cleaned, re.S)
        return input_file_names

    def create_file_path_content_dir(self, imported_latex_file_names):
        input_files_path_list = []
        input_file_path_content_dir = {}
        for latex_input_files in imported_latex_file_names:
            latex_input_files = os.path.normpath(latex_input_files)
            file_path = os.path.join(self.latext_directory_name, latex_input_files)
            if not file_path.endswith(".tex"):
              file_path = file_path + ".tex"
            input_files_path_list.append(file_path)
            latex_text_wo_comments = self.latex_file_read_remove_comment(file_path)
            input_file_command = "\input{" + latex_input_files + "}"
            input_file_path_content_dir[input_file_command] = latex_text_wo_comments
        return input_file_path_content_dir

    def replace_file_content(self, main_latex_text_wo_comments, input_file_path_content_dir):
        main_latex_file_content_new = main_latex_text_wo_comments
        for import_file in input_file_path_content_dir:
            print(import_file)
            main_latex_file_content_new = main_latex_file_content_new.replace(import_file,
                                                                              input_file_path_content_dir[import_file])
        return main_latex_file_content_new

    def latex_text_walker(self, latex_text_wo_comments):
        input_file_names = self.latex_extract_input_files(latex_text_wo_comments)
        print(len(input_file_names))
        if len(input_file_names) == 0:
            return latex_text_wo_comments
        if len(input_file_names) > 0:
            input_file_path_content_dir = self.create_file_path_content_dir(input_file_names)
            main_latex_file_content_new = self.replace_file_content(latex_text_wo_comments, input_file_path_content_dir)
            # print(main_latex_file_content_new)
            return self.latex_text_walker(main_latex_file_content_new)

    def latex_files_merger(self):
        main_latex_text_wo_comment = self.latex_file_read_remove_comment(self.main_latex_file_path)
        merged_text = self.latex_text_walker(main_latex_text_wo_comment)
        return merged_text
