from . import db
from sqlalchemy.sql import func

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
