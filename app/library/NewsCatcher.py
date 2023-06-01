import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

def catchNews(latestNewsDate = None):
  locale.setlocale(locale.LC_TIME, ('id', 'UTF-8'))
  datas = [] 
  for page in range(1, 10):
    url = 'https://turnbackhoax.id/' if page == 1 else 'https://turnbackhoax.id/page/'
    req = requests.get(url if page == 1 else '%s%s' %(url, page))
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'mh-loop-content mh-clearfix')
    isBreaked = False
    ## Loop data items 
    for it in items:
      titleIt = ''.join(it.find('h3', 'entry-title mh-loop-title').text.strip().split('/n'))
      newsdate = datetime.strptime(str(it.find('span', 'mh-meta-date updated').text), '%B %d, %Y')
      if latestNewsDate != None:
        if latestNewsDate >= newsdate.date():
          isBreaked = latestNewsDate >= newsdate.date()
          break
      if "[BENAR]" in titleIt:
        title = titleIt.replace('[BENAR] ','')
      elif "[SALAH]" in titleIt:
        title = titleIt.replace('[SALAH] ','')
      description = it.find('div','mh-excerpt').text
      label = True if "[BENAR]" in titleIt else False
      datas.append(
        {
          "title" : title.encode("ascii", 'ignore').decode('ascii'),
          "description": description,
          "date" : newsdate.strftime("%Y-%m-%d"),
          "label": label
        }
      )
    if isBreaked:
      break

  return datas