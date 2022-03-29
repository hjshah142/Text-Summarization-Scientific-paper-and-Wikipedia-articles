from summary_latex_file_report import LatexFileSummaryReport
merged_latex_file_path = "latex_sample_merged.tex"
# latex_dir_name = r"..\latex_papers\2001.06776"
latex_dir_name = r"..\latex_papers\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss"
# r"..\..\latex_papers\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex
latex_file_path = r"..\latex_papers\[KI] Hybrid Loss for Algorithm Selection_ Regression and Ranking Loss\main.tex"
pdf_file_path = r"Data\latex_summary_result.pdf"
latex_summary_report = LatexFileSummaryReport(latex_dir_name, latex_file_path)
merged_text_content = latex_summary_report.merge_latex_files(merged_latex_file_path)
abstract, section_names, sections_content, latex_parser = latex_summary_report.extract_latex_metadata(
    merged_latex_file_path)
sections_summary_dict = latex_summary_report.generate_sections_summary(abstract, sections_content)
latex_summary_report.create_pdf_report_latex_files(abstract, sections_summary_dict, latex_parser.toc, pdf_file_path)
