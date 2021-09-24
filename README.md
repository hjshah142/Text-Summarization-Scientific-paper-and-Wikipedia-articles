# Text Summarization on scientific datasets and wikipedia articles
Main tasks of this python projects:   
1. Extract text (abstract , content (body)) from the pdf files of research paper using  different python libraries to extract text from the pdf
  
2.  Text summarization on arxiv and pubmed datasets using different extractive and abstractive text summarization algorithms

3.  Text summarization on wikipedia articles using different extractive and abstractive text summarization algorithms 

- Extracting text from the pdf using following libraries:
    - Apache Tika
    - textract
    - pypdf2
    - pdfminer
    
- Implementation of the following text summarization algorithms:
    Transfromers library pipeline (default)
    - XLM Transformers
    - GPT-2 Transformers
    - Gensim with TextRank
    - Text Rank Algorithm
    - LexRank Algorithm
    - LSA (Latent semantic analysis) algorithm
    - Abstractive Summarizations with t5 transformers
    - BART transformers



# Datasets:
- Scientific Paper Datasets:

    1.	ArXiv 
    2.	PubMed Dataset 

- Wikipedia Article

## Scientific Paper Datasets Attributes:
- Two sets of long and structured documents obtained from Open Access repositories.
    -   Article: the body of the document, paragraphs seperated by "/n".
    - 	Abstract: the abstract of the document, paragraphs seperated by "/n".
    -	Section_names: titles of sections, seperated by "/n".
- Abstracts used as ground-truth summaries

Wikipedia Article:
- Wikipedia articles content on Artificial Intelligence
- https://en.wikipedia.org/wiki/Artificial_intelligence
# Evaluation:
- Abstract of scientific papers used as ground-truth summaries
- Evaluation Matrices: ROUGE (metric)
    - ROUGE: Recall-Oriented Understudy for Gisting Evaluation
    -  metrics compare an automatically generated summary or against a ground truth summary (Reference or a set of references or human-produced summary)
     
# References:
- A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents (added in citavi)
- https://www.tensorflow.org/datasets/catalog/scientific_papers#scientific_papersarxiv_default_config
-  https://github.com/armancohan/long-summarization






