import flask
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
from datetime import datetime
import json

with open('config.json','r') as c: 
    params= json.load(c)["params"]

local_server= True
app= Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL= True,
    MAIL_USERNAME= params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']

)
mail= Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    
    SNo= db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=True,nullable=False)
    Date = db.Column(db.String(120), unique=True)
    Email= db.Column(db.String(120), unique=True,nullable=False)
    Phone_number = db.Column(db.String(120), unique=True,nullable=False)
    Message = db.Column(db.String(120), unique=True,nullable=False)

class Posts(db.Model):

    SNo= db.Column(db.Integer, primary_key=True)
    Title= db.Column(db.String(80), unique=True,nullable=False)
    Subheading = db.Column(db.String(80),unique=True,nullable=True)
    Bodyheading = db.Column(db.String(101),unique=False,nullable=True)
    slug= db.Column(db.String(25), unique=True,nullable=False)
    Content= db.Column(db.String(120), unique=True,nullable=False)
    image= db.Column(db.String(25),unique=True,nullable =False)
    Date= db.Column(db.String(12), nullable=True)
    Author = db.Column(db.String(101),nullable=True)
    
@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)


@app.route("/about.html")
def about():
    return render_template('about.html',params=params)

@app.route("/allposts.html")
def post():
    posts = Posts.query.filter_by().all()
    return render_template('allposts.html', params=params, posts=posts)

@app.route("/contact.html",methods={'GET','POST'})
def contact():
    if  request.method=='POST':
        #Add entry to database
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=Contacts(Name=name, Email=email, Date=datetime.now(),Phone_number=phone,Message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Blog Maniac query from '+ name,
                            sender=email,
                            recipients=[params['gmail-user']],
                            body = message + "\n" + phone
        )
        
    return render_template('contact.html',params=params)

@app.route("/post.html/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    #fetch post
    post= Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)
    
if __name__ == "__main__": 
		app.run(debug=True)

