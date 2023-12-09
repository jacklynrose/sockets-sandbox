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
    "swing": "both",
    "durationInMinutes": "",
    "timerType": "",
    "timerStartAt": "",
    "timerActive": "false",
} 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set/<name>', defaults={'value': None})
@app.route('/set/<name>/<value>')
def set(name, value):
    if (value):
        state[name] = value
    else:
        state[name] = None
    
    return 'OK'

@app.route('/get')
def get():
    return state