import flask
from flask import Flask 
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/prince")
def prince():
    return "Hello! Prince"
app.run(debug=True)