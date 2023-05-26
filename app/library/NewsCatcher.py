import requests
from bs4 import BeautifulSoup
import csv
import os

news_type = input('Masukkan jenis berita : ')
url = 'https://turnbackhoax.id/page/'
url_search = '/?s=%5B{}%5D'.format(news_type)
#url_search = '/?s=%5BSALAH%5D'

datas = [] 
count_page = 0

for page in range(0, 10):
  count_page += 1
  print('scrapping page : ',count_page)
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
    datas.append([title, description, date, label])

head = ['Judul','Deskripsi','Tanggal Dibuat', 'Label']
cwd = os.getcwd()
writer = csv.writer(open('%s/%s.csv' %(cwd, news_type.upper()), 'w', newline=''))
writer.writerow(head)