
from flask import render_template, request
from flask import jsonify
from app import app
from app import q
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
            if not url[:8].startswith(('https://', 'http://')):
                url = 'http://' + url
            r = requests.get(url)
        except:
            errors.append("Unable to get URL. Please use valid url")
        if r:
            #text processing  
            p = Processor(url, r)          
            job = q.enqueue_call(func=p.process, args=(), result_ttl=5000)
            print("Job ID:", job.get_id())  
            errors.append("Submitted. Now processing...")
    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/health')
def health():
    return 'Healthy. Ready!'

@app.route("/results/<jobId>", methods=["GET"])
def get_results(jobId):
    return Processor.result(id)