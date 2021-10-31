# Text Summarization on scientific research paper datasets and wikipedia articles
Main tasks of this python projects:   
1. Extract text (abstract , content (body)) from the pdf files of research paper using  different python libraries to extract text from the pdf
  
2.  Text summarization on arxiv and pubmed datasets using different extractive and abstractive text summarization algorithms

3.  Text summarization on wikipedia articles using different extractive and abstractive text summarization algorithms 
4.   Text summarization on the latex files of research papers using different extractive and abstractive text summarization algorithms 

- Extracting text from the pdf using following libraries:
    - Apache Tika
    - textract
    - pypdf2
    - pdfminer
    
- Implementation of the following text summarization algorithms:
    - Transfromers library pipeline (default summarizer)
    - XLM Transformers
    - Google Bigbird summarizer with attention mechanism
    - GooglE pegasus xum
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
- Latex files of the research papers in area of computer science

## Scientific Paper Datasets Attributes:
- Two sets of long and structured documents obtained from Open Access repositories.
    -   Article: the body of the document, paragraphs seperated by "/n".
    - 	Abstract: the abstract of the document, paragraphs seperated by "/n".
    -	Section_names: titles of sections, seperated by "/n".
- Abstracts used as ground-truth summaries

Wikipedia Article:
- Wikipedia articles content on Artificial Intelligence, Machine Learning
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://en.wikipedia.org/wiki/Machine_learning


# Text preprocessing 
##  Data: Wikipedia article conent in Computer Science
Preprocessing steps:
- Convert everything to lowercase
- Remove HTML tags
- Contraction mapping
- Remove (‘s)
- Remove any text inside the parenthesis [] ( )
- Elimination of not required punctuations and special characters
## Text  Preprocessing for the latex files
- Remove text containig latex commands
- Remove text inside the parenthesis {}
- Remove any text cointaining equations 
# Evaluation:
- Abstract of scientific papers used as ground-truth summaries
- Evaluation Matrices: ROUGE (metric)
    - ROUGE: Recall-Oriented Understudy for Gisting Evaluation
    -  metrics compare an automatically generated summary or against a ground truth summary (Reference or a set of references or human-produced summary)
     
# References:
- A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents (added in citavi)
- https://www.tensorflow.org/datasets/catalog/scientific_papers#scientific_papersarxiv_default_config
-  https://github.com/armancohan/long-summarization






