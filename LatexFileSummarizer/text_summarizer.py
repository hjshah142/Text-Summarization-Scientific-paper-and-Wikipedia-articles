import torch
import sumy
import gensim
from gensim.summarization import summarize
import nltk
import re

nltk.download('punkt')
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig, BartModel
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

lsa_summarizer = LsaSummarizer()
# Parsing the text string using PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser


class TextSummarizer:
    def __init__(self):
        # Instantiating the model and tokenizer bart
        self.tokenizer_bart = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model_bart = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        # Instantiating the model and tokenizer t5
        self.model_t5 = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer_t5 = T5Tokenizer.from_pretrained('t5-small')
        # Instantiating the model and tokenizer google_bigbird
        self.model_BigBird = BigBirdPegasusForConditionalGeneration.from_pretrained(
            "google/bigbird-pegasus-large-arxiv", attention_type="original_full")
        self.tokenizer_BigBird = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")
        # by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64

        self.tokenizer_Pegasus = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
        self.model_Pegasus = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')

    def text_summarizer(self, text, min_len, max_len, num_sentences):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        text_summary_dict = {}

        text_summary_dict['_text_'] = text
        # Encoding the inputs and passing them to model.generate()
        inputs = self.tokenizer_bart.batch_encode_plus([text], return_tensors='pt', truncation=True)
        summary_ids = self.model_bart.generate(inputs['input_ids'], early_stopping=True, min_length=min_len,
                                               max_length=max_len)
        bart_summary = self.tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)
        # print(bart_summary)
        text_summary_dict['bart_summary'] = bart_summary

        inputs = self.tokenizer_BigBird(text, return_tensors='pt')
        summary_ids = self.model_BigBird.generate(**inputs, min_length=min_len, max_length=max_len)
        summary_BigBird = self.tokenizer_BigBird.batch_decode(summary_ids, skip_special_tokens=True)
        text_summary_dict['summary_BigBird'] = summary_BigBird
        print(summary_BigBird)

        # google pegasus summarization

        inputs = self.tokenizer_Pegasus([text], truncation=True, padding='longest', return_tensors="pt")
        summary_ids = self.model_Pegasus.generate(inputs['input_ids'], min_length=min_len, max_length=max_len)
        summary_google_pegasus = self.tokenizer_Pegasus.batch_decode(summary_ids, skip_special_tokens=True)
        text_summary_dict['summary_google_pegasus'] = summary_google_pegasus

        t5_text = "summarize:" + text
        # encoding the input text
        input_ids = self.tokenizer_t5.encode(t5_text, return_tensors='pt')
        summary_ids = self.model_t5.generate(input_ids, early_stopping=True, min_length=min_len, max_length=max_len)
        t5_summary = self.tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)
        text_summary_dict['t5_summary'] = t5_summary
        # gensim_summary
        summary_genensim = summarize(text)
        text_summary_dict['gensim_summary'] = summary_genensim
        my_parser = PlaintextParser.from_string(text, Tokenizer('english'))
        lexrank_summary_sentences = lex_rank_summarizer(my_parser.document, sentences_count=num_sentences)
        lexrank_summary = ""
        for sentence in lexrank_summary_sentences:
            lexrank_summary = lexrank_summary + " " + str(sentence)
        text_summary_dict['lexrank_summary'] = lexrank_summary
        # creating the lsa summarizer
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        lsa_summary_sentences = lsa_summarizer(parser.document, num_sentences)
        lsa_summary = ""
        #  lsa summary
        for sentence in lsa_summary_sentences:
            lsa_summary = lsa_summary + " " + str(sentence)
        text_summary_dict['lsa_summary'] = lsa_summary
        return text_summary_dict