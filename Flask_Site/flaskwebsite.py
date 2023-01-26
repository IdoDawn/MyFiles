from flask import Flask, render_template, url_for, flash, redirect, send_file, request, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from forms import RegistrationForm, LoginForm, UploadFileForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
 # from models import User, FileAuthor
import os
import datetime as dt



app = Flask(__name__)


baseFolderPath = r'/home/ido/Flask_Site/static/files'

app.config['SECRET_KEY'] = 'Sdgre32fxcasfa'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

    def retPass(self):
        return f'{self.password}'

    def retUsername(self):
        return self.username

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

class FileAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorname = db.Column(db.String(20), nullable=False)
    nameoffile = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.authorname}')"
    def __init__(self, authorname, nameoffile):
        self.authorname = authorname
        self.nameoffile = nameoffile
        
        

global islogged
islogged = 'Guest'


posts = [

    {
        'author': 'ido',
        'file_name': 'dogpic.jpg',
        'date_posted': 'april 20, 2069'
    },
    {
        'author': 'loido',
        'file_name': 'birdpic.jpg',
        'date_posted': 'april 21, 2067'
    }

]

def getTimeStampString(tSec: float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d')
    return tStr
def fObjFromScan(x):
        fileStat = x.stat()
        fTime = getTimeStampString(fileStat.st_mtime)
        fUpload = FileAuthor.query.filter_by(authorname=x.name).first()
        
        return {'name': x.name, 'mTime': fTime, 'mUpload': fUpload}
with app.app_context():
    fNames = [fObjFromScan(x) for x in os.scandir(baseFolderPath)]


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    with app.app_context():
        fNames = [fObjFromScan(x) for x in os.scandir(baseFolderPath)]
    if islogged:
        return render_template('home.html', files=fNames, logged=islogged)
    else:
        return render_template('home.html', files=fNames, logged='Guest')

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
        uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename)
    

@app.route("/fileupload", methods=['GET','POST'])
def fileupload():
    form = UploadFileForm()
    if form.validate_on_submit():
        # try:
            file = form.file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            uploader = FileAuthor(islogged, file.filename)
            db.session.add(uploader)
            db.session.commit()
            message = 'File Has Been Uploaded'
            return render_template('index.html', form=form, message=message)
        #except:
            #message = 'error'
            #return render_template('index.html', form=form, message=message)
    return render_template('index.html', form=form, message='upload your file')
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    message = 'hi'
    form = RegistrationForm()
    if form.validate_on_submit():
        message = 'hi again'
        named = request.form['username']
        passwd = request.form['password']
        newuser = User(named, passwd)
        
        try:
            db.session.add(newuser)
            db.session.commit()
            message = 'account created successfully'
            islogged = named
            return render_template('home.html', files=fNames, logged=named, message=message)
        except:
            message = 'account already exist'
            

        
    return render_template('register.html', title='Register',  form=form, message=message)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # y = ''
    message = 'Hi'
    
    # isPwRight = ''
    
    if form.validate_on_submit():
        newone = User.query.filter_by(username=form.username.data)


        # y = form.username.data
        # ps = form.password.data
        
        nright = User.query.filter_by(username=form.username.data).first()
        pRight = nright.password
        yy = "User('{}')".format(form.username.data)
        if yy.__eq__(nright.__repr__()) and pRight.__eq__(form.password.data):
            
            islogged = form.username.data
            return render_template('index.html', files=fNames, logged=islogged, message='logged in successfully')
        else:
            return render_template('login.html', title='Log_in', form=form, message=nright.__repr__())#'user name or password are incorrect')

    return render_template('login.html', title='Log_in', form=form, message=message)
    
if __name__ == '__main__':
	app.run(debug=True)

# with app.app_context():
  #  db.create_all()

