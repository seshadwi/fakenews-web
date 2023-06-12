import flask
from ..library import NewsCatcher, NewsChecker
from ..models import News, db, Results
from sqlalchemy import func

def identify():
    title = flask.request.values.get('title')
    if flask.request.method == "POST":
        if title:
            newsCheck = NewsChecker().checkNews(title)
            result = Results(newsCheck)
            db.session.add(result)
            db.session.commit()
            return flask.jsonify({
                'status': True,
                'data' : result.to_dict(),
                'message': "Success identify"
            }), 200
        
    return flask.jsonify({
        'status': False,
        'data': title,
        'message': "Wrong Method" if title != None else 'Tolong masukkan judul berita yang akan di klasifikasi'
    }), 400
    


def syncNews():
    if flask.request.method == "POST":
        latestDate = db.session.query(func.max(News.newsdate)).scalar()
        data = NewsCatcher.catchNews(latestDate)
        for i, dt in enumerate(data):
            news = News(dt['title'], dt['description'], dt['date'], dt['label'])
            db.session.add(news)

        db.session.commit()

        return flask.jsonify({
            "status": True,
            "message": "Berhasil memperbarui %s data terbaru" %(len(data)), 
            "data": data
        }), 200
    
    return flask.jsonify({
            "status": False,
            "message": "Wrong method", 
            "data": None
        }), 400