import math
from gensim.summarization import summarize
from transformers import BartForConditionalGeneration, BartTokenizer
# from transformers import XLMWithLMHeadModel, XLMTokenizer

# from transformers import T5Tokenizer, T5ForConditionalGeneration
# from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer
# from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# from bs4 import BeautifulSoup
# Importing the parser and tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
# Import the LexRank summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

lex_rank_summarizer = LexRankSummarizer()
from sumy.summarizers.lsa import LsaSummarizer

lsa_summarizer = LsaSummarizer()


def set_summary_length(text):
    number_of_words = len(word_tokenize(text))
    number_of_sentences = len(sent_tokenize(text))
    print(number_of_words)
    print(number_of_sentences)
    summary_sentences_len = math.ceil(number_of_sentences / 3)
    summary_min_tokens = math.ceil(number_of_words / 4)
    summary_max_tokens = number_of_words // 3
    return summary_min_tokens, summary_max_tokens, summary_sentences_len


class TextSummarizer:
    def __init__(self):
        """Performs text summarization for the given text by implementing different text summarization models
         __init__ method initialize all the models for text summary"""
        self.num_sentences = None
        self.max_len = None
        self.min_len = None
        self.text_summary_dict = {}
        # Instantiating the model and tokenizer bart
        self.tokenizer_bart = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model_bart = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        # Instantiating the model and tokenizer t5
        # self.model_t5 = T5ForConditionalGeneration.from_pretrained('t5-small')
        # self.tokenizer_t5 = T5Tokenizer.from_pretrained('t5-small')
        # # Instantiating the model and tokenizer google_bigbird
        # self.model_BigBird = BigBirdPegasusForConditionalGeneration.from_pretrained(
        #     "google/bigbird-pegasus-large-arxiv", attention_type="original_full")
        # self.tokenizer_BigBird = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")
        # by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64

        # self.tokenizer_Pegasus = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
        # self.model_Pegasus = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')

    @staticmethod
    def set_summary_length(text):
        """
        set the length of summary for extractive and abstractive summary based on size of tokens and number of
        sentences in text.
        :param text: text to be summarized
        :return:  minimum maximum size of tokens for transformers models and number of sentence in summary for
        extractive summary
        """
        number_of_words = len(word_tokenize(text))
        number_of_sentences = len(sent_tokenize(text))
        print(number_of_words)
        print(number_of_sentences)
        summary_sentences_len = math.ceil(number_of_sentences / 3)
        summary_min_tokens = math.ceil(number_of_words / 4)
        summary_max_tokens = number_of_words // 3
        return summary_min_tokens, summary_max_tokens, summary_sentences_len

    def bart_model_summary_generation(self, text):
        # Encoding the inputs and passing them to model.generate()
        inputs = self.tokenizer_bart.batch_encode_plus([text], return_tensors='pt', truncation=True)
        summary_ids = self.model_bart.generate(inputs['input_ids'], early_stopping=True, min_length=self.min_len,
                                               max_length=self.max_len)
        bart_summary = self.tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)
        # print(bart_summary)
        self.text_summary_dict['bart_summary'] = bart_summary

    def bigbird_model_summary_generation(self, text):
        inputs = self.tokenizer_BigBird(text, return_tensors='pt')
        summary_ids = self.model_BigBird.generate(**inputs, min_length=self.min_len, max_length=self.max_len)
        summary_BigBird = self.tokenizer_BigBird.batch_decode(summary_ids, skip_special_tokens=True)
        self.text_summary_dict['summary_BigBird'] = summary_BigBird
        # print(summary_BigBird)

    def google_pagasus_model_summary_generation(self, text):
        # google pegasus summarization
        inputs = self.tokenizer_Pegasus([text], truncation=True, padding='longest', return_tensors="pt")
        summary_ids = self.model_Pegasus.generate(inputs['input_ids'], min_length=self.min_len, max_length=self.max_len)
        summary_google_pegasus = self.tokenizer_Pegasus.batch_decode(summary_ids, skip_special_tokens=True)
        self.text_summary_dict['summary_google_pegasus'] = summary_google_pegasus

    def t5_transformers_summary_generation(self, text):
        t5_text = "summarize:" + text
        # encoding the input text
        input_ids = self.tokenizer_t5.encode(t5_text, return_tensors='pt')
        summary_ids = self.model_t5.generate(input_ids, early_stopping=True, min_length=self.min_len,
                                             max_length=self.max_len)
        t5_summary = self.tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)
        self.text_summary_dict['t5_summary'] = t5_summary

    def lex_rank_summary_generation(self, text):
        my_parser = PlaintextParser.from_string(text, Tokenizer('english'))
        lexrank_summary_sentences = lex_rank_summarizer(my_parser.document, sentences_count=self.num_sentences)
        lexrank_summary = ""
        for sentence in lexrank_summary_sentences:
            lexrank_summary = lexrank_summary + " " + str(sentence)
        self.text_summary_dict['lexrank_summary'] = lexrank_summary

    def lsa_summary_generation(self, text):
        # creating the lsa summarizer
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        lsa_summary_sentences = lsa_summarizer(parser.document, self.num_sentences)
        lsa_summary = ""
        #  lsa summary
        for sentence in lsa_summary_sentences:
            lsa_summary = lsa_summary + " " + str(sentence)
        self.text_summary_dict['lsa_summary'] = lsa_summary

    def gensim_summary_generation(self, text):
        summary_gensim = summarize(text)
        self.text_summary_dict['gensim_summary'] = summary_gensim

    def text_summarizer(self, summary_text):
        """
        Performs text summarization for give text using different text summarization approaches and save results in
        dictionary format where keys are summarization algorithm and values representing the summary generated using

        :param summary_text:
        :return: text_summary_dict: summary generated using different summarizers
        """
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.text_summary_dict['_text_'] = text
        self.min_len, self.max_len, self.num_sentences = self.set_summary_length(summary_text)
        self.bart_model_summary_generation(summary_text)
        # self.bigbird_model_summary_generation(summary_text)
        # self.google_pagasus_model_summary_generation(summary_text)
        # self.t5_transformers_summary_generation(summary_text)
        self.lex_rank_summary_generation(summary_text)
        self.lsa_summary_generation(summary_text)
        self.gensim_summary_generation(summary_text)


        return self.text_summary_dict
