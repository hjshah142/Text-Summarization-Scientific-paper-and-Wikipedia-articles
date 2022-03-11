import torch
import sumy
import gensim
from gensim.summarization import summarize
import nltk
import re
nltk.download('punkt')
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig,BartModel
from transformers import GPT2Tokenizer,GPT2LMHeadModel
from transformers import XLMWithLMHeadModel, XLMTokenizer
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration
from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from bs4 import BeautifulSoup 
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
  """ Class Text Summarizer: Class return the text summarisation performed on given text  using diffferent different state-of-the-art text summmarizer """
  def __init__(self):
    # Instantiating the model and tokenizer with gpt-2 and bart
    self.tokenizer_gpt2=GPT2Tokenizer.from_pretrained('gpt2')
    self.model_gpt2=GPT2LMHeadModel.from_pretrained('gpt2')
    # Instantiating baer model 
    self.tokenizer_bart=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    self.model_bart=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    # Instantiating the model and tokenizer t5
    self.model_t5 = T5ForConditionalGeneration.from_pretrained('t5-small')
    self.tokenizer_t5 = T5Tokenizer.from_pretrained('t5-small')
    # Instantiating the model and tokenizer google_bigbird
    self.model_BigBird = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv", attention_type="original_full")
    self.tokenizer_BigBird = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")
    # by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
    
    self.tokenizer_Pegasus = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
    self.model_Pegasus = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')


  def text_summarizer(self, text):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    text_summary_list = []
    text_summary_dict = {}

    text_summary_dict['_text_'] = text
    # Encoding the inputs and passing them to model.generate()
    inputs = self.tokenizer_bart.batch_encode_plus([text],return_tensors='pt')
    summary_ids = self.model_bart.generate(inputs['input_ids'], early_stopping=True,min_length = 50, max_length=75)
    bart_summary = self.tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)
    print(bart_summary)
    text_summary_list.append(bart_summary)
    text_summary_dict['bart_summary'] = bart_summary

    inputs = self.tokenizer_BigBird(text, return_tensors='pt')
    summary_ids = self.model_BigBird.generate(**inputs,min_length=50, max_length=75)
    summary_BigBird = self.tokenizer_BigBird.batch_decode(summary_ids, skip_special_tokens=True)
    text_summary_list.append(summary_BigBird)
    text_summary_dict['summary_BigBird'] = summary_BigBird
    print(summary_BigBird)
    
    # GPL Summary
    inputs=self.tokenizer_gpt2.batch_encode_plus([text],return_tensors='pt',max_length=512)
    summary_ids=self.model_gpt2.generate(inputs['input_ids'],early_stopping=True)
    GPT_summary=self.tokenizer_gpt2.decode(summary_ids[0],skip_special_tokens=True)
    # print(GPT_summary)
    text_summary_list.append(GPT_summary)
    text_summary_dict['gpt_summary'] = GPT_summary
    # Concatenating the word "summarize:" to raw text
    # google pegasus summarization
    inputs = self.tokenizer_Pegasus([text], truncation=True, padding='longest', return_tensors="pt")
    summary_ids = self.model_Pegasus.generate(inputs['input_ids'], min_length=50, max_length=75)
    summary_google_pegasus = self.tokenizer_Pegasus.batch_decode(summary_ids, skip_special_tokens=True)
    text_summary_list.append(summary_google_pegasus)
    text_summary_dict['summary_google_pegasus'] = summary_google_pegasus
    
    t5_text = "summarize:" + text
    # encoding the input text
    input_ids=self.tokenizer_t5.encode(t5_text, return_tensors='pt')
    summary_ids = self.model_t5.generate(input_ids,early_stopping=True, min_length = 50, max_length=75)
    t5_summary = self.tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)
    text_summary_list.append(t5_summary)
    text_summary_dict['t5_summary'] = t5_summary
    # gensim_summary
    summary_genensim = summarize(text)
    text_summary_dict['gensim_summary'] = summary_genensim
    text_summary_list.append(summary_genensim)
    my_parser = PlaintextParser.from_string(text,Tokenizer('english'))
    lexrank_summary_sentences = lex_rank_summarizer(my_parser.document,sentences_count=3)
    lexrank_summary = ""
    for sentence in lexrank_summary_sentences:
      lexrank_summary= lexrank_summary + " "+ str(sentence)
    text_summary_list.append(lexrank_summary)
    text_summary_dict['lexrank_summary'] = lexrank_summary
    # creating the lsa summarizer
    parser=PlaintextParser.from_string(text,Tokenizer('english'))
    lsa_summary_sentences= lsa_summarizer(parser.document,3)
    lsa_summary =""
    #  lsa summary
    for sentence in lsa_summary_sentences:
        lsa_summary= lsa_summary+" "+ str(sentence)
    text_summary_list.append(lsa_summary)
    text_summary_dict['lsa_summary'] = lsa_summary
    return text_summary_list, text_summary_dict

def clean_latext_content(text):
  """ Preprocessing for the text summarizer for sceintific research articles in .tex file"""
  clean_text = re.sub(r'\{[^)]*\}', '', text)
  clean_text2 = clean_text.replace("\cite", "").replace("\n","").replace("\ref", "").replace("\textit","").replace('\\',"")
  return clean_text2