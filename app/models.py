from . import db
from sqlalchemy.sql import func, select
from python_translator import Translator

class News(db.Model):
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
        self.title_en = str(Translator().translate(title, 'EN', 'ID'))
        self.description = description
        self.newsdate = newsdate
        self.label = label

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
