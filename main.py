from flask import render_template
from app import app
from models import Result
import os

print(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/health')
def health():
    return 'Healthy. Ready!'

if __name__ == '__main__':
    app.run()