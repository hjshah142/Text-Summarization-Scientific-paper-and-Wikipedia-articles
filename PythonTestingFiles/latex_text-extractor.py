from Latex_text_Parser import LatexTextParser
file_sample = r"C:\Users\lenovo\Downloads\[PAKDD] Superset-Learning for Algorithm Selection with Right-Censored Data (1)\main.tex"
latex_text_parser = LatexTextParser(file_sample)
section_content_file, abstract_file, section_names_file = latex_text_parser.latex_text_parser()
print("Sections: ", section_names_file)
# print("abstract: ", abstract_file)
file_sample2 = r"C:\Users\lenovo\Downloads\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
latex_text_parser = LatexTextParser(file_sample2)
section_content_file2, abstract_file2, section_names_file2 = latex_text_parser.latex_text_parser()
print("Sections: ", section_names_file2)
# print("abstract: ", abstract_file2)
