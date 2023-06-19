from . import db
from sqlalchemy.sql import func, select
from python_translator import Translator
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from sqlalchemy_serializer import SerializerMixin
from encoding_tools import TheSoCalledGreatEncoder
import uuid, json

def steamer_bahasa(text):
  from .library.wordHelper import removeStopWordsIndonesian
  text = " ".join(removeStopWordsIndonesian(word_tokenize(text)))
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()  
  return "".join(stemmer.stem(text))

def encodeText(text):
   encoder = TheSoCalledGreatEncoder()
   encoder.load_str(text)
   encoder.encode("UTF-8", force_ascii=True)
   return encoder.encoded_data

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    description = db.Column(db.Text)
    newsdate = db.Column(db.Date)
    label = db.Column(db.Boolean)
    url = db.Column(db.Text)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self, title, description, newsdate, label, url):
        translate = Translator().translate(steamer_bahasa(title), 'EN', 'ID')
        self.title = title
        self.title_en = encodeText(str(translate)).decode('utf-8')
        self.description = description
        self.newsdate = newsdate
        self.label = label
        self.url = url
    

class Results(db.Model, SerializerMixin):
  __tablename__='results'
  id = db.Column(db.String(255), primary_key=True)
  result = db.Column(db.JSON)
  createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
  updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())

  def __init__(self, result:dict):
     self.id = str(uuid.uuid4())
     self.result = json.dumps(result)