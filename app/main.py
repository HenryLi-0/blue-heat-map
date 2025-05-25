from flask import Flask, render_template
from threading import Thread
from settings import *
import requests
from app.logging import *

'''MINECRAFT PROCESSING STUFF'''
if BACKEND:
    Network.tick()
    def backendThread():
        pass
    thread = Thread(target=backendThread)
    thread.start()

'''FLASK STUFF'''

if FRONTEND:
    app = Flask(__name__)

    '''
    TO DO:
    - main site (reports service/storage/etc. status and links to other bits)
    - log reading site (reads logs)
    - data analysis site (basically log reader except for data analysis, might change)
    - live dashboard
    '''

    @app.route('/')
    def test():
        return render_template("test2.html")

    @app.route('/original')
    def hmm():
        return render_template("test.html")

    app.run(debug=True, host="0.0.0.0", port=5000)