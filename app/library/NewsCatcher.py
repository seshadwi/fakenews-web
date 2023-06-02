import requests
from bs4 import BeautifulSoup
from datetime import datetime


def formatDate(date):
  month = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
  listDate = str(date).replace(",", "").split(" ")
  for i,m in enumerate(month):
    if m == listDate[0]:
      listDate[0] = str(i+1)

  return " ".join(listDate)

def catchNews(latestNewsDate = None):
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
      dateit= str(it.find('span', 'mh-meta-date updated').text)
      newsdate = datetime.strptime(formatDate(dateit), '%m %d %Y')
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