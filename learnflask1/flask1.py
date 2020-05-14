import flask
from flask import Flask ,render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/prince")
def prince():
    name='Prince Gaur'
    return render_template('about.html',name1=name)
app.run(debug=True)