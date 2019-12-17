import os
import flask
from flask import render_template, request, jsonify, redirect, url_for, make_response
from flask_security import Security, MongoEngineUserDatastore ,login_user, logout_user, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import jieba

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config.from_object('app.config')

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
db = client['EventResourse']
col = db['Event']
location_col = db['newEvent']
db = MongoEngine(app)


# 不同種權限身份
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

# 使用者資訊
class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#沒有權限導引畫面
def unauthorized_callback():
	return redirect('/')

# 設定未授權時轉跳畫面
security._state.unauthorized_handler(unauthorized_callback)

@app.before_first_request
def create_user():
    user_role = user_datastore.find_or_create_role('user')
    if user_datastore.get_user('user') == None:
        user_datastore.create_user(
            email='user', password='user', roles=[user_role]
        )
    admin_role = user_datastore.find_or_create_role('admin')
    if user_datastore.get_user('root') == None:
        user_datastore.create_user(
            email='root', password='root', roles=[admin_role]
        )
    guest_role = user_datastore.find_or_create_role('guest')
    if user_datastore.get_user('guest') == None:
        user_datastore.create_user(
            email='guest', password='guest', roles=[guest_role]
        )
        
def insert_data(event):
    if col.find_one({"eventName":event["eventName"]}) is None:
        col.insert_one(event)
        print('insert success')
    #else:
        #print(col.find_one({"eventName":event["eventName"]}))

#@app.route('/')
#def login():
#    if current_user.is_authenticated:
#        return redirect('index.html')
#    return render_template('login.html')
#    
@app.route('/')
@app.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_Use():
    nowUser = request.values.to_dict()
    print(nowUser)
    userdb =client['flaskTest']
    user_col=userdb['user']
    print(user_col.find_one({'email':nowUser['email']}))
    if user_col.find_one({'email':nowUser['email'],'password':nowUser['password']}) is None:
        return redirect('/login')
    nowUser=user_datastore.get_user(nowUser['email'])
    login_user(nowUser)
    return redirect('index')
           
           
@app.route('/index', methods=['GET'])
def home():
    temp_events=list()
    event={
       "http":"http://www.accupass.com/event/1904040739571150361040",
       "img":"static/images/pic01.jpg"
       }
    temp_events.append(event)
    event={
           "http":"http://www.accupass.com/event/1909140357534178828000",
           "img":"static/images/pic02.png"
           }
    temp_events.append(event)
    event={
           "http":"http://www.accupass.com/event/1901271544488531904750",
           "img":"static/images/pic03.png"
           }
    temp_events.append(event)
    return render_template("index.html",event = temp_events)

@app.route('/upLoadEvent')
@login_required
@roles_accepted('user','root')

def element():
    return render_template("upLoadEvent.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/complete', methods=['GET','POST'])
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

@app.route('/search', methods=['GET'])
def searchPage():
    return render_template('search.html')

@app.route('/localCompany',methods=['GET','POST'])
def local_company():
    return render_template('localCompany.html')

@app.route('/searchcomplete', methods=['GET','POST'])
def searchEvent():
    if request.method=='POST':
        data= request.get_json(silent=True)
        print(data)
        ##主題搜尋
        searchEvents=list()
        if data['type'] =='byType':
            for element in data['data']:
                searchType = col.find({element:'on'})
                for searchEvent in searchType:
                    temp_event={
                            'eventName' :searchEvent['eventName'],
                            'http':searchEvent['email_'],
                            'eventM_B' : searchEvent['eventM_B'],
                            'eventLocation' : searchEvent['eventLocation'],
                            }
                    searchEvents.append(temp_event)
            return jsonify(searchEvents)
        ##關鍵字搜尋 
        if data['type'] =='byName':
            stopWords=[]
            segments=[]
            remainderWords=[]
            with open('stopwordlist.txt', 'r', encoding='UTF-8') as file:
                for d in file.readlines():
                    d = d.strip()
                    stopWords.append(d)
            
            text = data['data']
            segments = jieba.cut(text, cut_all=False)
            
            remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', segments))
            #print(remainderWords)
            for word in remainderWords:
                findEvents = col.find({"eventName" : {'$regex' : ".*"+word+".*"}})
                print(findEvents)
                #print(word)
                for match in findEvents:
                    print(match)
                    events={
                        'eventName' :match['eventName'],
                        'email':match['email_'],
                        'eventM_B' : match['eventM_B'].replace("T"," "),
                        'eventLocation' : match['eventLocation'],
                    }
                    print(events)
                    searchEvents.append(events)
            return jsonify(searchEvents)
        #3 Latest event 
        if data['type']=='recently':
            print('here')
            lastupload = col.aggregate([{ "$sort": { "eventM_B": -1 } }])
            count = 0
            for match in lastupload:
                count+=1
                events={
                    'eventName' :match['eventName'],
                    'email':match['email_'],
                    'eventM_B' : match['eventM_B'].replace("T"," "),
                    'eventLocation' : match['eventLocation'],
                }
                print(events)
                searchEvents.append(events)
                if count == 3:
                    break
            return jsonify(searchEvents)
            
        # #3 earlist upload time
        if data['type']=='upLoadTime':
            print('here')
            lastupload = col.find().skip(col.count() - 3)
            for match in lastupload:
                events={
                    'eventName' :match['eventName'],
                    'email':match['email_'],
                    'eventM_B' : match['eventM_B'].replace("T"," "),
                    'eventLocation' : match['eventLocation'],
                }
                print(events)
                searchEvents.append(events)
            return jsonify(searchEvents)


# @app.route('/eventdetails',methods=['GET','POST'])
# def showEvents():
#     data= request.values.to_dict()
#     activity_data=col.find_one({"eventName":data["eventName"]})
#     return render_template('events.html',activity= activity_data)
@app.route('/eventdetails',methods=['GET','POST'])
def showEvents():
    data= request.values.to_dict()
    print(data)
    activity_data=col.find_one({"eventName":data["eventName"]})
    tempB=activity_data['eventM_B']
    tempF=activity_data['eventM_F']
    tempB=str(activity_data['eventM_B'])
    tempF=str(activity_data['eventM_F'])
    tempB=tempB.replace("T"," ")
    tempF=tempF.replace("T"," ")

    activity_data['eventM_B']=tempB
    activity_data['eventM_F']=tempF
    del activity_data["_id"]
    return render_template('events.html',activity= activity_data)

@app.route('/index_Logined',methods=['GET','POST'])
def IamAdmin():
    return render_template('index_Logined.html')

@roles_accepted('admin')
@app.route('/adminEdit', methods=['GET','POST'])
def admin_edit():
    data= request.get_json()
    col.delete_one({"eventName":data["eventName"]})
    return render_template("editEvent.html")
    
@app.route('/api/map/location', methods = ['GET','POST'])
def find_near_location():
    data = request.get_json()
    return jsonify({"location": [['25.150339','121.777132'],
                    ['25.250339','121.777132'],['25.350339',
                    '121.777132']]})

@app.route('/map')
def map():
    return render_template("map.html")

app.run(host="140.121.199.231", port=27018)
#127.0.0.1
#140.121.199.231