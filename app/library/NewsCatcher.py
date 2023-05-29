import requests
from bs4 import BeautifulSoup
from python_translator import Translator
import csv
import os

def catchNews(news_type):
  url = 'https://turnbackhoax.id/page/'
  url_search = '/?s=%5B{}%5D'.format(news_type)
  datas = [] 
  for page in range(0, 10):
    req = requests.get(url+str(page)+str(url_search))
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'mh-loop-content mh-clearfix')
    ## Loop data items 
    for it in items:
      if news_type.lower() == 'benar':
        title = ''.join(it.find('h3', 'entry-title mh-loop-title').text.strip().split('/n')).replace('[BENAR]','')
      elif news_type.lower() == 'salah':
        title = ''.join(it.find('h3', 'entry-title mh-loop-title').text.strip().split('/n')).replace('[SALAH]','')
      description = it.find('div','mh-excerpt').text
      date = it.find('span', 'mh-meta-date updated').text
      label = '1' if news_type.lower() == 'benar' else '0'
      datas.append(
        {
          "title" : title, 
          "title_en": str(Translator().translate(title, "en", "id")),
          "date" : date,
          "label": label
        }
      )

  return datas