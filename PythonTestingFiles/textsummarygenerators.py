import torch
import sumy
import gensim
from gensim.summarization import summarize
import nltk
nltk.download('punkt')
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig,BartModel
from transformers import GPT2Tokenizer,GPT2LMHeadModel
from transformers import XLMWithLMHeadModel, XLMTokenizer
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration
# Import the LexRank summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# Importing the parser and tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
# Import the LexRank summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
lex_rank_summarizer = LexRankSummarizer() 
from sumy.summarizers.lsa import LsaSummarizer
lsa_summarizer=LsaSummarizer()
# Parsing the text string using PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser



class TextSummarizer:
  def __init__(self):
    # Instantiating the model and tokenizer with gpt-2 and bart and XLM
    self.tokenizer_bart_large = BartTokenizer.from_pretrained('facebook/bart-large')
    self.model_bart_large = BartModel.from_pretrained('facebook/bart-large')
    self.tokenizer_gpt2=GPT2Tokenizer.from_pretrained('gpt2')
    self.model_gpt2=GPT2LMHeadModel.from_pretrained('gpt2')
    self.tokenizer_bart=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    self.model_bart=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    # Instantiating the model and tokenizer xlm 
    self.tokenizer_XLM=XLMTokenizer.from_pretrained('xlm-mlm-en-2048')
    self.model_XLM=XLMWithLMHeadModel.from_pretrained('xlm-mlm-en-2048')
    self.model_t5 = T5ForConditionalGeneration.from_pretrained('t5-small')
    self.tokenizer_t5 = T5Tokenizer.from_pretrained('t5-small')
    self.tokenizer_list = [self.tokenizer_gpt2,self.tokenizer_bart, self.tokenizer_XLM]
    self.model_list = [self.model_gpt2,self.model_bart, self.model_XLM]

  def text_summarizer(self, text):
    text_summary_list =[]
    for models in range(len(self.model_list)):
      print('summarization using ' ,  self.model_list[models].name_or_path)
      
      if  self.model_list[models].name_or_path == "xlm-mlm-en-2048":
        # print('true')
        text = text[0:2500]

      inputs=self.tokenizer_list[models](text, return_tensors='pt' )
      summary_ids=self.model_list[models].generate(inputs['input_ids'], early_stopping=True, min_length = 15, max_length= 20)
      text_summary= self.tokenizer_list[models].batch_decode(summary_ids)
      text_summary_list.append(text_summary)
      print(text_summary)
    # Concatenating the word "summarize:" to raw text
    t5_text = "summarize:" + text
    # encoding the input text
    input_ids=self.tokenizer_t5.encode(t5_text, return_tensors='pt', truncation=True)
    summary_ids = self.model_t5.generate(input_ids,early_stopping=True, min_length = 15, max_length= 20)
    t5_summary = self.tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)
    text_summary_list.append(t5_summary)
    summary_genensim = summarize(text)
    text_summary_list.append(summary_genensim)
    my_parser = PlaintextParser.from_string(text,Tokenizer('english'))
    lexrank_summary_sentences = lex_rank_summarizer(my_parser.document,sentences_count=3)
    lexrank_summary = ""
    for sentence in lexrank_summary_sentences:
      lexrank_summary= lexrank_summary + " "+ str(sentence)
    text_summary_list.append(lexrank_summary)

    # creating the lsa summarizer

    parser=PlaintextParser.from_string(text,Tokenizer('english'))
    lsa_summary_sentences= lsa_summarizer(parser.document,3)
    lsa_summary =""
    # Printing the summary
    for sentence in lsa_summary_sentences:
        lsa_summary= lsa_summary+" "+ str(sentence)
    text_summary_list.append(lsa_summary)
    
    return text_summary_list



