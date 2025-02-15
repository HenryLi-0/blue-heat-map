from flask import Flask, render_template
from threading import Thread
from settings import *
import requests

'''MINECRAFT PROCESSING STUFF'''
if BACKEND:
    def listener():
        pass
    thread = Thread(target=listener)
    thread.start()

'''FLASK STUFF'''

if FRONTEND:
    app = Flask(__name__)

    @app.route('/')
    def test():
        return render_template("test2.html")

    @app.route('/original')
    def hmm():
        return render_template("test.html")

    app.run(debug=True, host="0.0.0.0", port=5000)