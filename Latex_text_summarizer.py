import re
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode
from pylatexenc.latex2text import LatexNodes2Text


def latex_text_pre_processing(latex_text_wo_comments):
    figure_content = re.findall(r'\\begin{figure}(.*?)\\end{figure}', latex_text_wo_comments, re.S)
    equation_content = re.findall(r'\\begin{equation}(.*?)\\end{equation}', latex_text_wo_comments, re.S)
    table_content = re.findall(r'\\begin{table}(.*?)\\end{table}', latex_text_wo_comments, re.S)
    latex_codes = table_content + equation_content + figure_content
    latex_text_cleaned = latex_text_wo_comments
    for latex_code in latex_codes:
        latex_text_cleaned = latex_text_cleaned.replace(latex_code, "")
    return latex_text_cleaned


def latex_extract_abstract_sections(latex_text_cleaned):
    abstract = re.findall(r'\\begin{abstract}(.*?)\\end{abstract}', latex_text_cleaned, re.S)
    section_names = re.findall(r'\\section{(.*?)}', latex_text_cleaned, re.S)
    return abstract, section_names


def find_substring(s, start_string, end_string):
    start = s.find(start_string) + len(start_string)
    end = s.find(end_string)
    substring = s[start:end]
    return substring


def get_sections_abstract_text(abstract, section_names, latex_text_cleaned):
    section_content = dict()
    sections_tags = []
    for section in section_names:
        section_tag = "\section{" + section + "}"
        sections_tags.append(section_tag)

    sections_tags.append("\end{document}")

    for section_index in range(len(sections_tags) - 1):
        sections_text_latex = find_substring(latex_text_cleaned, sections_tags[section_index],
                                             sections_tags[section_index + 1])
        sections_text = LatexNodes2Text().latex_to_text(sections_text_latex)
        section_content[section_names[section_index]] = sections_text

    abstract_text = LatexNodes2Text().latex_to_text("".join(abstract))
    section_content['abstract'] = abstract_text
    return section_content


class LatexTextSummarizer:

    def __init__(self, file_path):
        self.file_path = file_path
        latex_file_list = open(file_path).readlines()
        latex_file_wo_comments = []
        for line in latex_file_list:
            if not line.startswith("%"):
                latex_file_wo_comments.append(line)
        latex_text_wo_comments = "".join(latex_file_wo_comments)
        latex_text_cleaned = latex_text_pre_processing(latex_text_wo_comments)
        self.abstract, self.section_names = latex_extract_abstract_sections(latex_text_cleaned)
        self.section_content = get_sections_abstract_text(self.abstract, self.section_names, latex_text_cleaned)


file_sample = r"C:\Users\lenovo\Downloads\[PAKDD] Superset-Learning for Algorithm Selection with Right-Censored Data (1)\main.tex"
latex_text_summarizer = LatexTextSummarizer(file_sample)
print(latex_text_summarizer.section_content)
# print section names
print("Section", latex_text_summarizer.section_names)

file_sample2 = r"C:\Users\lenovo\Downloads\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
latex_text_summarizer = LatexTextSummarizer(file_sample2)
print(latex_text_summarizer.section_content)
# print sections
print("Section", latex_text_summarizer.section_names)


