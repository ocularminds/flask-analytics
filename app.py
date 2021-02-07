
import os
from flask import Flask
from rq import Queue
from worker import conn

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

q = Queue(connection=conn)
from models import *