from flask import Flask
from routes.web import blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app = create_app()
app.register_blueprint(blueprint)


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)