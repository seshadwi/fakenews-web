from app import app
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)