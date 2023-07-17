import string, re, nltk, time, numpy, json
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from python_translator import Translator
from sqlalchemy import or_

from ..models import News

class NewsChecker():

    def __init__(self):
        # Download NLTK library
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
    def checkNews(self, newsTitle):
        startedTime = time.time()
        # Input process digunakan untuk tokenizing 
        newsTitleProcessed = self.inputProcess(newsTitle, True)
        # Digunakan untuk memproses text berita menjadi array dan check kata yang memiliki makna sama
        sense1 = self.wordDisambiguation(newsTitleProcessed)
        search_terms = newsTitle.split()
        conditions = [News.title.contains(term) for term in search_terms]
        # Digunakan untuk mendapakan data berita dari database dengan query judul yang hampir sama dengan yang dimasukkan pengguna
        newsWhereLike = [ News.title.like('%'+ n +'%') for n in newsTitle.split(' ')]
        newsData = News.query.filter(or_(*newsWhereLike)).all()
        # Jika tidak ada, maka akan di ambilkan 50 data berita terbaru
        if(len(newsData) == 0):
            newsData = News.query.limit(50).all()
        WUPArr = []
        PATHArr = []
        process = []
        for i, dt in enumerate(newsData):
            # Digunakan untuk memproses text berita menjadi array dan check kata yang memiliki makna sama
            sense2 = self.wordDisambiguation(self.inputProcess(dt.title_en))
            # Digunakan untuk memeriksa antara data dari database dan dari input user dan di ambil nilai WUP dan PATH
            wup = self.resultWUP(sense2, sense1)
            path = self.resultPATH(sense2, sense1)
            wupScore, pathScore = numpy.mean(wup), numpy.mean(path)
            WUPArr.append({'score': numpy.mean(wup), 'totalmatch' : sum(w != 0 for w in wup)})
            PATHArr.append({'score': numpy.mean(path), 'totalmatch' : sum(w != 0 for w in path)})
            process.append({'judul': dt.title, 'wupScore':  wupScore, 'pathScore': pathScore})
            
        # digunakan data tertinggi dari wup dan path
        resultWUP = max(w['score'] for w in WUPArr)
        resultPATH = max(w['score'] for w in PATHArr)
        # mendapatkan data berita yang mempunyai score tertinggi
        resultIndexWup = [w['score'] for w in WUPArr].index(resultWUP)
        resultIndexPath = [w['score'] for w in PATHArr].index(resultPATH)
        dataWUP = newsData[resultIndexWup]
        dataPATH = newsData[resultIndexPath]

        endedtime = time.time()
        elapsedTime = endedtime - startedTime
        # Digunakan untuk return data ke response json untuk API news Checker
        return {
            "elapsedtime": round(elapsedTime) / 60,
            "scrapdata": json.dumps([ dt.to_dict() for dt in newsData]),
            "process": json.dumps(process),
            "result": {
                "WUP": WUPArr[resultIndexWup],
                "PATH": PATHArr[resultIndexPath],
                "datamatchWUP": json.dumps(dataWUP.to_dict()),
                "datamatchPATH": json.dumps(dataPATH.to_dict()),
            }
        }

    def calculateResult(self, result, length):
        return sum(result) / length

    def wordDisambiguation(self, words):
        return [wordnet.synsets(word) for word in words if wordnet.synsets(word)]

    def resultWUP(self, synsets1, synsets2):
        return [max([max([max([synsety.wup_similarity(synsetx) for synsety in synset2]) for synsetx in synset1]) for synset2 in synsets2]) for synset1 in synsets1]

    def resultPATH(self, synsets1, synsets2):
        return [max([max([max([synsety.path_similarity(synsetx) for synsety in synset2]) for synsetx in synset1]) for synset2 in synsets2]) for synset1 in synsets1]

    def steamer_bahasa(self, text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return stemmer.stem(text)

    def remove_special(self, text):
        # remove tab, new line, ans back slice
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
        # remove non ASCII (emoticon, chinese word, .etc)
        text = text.encode('ascii', 'replace').decode('ascii')
        # remove mention, link, hashtag
        text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
        # remove incomplete URL
        return text.replace("http://", " ").replace("https://", " ")
                

    #remove number
    def remove_number(self, text):
        return  re.sub(r"\d+", "", text)

    #remove punctuation
    def remove_punctuation(self, text):
        return text.translate(str.maketrans("","",string.punctuation))

    #remove whitespace leading & trailing
    def remove_whitespace_LT(self, text):
        return text.strip()

    #remove multiple whitespace into single whitespace
    def remove_whitespace_multiple(self, text):
        return re.sub('\s+',' ',text)

    # remove single char
    def remove_singl_char(self, text):
        return re.sub(r"\b[a-zA-Z]\b", "", text)

    # NLTK word rokenize 
    def word_tokenize_wrapper(self, text):
        return word_tokenize(text)
    
    def doTranslate(self, text):
        return str(Translator().translate(text, "en", 'id'))
    
    def inputProcess(self, word, isSourceBahasa = False):
        if isSourceBahasa:
            word = self.steamer_bahasa(word)
            word = self.doTranslate(word)
        word = self.remove_special(str(word).lower())
        word = self.remove_number(word)
        word = self.remove_punctuation(word)
        word = self.remove_whitespace_LT(word)
        word = self.remove_whitespace_multiple(word)
        word = self.remove_singl_char(word)
        searchToken = word_tokenize(word)
        stopWords = set(stopwords.words('english')) 
        return [w for w in searchToken if w not in stopWords]