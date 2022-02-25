from LatexFileSummarizer import *
from LatexFileSummarizer.text_summarizer import TextSummarizer
from LatexFileSummarizer.latex_files_merger import LatexFilesMerger
from LatexFileSummarizer.latex_text_parser import LatexTextParser


def merge_latex_files(latex_dir_name, main_latex_file_path, merged_file_path):
    latex_file_merger = LatexFilesMerger(latex_dir_name, main_latex_file_path)
    merged_text_content = latex_file_merger.latex_files_merger()
    try:
        with open(merged_file_path, "w") as f:
            print("Merged File", merged_file_path, "created !!!")
            f.write(merged_text_content)
    except FileNotFoundError:
        print("The directory does not exist/accecible")

    return merged_text_content



latex_dir_name = r"C:\Users\lenovo\Downloads\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss"
main_file_path = r"C:\Users\lenovo\Downloads\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
latext_directory_name = "/content/drive/MyDrive/latex_papers/2105.08215"
merged_file_path = "latex_sample_merged.tex"
merged_text_content = merge_latex_files(latex_dir_name, main_file_path, merged_file_path)
latex_parser = LatexTextParser(merged_file_path)
section_content, abstract, section_names = latex_parser.latex_text_parser()
print(section_names)
# print(abstract)


textSummarizer = TextSummarizer()
ai_blog_wiki = """
Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans or animals. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving", however this definition is rejected by major AI researchers. AI applications include advanced web search engines (i.e. Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri or Alexa), self-driving cars (e.g. Tesla), and competing at the highest level in strategic game systems (such as chess and Go), As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
"""
text_summary_dict = textSummarizer.text_summarizer(ai_blog_wiki)



# creating pdf report
from transformers.models import auto
from fpdf import FPDF

# save FPDF() class into a  variable pdf
pdf = FPDF()
# pdf.set_auto_page_break(auto=True)
# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size=10)

pdf.cell(200, 10, txt="Text:",
         ln=2, align='L')
pdf.multi_cell(200, 10, txt=ai_blog_wiki,
               align='L')

# create a cell
pdf.cell(200, 10, txt="Summary", ln=1, align='C')

for summary_name in text_summary_dict:
    pdf.cell(200, 10, txt=summary_name,
             ln=2, align='C')

    summary = text_summary_dict[summary_name]
    pdf.multi_cell(200, 9, txt="".join(summary), align='L')

# add another cell


# save the pdf with name .pdf
pdf.output("/content/summary_results.pdf", 'F')




