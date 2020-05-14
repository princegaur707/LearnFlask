import flask
from flask import Flask ,render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/prince")
def prince():
    return render_template('about.html')
app.run(debug=True)