import pickle
from fpdf import FPDF
from LatexFileSummarizer.text_summarizer import TextSummarizer

textSummarizer = TextSummarizer()
# pickle_file_path = r"C:\Users\lenovo\OneDrive - mail.uni-paderborn.de\Documents\Scientific-Papers-Text-Analytics\TextSummaryModels\text_summary_obj.pkl"


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

    def create_pdf_report(self):
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
            pdf.cell(200, 10, txt= summary_name,
                     ln=2, align='C')

            summary = self.text_summary_dict[summary_name]
            pdf.multi_cell(200, 9, txt="".join(summary), align='L')
        # save the pdf
        pdf.output("/data/summary_results.pdf", 'F')


if __name__ == "__main__":
    ai_blog_wiki = """Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the 
    natural intelligence displayed by humans or animals. Leading AI textbooks define the  field as the study of 
    "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of 
    achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic 
    "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving", 
    however this definition is rejected by major AI researchers. AI applications include advanced web search engines 
    (i.e. Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as 
    Siri or Alexa), self-driving cars (e.g. Tesla), and competing at the highest level in strategic game systems (
    such as chess and Go), As machines become increasingly capable, tasks considered to require "intelligence" are 
    often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character 
    recognition is frequently excluded from things considered to be AI, having become a routine technology. """

    text_summary_report = TextSummaryReport(ai_blog_wiki)
    text_summary_report.generate_text_summary()
    text_summary_report.create_pdf_report()
