import flask
from flask import Blueprint, render_template, redirect, request, url_for
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore ,login_user, logout_user, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from werkzeug.utils import secure_filename
import os

#--------------------------------------
app = flask.Flask(__name__)
event_web = Blueprint("event_web",__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config.from_object('app.config')

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
db = client['EventResourse']
col = db['Event']
#---------------------------------------

def insert_data(event):
    if col.find_one({"eventName":event["eventName"]}) is None:
        col.insert_one(event)
        print('insert success')


@event_web.route('/complete', methods=['GET','POST'])
def complete():
    #activity_data是使用者輸入表單的資料    
    activity_data = request.values.to_dict()
    insert_data(activity_data)
    #print(activity_data)
    if 'event_photo' not in request.files:
        print('No file part')
    else:
        file = request.files['event_photo']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], activity_data['eventName']+".jpg"))
    return render_template('eventsBuild.html',title='MyActivity', activity=activity_data)

@event_web.route('/upLoadEvent')
# @login_required
# @roles_accepted('user','root')

def element():
    return render_template("upLoadEvent.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
