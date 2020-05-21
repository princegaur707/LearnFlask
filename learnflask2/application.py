import flask
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/blogmaniac'
db = SQLAlchemy(app)

class Contacts(db.Model):
    
    SNo= db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=True,nullable=False)
    Date = db.Column(db.String(120), unique=True)
    Email= db.Column(db.String(120), unique=True,nullable=False)
    Phone_number = db.Column(db.String(120), unique=True,nullable=False)
    Message = db.Column(db.String(120), unique=True,nullable=False)

class posts(db.Model):

    SNo= db.Column(db.Integer, primary_key=True)
    Title= db.Column(db.String(80), unique=True,nullable=False)
    Content= db.Column(db.String(120), unique=True,nullable=False)
    Date= db.Column(db.String(120), nullable=True)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about.html")
def about():
    return render_template('about.html')


@app.route("/contact.html",methods={'GET','POST'})
def contact():
    if  request.method=='POST':
        #Add entry to database
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=Contacts(Name=name, Email=email,Phone_number=phone,Message=message)
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contact.html')

@app.route("/post.html")
def post():
    return render_template('post.html')
    
app.run(debug=True)
