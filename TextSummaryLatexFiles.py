import pickle
import re
from LatexFileSummarizer.latex_files_merger import LatexFilesMerger
from LatexFileSummarizer.latex_text_parser import LatexTextParser
# from LatexFileSummarizer.text_summarizer import TextSummarizer
# textSummarizer = TextSummarizer()
from fpdf import FPDF

# save FPDF() class into a  variable pdf
# latex_dir_name = r"C:\Users\lenovo\OneDrive\latex_papers\thesis"
# latex_dir_name = "/content/drive/MyDrive/thesis"
# main_file_path = r"C:\Users\lenovo\OneDrive\latex_papers\thesis\thesis.tex"
#
merged_file_path = "latex_sample_merged.tex"
latex_directory_name = r"C:\Users\lenovo\OneDrive\latex_papers\2001.06776"
latex_file_path = r"C:\Users\lenovo\OneDrive\latex_papers\2001.06776\Krishnamurthy20.tex"
pickle_file_path = r"..\TextSummaryModels\text_summary_obj.pkl"
pdf_file_path = r"Data\latex_summary_result.pdf"


def merge_latex_files(latex_dir_name, main_latex_file_path, merged_file_path):
    latex_file_merger = LatexFilesMerger(latex_dir_name, main_latex_file_path)
    merged_text_content = latex_file_merger.latex_files_merger()
    try:
        with open(merged_file_path, "w") as f:
            print("Merged File", merged_file_path, "created !!!")
            f.write(merged_text_content)
    except FileNotFoundError:
        print("The directory does not exist or accessible")

    return merged_text_content


def preprocessing_text(text):
    # lower_text = text.lower()
    # removing html tags
    # clean_text = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in clean_text.split(" ")])
    # clean_text = re.sub("[\(\[].*?[\)\]]", "", clean_text)
    clean_text = re.sub('"', '', text)
    clean_text = re.sub("\n", "", clean_text)
    clean_text = re.sub(r"'s\b", "", clean_text)
    return clean_text


def create_pdf_report(abstract_text, sections_summary_dict, table_of_content,  pdf_file_path):
    pdf = FPDF()
    # save the pdf
    pdf.set_auto_page_break(auto=True)
    # pdf.set_doc_option('core_fonts_encoding', 'utf-8')
    # Add a page
    # pdf.normalize_text("")
    pdf.add_page()
    # set style and size of font
    # pdf.add_font('Arial', '', 'Arial.ttf', True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 9, txt="Text Summary Report:", align='C')
    pdf.cell(200, 9, txt="Abstract", align='L')
    # abstract = "".join(abstract)
    abstract_cleaned = preprocessing_text(abstract_text)
    # abstract_cleaned = abstract_cleaned.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(200, 9, txt=abstract_cleaned, align='L')
    pdf.add_page()
    pdf.cell(200, 9, txt="Table of Contents", align='L')
    print(table_of_content)
    pdf.cell(200, 9, txt=table_of_content, align='C')
    # # create a cell
    # pdf.cell(200, 10, txt="Summary:", ln=1, align='C')

    for section in sections_summary_dict:
        # print(sections)
        pdf.cell(200, 9, txt=section,
                 align='L')

        for summary_name in sections_summary_dict[section]:
            print(summary_name)
            pdf.cell(200, 9, txt=summary_name,
                     ln=1, align='C')

            summary = sections_summary_dict[section][summary_name]
            summary = "".join(summary)
            summary = preprocessing_text(summary)
            summary = summary.encode('latin-1', 'replace').decode('latin-1')
            summary = preprocessing_text(summary)

            # summary.encode('cp1252')
            pdf.multi_cell(200, 9, txt=summary, align='L')

        # save the pdf with name .pdf
    pdf.output(pdf_file_path, 'F')


merged_text_content = merge_latex_files(latex_directory_name, latex_file_path, merged_file_path)
latex_parser = LatexTextParser(merged_file_path)
abstract, section_names, sections_content = latex_parser.latex_text_parser()
# # print(latex_parser.list_subsections__content)
print(type(latex_parser.toc))
# print(len(latex_parser.list_subsections__content))
pickle_file_object = open(pickle_file_path, 'rb')
textSummarizer = pickle.load(pickle_file_object)

sections_summary_dictionary = {}

# for sections in sections_content:
#     print(sections)
#     # text_summary_dict = sections_content[sections][0:500]
#     text_summary_dict = textSummarizer.text_summarizer(sections_content[sections][0:500])
#
#     sections_summary_dictionary[sections] = text_summary_dict

abstract_summary = textSummarizer.text_summarizer(abstract)
print(abstract_summary)
sections_summary_dictionary['abstract'] = abstract_summary
# print(sections_summary_dict)
create_pdf_report(abstract, sections_summary_dictionary, latex_parser.toc, pdf_file_path)
