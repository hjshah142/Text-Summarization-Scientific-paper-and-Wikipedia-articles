import pickle
import re
from fpdf import FPDF
from LatexFileSummarizer.latex_files_merger import LatexFilesMerger
from LatexFileSummarizer.latex_text_parser import LatexTextParser
from LatexFileSummarizer.text_summarizer import TextSummarizer

textSummarizer = TextSummarizer()


pickle_file_path = r"..\TextSummaryModels\text_summary_obj.pkl"
pickle_file_object = open(pickle_file_path, 'rb')
# textSummarizer = pickle.load(pickle_file_object)
pdf = FPDF(orientation='P', unit='mm', format='A4')


def preprocessing_text(text):
    clean_text = re.sub('"', '', text)
    clean_text = re.sub("\n", "", clean_text)
    clean_text = re.sub(r"'s\b", "", clean_text)
    return clean_text


class LatexFileSummaryReport:

    def __init__(self, latex_directory_name, main_latex_file_path):

        self.latex_parser_obj = None
        self.abstract = ""
        self.section_names = []
        self.sections_content = dict()
        self.sections_summary_dictionary = dict()
        self.latex_directory_name = latex_directory_name
        self.main_latex_file_path = main_latex_file_path

    def merge_latex_files(self, merged_file_path):
        latex_file_merger = LatexFilesMerger(self.latex_directory_name, self.main_latex_file_path)
        merged_latext_text = latex_file_merger.latex_files_merger()
        try:
            with open(merged_file_path, "w") as f:
                print("Merged File", merged_file_path, "created !!!")
                f.write(merged_latext_text)
        except FileNotFoundError:
            print("The directory does not exist or accessible")

        return merged_latext_text

    def extract_latex_metadata(self, merged_file_path):

        self.latex_parser_obj = LatexTextParser(merged_file_path)
        self.abstract, self.section_names, self.sections_content = self.latex_parser_obj.latex_text_parser()
        return self.abstract, self.section_names, self.sections_content, self.latex_parser_obj

    def generate_sections_summary(self, abstract, sections_content):
        self.sections_summary_dictionary = {}
        abstract_summary = textSummarizer.text_summarizer(abstract)
        # print(abstract_summary)
        for sections in sections_content:
            print(sections)
            # text_summary_dict = sections_content[sections][0:500]
            text_summary_dict = textSummarizer.text_summarizer(sections_content[sections][0:1000])

            self.sections_summary_dictionary[sections] = text_summary_dict

        abstract_summary = textSummarizer.text_summarizer(abstract)
        print(abstract_summary)
        self.sections_summary_dictionary['abstract'] = abstract_summary

        return self.sections_summary_dictionary

    def create_pdf_report_latex_files(self, abstract_text, sections_summary_dict, table_of_content, pdf_file_path):

        # save the pdf
        pdf.set_auto_page_break(auto=True)
        # pdf.set_doc_option('core_fonts_encoding', 'utf-8')
        # Add a page
        # pdf.normalize_text("")
        pdf.add_page()
        # set style and size of font
        pdf.set_font('helvetica', '', 10)
        pdf.cell(180, 7, txt="Text Summary Report:", align='C', ln=True, border=True)
        # abstract = "".join(abstract)
        abstract_cleaned = preprocessing_text(abstract_text)
        # abstract_cleaned = abstract_cleaned.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(180, 7, txt="Abstract:",
                 ln=True, align='L')
        print(abstract_text)
        pdf.multi_cell(180, 7, txt=abstract_cleaned, align='L')

        pdf.cell(180, 7, txt="Table of Contents", align='C', ln=True, border=True)
        print(table_of_content)
        pdf.multi_cell(180, 7, txt=table_of_content, align='L')
        # # create a cell
        # pdf.cell(200, 10, txt="Summary:", ln=1, align='C')

        for section in sections_summary_dict:
            print(section)
            pdf.cell(180, 7, txt=section,
                     align='L', ln=True, border=True)

            for summary_name in sections_summary_dict[section]:
                # print(summary_name)
                pdf.cell(180, 7, txt=summary_name,
                         ln=True, align='C', border=True)

                summary = sections_summary_dict[section][summary_name]
                summary = "".join(summary)
                summary = preprocessing_text(summary)
                # summary = summary.encode('latin-1', 'replace').decode('latin-1')

                # summary.encode('cp1252')
                pdf.multi_cell(180, 7, txt=summary, align='L')

            # save the pdf with name .pdf
        pdf.output(pdf_file_path, 'F')


if __name__ == '__main__':
    merged_latex_file_path = "latex_sample_merged.tex"
    latex_dir_name = r"..\latex_papers\2001.06776"
    latex_file_path = r"..\latex_papers\2001.06776\Krishnamurthy20.tex"
    pdf_file_path = r"Data\latex_summary_result.pdf"
    latex_summary_report = LatexFileSummaryReport(latex_dir_name, latex_file_path)
    merged_text_content = latex_summary_report.merge_latex_files(merged_latex_file_path)
    abstract, section_names, sections_content, latex_parser = latex_summary_report.extract_latex_metadata(
        merged_latex_file_path)
    sections_summary_dict = latex_summary_report.generate_sections_summary(abstract, sections_content)
    latex_summary_report.create_pdf_report_latex_files(abstract, sections_summary_dict, latex_parser.toc, pdf_file_path)
