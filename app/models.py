from . import db
from sqlalchemy.sql import func, select
from python_translator import Translator
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from sqlalchemy_serializer import SerializerMixin
import uuid, json

def steamer_bahasa(text):
  from .library.wordHelper import removeStopWordsIndonesian
  text = " ".join(removeStopWordsIndonesian(word_tokenize(text)))
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()
  return "".join(stemmer.stem(text))

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    description = db.Column(db.Text)
    newsdate = db.Column(db.Date)
    label = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self, title, description, newsdate, label):
        self.title = title
        self.title_en = str(Translator().translate(steamer_bahasa(title), 'EN', 'ID'))
        self.description = description
        self.newsdate = newsdate
        self.label = label
    

class Results(db.Model, SerializerMixin):
  __tablename__='results'
  id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
  result = db.Column(db.JSON)
  createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
  updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())

  def __init__(self, result:dict):
     self.result = json.dumps(result)