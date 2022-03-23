from text_summary_report import TextSummaryReport
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
