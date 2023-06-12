from nltk.corpus import stopwords
import requests

def removeStopWordsIndonesian(words):
    list_stopwords = stopwords.words('indonesian')
    list_stopwords.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                       '&amp', 'yah'])
    urlPasteBin = 'https://pastebin.com/raw/utu7qqbs'
    txt_stopword = requests.get(urlPasteBin).text.split('\r\n')
    list_stopwords.extend(txt_stopword)
    list_stopwords = set(list_stopwords)
    return [word for word in words if word not in list_stopwords]