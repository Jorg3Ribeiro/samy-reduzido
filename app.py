from sumy.parsers.plaintext import PlaintextParser # type: ignore
from sumy.parsers.html import HtmlParser # type: ignore
from sumy.nlp.tokenizers import Tokenizer # type: ignore
from sumy.nlp.stemmers import Stemmer # type: ignore
from sumy.utils import get_stop_words # type: ignore

import gradio as gr

import nltk
nltk.download('punkt')

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    method: str
    language: str 
    sentence_count: int 
    input_type: str
    input_: str

@app.post("/summarize")
def summarize(data: Data):
  if data.method== 'LSA':
    from sumy.summarizers.lsa import LsaSummarizer as Summarizer
  if data.method=='text-rank':
    from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
  if data.method=='lex-rank':
    from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
  if data.method=='edmundson':
    from sumy.summarizers.edmundson import EdmundsonSummarizer as Summarizer
  if data.method=='luhn':
    from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
  if data.method=='kl-sum':
    from sumy.summarizers.kl import KLSummarizer as Summarizer
  if data.method=='random':
    from sumy.summarizers.random import RandomSummarizer as Summarizer
  if data.method=='reduction':
    from sumy.summarizers.reduction import ReductionSummarizer as Summarizer

  if data.input_type=="URL":
    parser = HtmlParser.from_url(data.input_, Tokenizer(data.language))
  if data.input_type=="text":
    parser = PlaintextParser.from_string(data.input_, Tokenizer(data.language))
    
  stemmer = Stemmer(data.language)
  summarizer = Summarizer(stemmer)
  stop_words = get_stop_words(data.language)

  if data.method=='edmundson':
    summarizer.null_words = stop_words
    summarizer.bonus_words = parser.significant_words
    summarizer.stigma_words = parser.stigma_words
  else:
    summarizer.stop_words = stop_words

  summary_sentences = summarizer(parser.document, data.sentence_count)
  summary = ' '.join([str(sentence) for sentence in summary_sentences])
  
  return summary

if __name__ == "__main__":
  uvicorn.run(app, port=8888, host="0.0.0.0")

