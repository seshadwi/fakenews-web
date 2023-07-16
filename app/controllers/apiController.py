import flask
from ..library import NewsCatcher, NewsChecker
from ..models import News, db, Results
from sqlalchemy import func

def identify():
    title = flask.request.values.get('title')
    if flask.request.method == "POST":
        if title:
            # memanggil fungsi check berita
            newsCheck = NewsChecker().checkNews(title)
            # Digunakan untuk menyimpan hasil ke database table result
            result = Results(newsCheck)
            db.session.add(result)
            db.session.commit()
            # Digunakan untuk menampilkan response di request api nanti dan di tampilkan di web
            return flask.jsonify({
                'status': True,
                'data' : result.to_dict(),
                'message': "Success identify"
            }), 200
    # Digunakan untuk menampilkan response di request api nanti dan di tampilkan di web
    return flask.jsonify({
        'status': False,
        'data': title,
        'message': "Wrong Method" if title != None else 'Tolong masukkan judul berita yang akan di klasifikasi'
    }), 400
    


def syncNews():
    if flask.request.method == "POST":
        # mendapatkan data tanggal terbaru berita dari database
        latestDate = db.session.query(func.max(News.newsdate)).scalar()
        # Untuk mendapatkan data berita dari kominfo dan turnbackhoax
        data = NewsCatcher.catchNews(latestDate)
        # Digunakan untuk menampilkan response di request api nanti dan di tampilkan di web
        return flask.jsonify({
            "status": True,
            "message": "Berhasil memperbarui %s data terbaru" %(len(data)), 
            "data": data
        }), 200
    # Digunakan untuk menampilkan response di request api nanti dan di tampilkan di web
    return flask.jsonify({
            "status": False,
            "message": "Wrong method", 
            "data": None
        }), 400