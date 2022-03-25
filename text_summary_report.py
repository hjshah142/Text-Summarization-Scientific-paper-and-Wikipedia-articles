import pickle
from fpdf import FPDF
from LatexFileSummarizer.text_summarizer import TextSummarizer
textSummarizer = TextSummarizer()
pickle_file_path = r"..\TextSummaryModels\text_summary_obj.pkl"


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
# save_object(textSummarizer, pickle_file_path)
# pickle_file_object = open(pickle_file_path, 'rb')
# textSummarizer = pickle.load(pickle_file_object)


class TextSummaryReport:
    def __init__(self, summary_text):
        self.text_summary_dict = dict()
        self.summary_text = summary_text

    def generate_text_summary(self):
        self.text_summary_dict = textSummarizer.text_summarizer(self.summary_text)
        return self.text_summary_dict

    def create_pdf_report(self, pdf_file_path):
        # save FPDF() class into a  variable pdf
        pdf = FPDF()
        # pdf.set_auto_page_break(auto=True)
        # Add a page
        pdf.add_page()
        # set style and size of font in the pdf
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Text:",
                 ln=2, align='L')
        pdf.multi_cell(200, 10, txt=self.summary_text,
                       align='L')
        # create a cell
        pdf.cell(200, 10, txt="Summary", ln=1, align='C')

        for summary_name in self.text_summary_dict:
            pdf.cell(200, 10, txt=summary_name,
                     ln=2, align='C')

            summary = self.text_summary_dict[summary_name]
            pdf.multi_cell(200, 9, txt="".join(summary), align='L')
        # save the pdf

        pdf.output(pdf_file_path, 'F')

