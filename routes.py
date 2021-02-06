
from flask import render_template, request
from app import app
from models import Result
from processor import Processor
import os
import requests

print(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        #get url that user has entered
        try:
            url = request.form['url']
            r = requests.get(url)
            #print(r.text)
        except:
            errors.append("Unable to get URL. Please use valid url")
        if r:
            #text processing
            p = Processor(url, r)
            data = p.process()
            errors = data["errors"]
            results = data["results"]
    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/health')
def health():
    return 'Healthy. Ready!'