from flask import Flask
from flask import *

app = Flask(__name__, static_folder='static')

@app.route('/')
def testing():
     return render_template('index.html')

if __name__ == '__main__':
    app.run()