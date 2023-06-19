import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ..models import News, db, Results


def formatDate(date):
  month = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
  listDate = str(date).replace(",", "").split(" ")
  for i,m in enumerate(month):
    if m == listDate[0]:
      listDate[0] = str(i+1)

  return " ".join(listDate)

def catchFromKominfo(page, latestNewsDate):
  url = 'https://www.kominfo.go.id/content/all/laporan_isu_hoaks'
  req = requests.get(url if page == 1 else "%s?page=%s"%(url, page))
  soup = BeautifulSoup(req.text, 'html.parser')
  items = soup.findAll('div', 'content')
  itemsDates = soup.findAll('div', 'data-column')
  isBreaked = False
  for (index, it) in enumerate(items):
    title = it.find('a', 'title').text
    if "[HOAKS] " in title:
      title = title.replace("[HOAKS] ", '') 
      url = it.find('a', 'title', href=True)['href']
      label = 0
      dates = itemsDates[index].find('div', "date")
      month = "-".join(str(dates.text).split(" "))
      dateRender = datetime.strptime(month, '%d-%M-%Y')
      if latestNewsDate != None:
        if latestNewsDate >= dateRender.date():
          isBreaked = latestNewsDate >= dateRender.date()
          break
      dt = {
        "title" : title.encode("ascii", 'ignore').decode('ascii'),
        "description": '',
        "date" : dateRender.strftime("%Y-%m-%d"),
        "label": label,
        "url": 'https://www.kominfo.go.id%s'%(url)
      }
      news = News(dt['title'], dt['description'], dt['date'], dt['label'], dt['url'])
      db.session.add(news)
  db.session.commit()
  if isBreaked:
    return False
  return True

def catchFromTurnbackhoax(page, latestNewsDate):
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
    urlNews = it.find('a', href=True)['href']
    label = True if "[BENAR]" in titleIt else False
    dt = {
        "title" : title.encode("ascii", 'ignore').decode('ascii'),
        "description": description,
        "date" : newsdate.strftime("%Y-%m-%d"),
        "label": label,
        "url": urlNews
      }
    news = News(dt['title'], dt['description'], dt['date'], dt['label'], dt['url'])
    
    db.session.add(news)
  db.session.commit()
  if isBreaked:
    return False
  return True

def catchNews(latestNewsDate = None):
  datas = [] 
  for page in range(1, 10):
    catchFromTurnbackhoax(page, latestNewsDate)
    catchFromKominfo(page, latestNewsDate)
  return datas