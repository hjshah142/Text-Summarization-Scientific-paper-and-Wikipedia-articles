import re
# from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode
from pylatexenc.latex2text import LatexNodes2Text




def find_substring(s, start_string, end_string):
    start = s.find(start_string) + len(start_string)
    end = s.find(end_string)
    substring = s[start:end]
    return substring


class LatexTextParser:

    def __init__(self, file_path):

        self.list_sub_section_total_content = None
        self.toc = ""
        self.section_content = dict()
        # self.sub_sections_content = dict()
        self.section_names = []
        self.abstract = None
        self.file_path = file_path
        latex_file_list = open(file_path).readlines()
        latex_file_wo_comments = []
        # removal of comments in the latex files
        for line in latex_file_list:
            if not line.startswith("%"):
                latex_file_wo_comments.append(line)
        self.latex_text_wo_comments = "".join(latex_file_wo_comments)

    def latex_text_pre_processing(self):
        figure_content = re.findall(r'\\begin{figure}(.*?)\\end{figure}', self.latex_text_wo_comments, re.S)
        equation_content = re.findall(r'\\begin{equation}(.*?)\\end{equation}', self.latex_text_wo_comments, re.S)
        table_content = re.findall(r'\\begin{table}(.*?)\\end{table}', self.latex_text_wo_comments, re.S)
        latex_codes = table_content + equation_content + figure_content
        latex_text_cleaned = self.latex_text_wo_comments
        for latex_code in latex_codes:
            latex_text_cleaned = latex_text_cleaned.replace(latex_code, "")
        return latex_text_cleaned

    def latex_extract_abstract_sections(self, latex_text_cleaned):
        self.abstract = re.findall(r'\\begin{abstract}(.*?)\\end{abstract}', latex_text_cleaned, re.S)
        self.section_names = re.findall(r'\\section{(.*?)}', latex_text_cleaned, re.S)
        return self.abstract, self.section_names

    def extract_subsection(self, sections_text):

        sub_section_names = re.findall(r'\\subsection{(.*?)}', sections_text, re.S)
        # print("Subsections:", len(sub_section_names))
        self.toc = self.toc + "Subsections:" + str(len(sub_section_names)) + "\n"
        for subsections in sub_section_names:
            # print("\t", subsections)
            self.toc = self.toc + "\t" + subsections + "\n"
        # if len(sub_section_names) > 0:

        sub_section_content = self.get_subsections_content(sub_section_names, sections_text, )

        # print(sub_section_names)
        return sub_section_content

    def get_sections_abstract_text(self, abstract, section_names, latex_text_cleaned):

        sections_tags = []
        for section in section_names:
            section_tag = "\section{" + section + "}"
            sections_tags.append(section_tag)

        sections_tags.append("\end{document}")
        self.list_sub_section_total_content = []
        for section_index in range(len(sections_tags) - 1):
            sections_text_latex = find_substring(latex_text_cleaned, sections_tags[section_index],
                                                 sections_tags[section_index + 1])
            # print("Section:", section_names[section_index])
            self.toc = self.toc + section_names[section_index] + "\n"

            sub_section_content = self.extract_subsection(sections_text_latex)
            self.list_sub_section_total_content = self.list_sub_section_total_content + sub_section_content
            sections_text = LatexNodes2Text().latex_to_text(sections_text_latex)
            self.section_content[section_names[section_index]] = sections_text

        abstract_text = LatexNodes2Text().latex_to_text("".join(abstract))
        self.section_content['abstract'] = abstract_text
        return self.section_content

    def get_subsections_content(self, sub_section_names, sections_text):
        sub_sections_tags = []
        sub_section_content = []
        for subsection in sub_section_names:
            subsection_tag = "\subsection{" + subsection + "}"
            sub_sections_tags.append(subsection_tag)

        sub_sections_tags.append("\section{")
        # print(sub_sections_tags)
        #
        for sub_section_index in range(0, len(sub_sections_tags) - 1):
            subsections_text_latex = find_substring(sections_text, sub_sections_tags[sub_section_index],
                                                    sub_sections_tags[sub_section_index + 1])
            # print("Section:", section_names[section_index])
            print(subsections_text_latex[0:50])
            # print("sub_section_names[sub_section_index]", sub_section_names[sub_section_index])
            # sub_sections_content[sub_section_names[sub_section_index]] = subsections_text_latex
            sub_section_content.append(subsections_text_latex)
            # self.sub_sections_content.append(subsections_text_latex[0:25])
        # print(sub_sections_content)
        print(sub_section_content)
        return sub_section_content

    def latex_text_parser(self):
        latex_text_cleaned = self.latex_text_pre_processing()
        abstract, section_names = self.latex_extract_abstract_sections(latex_text_cleaned)
        section_content = self.get_sections_abstract_text(abstract, section_names, latex_text_cleaned)
        return section_content, abstract, section_names

# file_path = r"C:\Users\lenovo\Downloads\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
# latexTextParser = LatexTextParser(file_path)
# section_content, abstract, section_names = latexTextParser.latex_text_parser()
# # print(section_content)
# print(latexTextParser.toc)
# print(latexTextParser.sub_sections_content)
# ssd = open(file_path, 'r').read()
# answer = find_substring(ssd, "\subsection{Evaluation Setup}","\subsection{Results}")
# print(answer)
