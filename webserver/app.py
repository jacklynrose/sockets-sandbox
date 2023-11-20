from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

state = {
    "power": "off",
    "mode": "auto",
    "temp": "21",
    "fan": "1",
    "swing": "both"
} 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set/<name>/<value>')
def set(name, value):
    state[name] = value
    return 'OK'

@app.route('/get')
def get():
    return state