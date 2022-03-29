import re
# from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode
# from pylatexenc.latex2text import LatexNodes2Text


def find_substring(s, start_string, end_string):
    start = s.find(start_string) + len(start_string)
    end = s.find(end_string)
    substring = s[start:end]
    return substring


def find_list_subsection_content(s, start_string):
    substring = s.split(start_string, 1)[1]
    return substring


class LatexTextParser:

    def __init__(self, latex_file_path):
        """
        Class removes the latex comment, performs the preprocessing of latex files,
        extract abstract, toc, sections and subsections from the latex files
        :param latex_file_path: path of a latex file
        """
        self.title = ""
        self.sub_sections_dict = dict()
        self.toc = ""
        self.section_content = dict()
        self.list_subsections_content = None
        # self.sub_sections_content = dict()
        self.latex_metadata = dict()
        self.section_names = []
        self.abstract = ""
        self.file_path = latex_file_path
        self.toc_dict = dict()
        latex_file_list = open(latex_file_path).readlines()
        latex_file_wo_comments = []
        # removal of comments in the latex files
        for line in latex_file_list:
            if not line.startswith("%"):
                latex_file_wo_comments.append(line)
        self.latex_text_wo_comments = "".join(latex_file_wo_comments)


    def latex_text_pre_processing(self):
        figure_content = re.findall(r'\\begin{figure}(.*?)\\end{figure}', self.latex_text_wo_comments, re.S)
        self.latex_metadata['Figures'] = len(figure_content)
        equation_content = re.findall(r'\\begin{equation}(.*?)\\end{equation}', self.latex_text_wo_comments, re.S)
        self.latex_metadata['Equations'] = len(equation_content)
        table_content = re.findall(r'\\begin{table}(.*?)\\end{table}', self.latex_text_wo_comments, re.S)
        self.latex_metadata['Tables'] = len(table_content)
        latex_codes = table_content + equation_content + figure_content
        latex_text_cleaned = self.latex_text_wo_comments
        for latex_code in latex_codes:
            latex_text_cleaned = latex_text_cleaned.replace(latex_code, "")
        return latex_text_cleaned

    def latex_extract_abstract_sections(self, latex_text_cleaned):
        abstract = re.findall(r'\\begin{abstract}(.*?)\\end{abstract}', latex_text_cleaned, re.S)
        self.section_names = re.findall(r'\\section{(.*?)}', latex_text_cleaned, re.S)
        abstract_text = abstract[0]
        # self.abstract = LatexNodes2Text().latex_to_text(abstract_text)
        self.abstract = abstract_text
        title = re.findall(r'\\title{(.*?)}', latex_text_cleaned, re.S)
        self.title = " ".join(title)
        print(self.title)
        return self.abstract, self.section_names

    def get_sections_text(self, section_names, latex_text_cleaned):

        sections_tags = []
        for section in section_names:
            section_tag = "\section{" + section + "}"
            sections_tags.append(section_tag)

        sections_tags.append("\end{document}")
        self.list_subsections_content = []

        for section_index in range(len(sections_tags) - 1):
            sections_text_latex = find_substring(latex_text_cleaned, sections_tags[section_index],
                                                 sections_tags[section_index + 1])
            # print("Section:", section_names[section_index])
            section_title = section_names[section_index]
            self.toc = self.toc + str(section_index+1) +". " + section_title + "\n"

            sub_section_names, sub_section_content = self.extract_subsection(sections_text_latex)
            self.latex_metadata[section_title] = sub_section_names
            self.sub_sections_dict[section_title] = sub_section_content
            self.list_subsections_content = self.list_subsections_content + sub_section_content
            # sections_text = LatexNodes2Text().latex_to_text(sections_text_latex)
            # abstract_text = sections_text_latex
            self.section_content[section_names[section_index]] = sections_text_latex

        # self.section_content['abstract'] = abstract_text
        return self.section_content

    def extract_subsection(self, sections_text):

        sub_section_names = re.findall(r'\\subsection{(.*?)}', sections_text, re.S)

        # print("Subsections:", len(sub_section_names))
        # self.toc = self.toc + "Subsections:" + str(len(sub_section_names)) + "\n"
        for index, subsections in enumerate(sub_section_names):
            # print("\t", subsections)
            self.toc = self.toc + "      " + "\t" + str(index+1)+". " + subsections + "\n"
        sub_section_content = []
        if len(sub_section_names) > 0:
            sub_section_content = self.get_subsections_content(sub_section_names, sections_text, )

        # print(sub_section_names)
        return sub_section_names, sub_section_content

    def get_subsections_content(self, sub_section_names, sections_text):
        sub_sections_tags = []
        sub_section_content = []
        for subsection in sub_section_names:
            subsection_tag = "\subsection{" + subsection + "}"
            sub_sections_tags.append(subsection_tag)

        # sub_sections_tags.append("\section{")
        # print(sub_sections_tags)
        #
        for sub_section_index in range(0, len(sub_sections_tags) - 1):
            subsections_text_latex = find_substring(sections_text, sub_sections_tags[sub_section_index],
                                                    sub_sections_tags[sub_section_index + 1])
            # print("Section:", section_names[section_index])
            # print(subsections_text_latex[0:50])
            # print("sub_section_names[sub_section_index]", sub_section_names[sub_section_index])
            sub_section_content.append(subsections_text_latex)

            # self.sub_sections_content.append(subsections_text_latex[0:25])

        last_sub_section_text = find_list_subsection_content(sections_text, sub_sections_tags[-1])
        sub_section_content.append(last_sub_section_text)
        # print(last_sub_section_text)
        self.get_subsubsections(sub_section_content)
        return sub_section_content

    def get_subsubsections(self, sub_section_content):
        sub_sub_section_content_tex = " ".join(sub_section_content)
        sub_sub_section_names = re.findall(r'\\subsubsection{(.*?)}', sub_sub_section_content_tex, re.S)
        if len(sub_sub_section_names) > 0:
            for ind, subsubsection in enumerate(sub_sub_section_names):
                print("\t\t subsections:", subsubsection)
                self.toc = self.toc + "          "+ "\t"+ "\t" + str(ind+1) +". "+ subsubsection + "\n"
        return sub_sub_section_names

    def latex_text_parser(self):
        latex_text_cleaned = self.latex_text_pre_processing()
        abstract, section_names = self.latex_extract_abstract_sections(latex_text_cleaned)
        sections_content = self.get_sections_text(section_names, latex_text_cleaned)
        return abstract, section_names, sections_content


# file_path = r"..\..\latex_papers\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
# latexTextParser = LatexTextParser(file_path)
# section_content_file, abstract_file, section_names_file = latexTextParser.latex_text_parser()
# print(latexTextParser.toc)


