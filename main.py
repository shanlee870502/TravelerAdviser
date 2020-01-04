# -*- coding: utf-8 -*-
import os
import flask
from flask import render_template, request, jsonify, redirect, url_for, make_response, flash, session
from flask_bcrypt import Bcrypt
from flask_security import Security, MongoEngineUserDatastore ,login_user, logout_user, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import jieba
from bson import ObjectId
from datetime import datetime
from models import Map

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config.from_object('app.config')

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
db = client['EventResourse']
col = db['newEvent2']
#col = db['Event']
db = MongoEngine(app)
bcrypt = Bcrypt(app)
#密碼加密
def hashPassword(password):
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return pw_hash
#活動地址轉經緯度
def getlatlng(address):
    import googlemaps 
    gmaps = googlemaps.Client(key='AIzaSyBaLZySMH6UEN1158bcMPpUi3XaXotIb3A')
    try:
        geocode_result = gmaps.geocode(address)[0]['geometry']['location']
        return geocode_result
    except:
        return None
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
    flash("你沒有權限") 
    return redirect('/index')

# 設定未授權時轉跳畫面
security._state.unauthorized_handler(unauthorized_callback)

@app.before_first_request
def create_user():
    user_role = user_datastore.find_or_create_role('user')
    if user_datastore.get_user('user') == None:       
        user_datastore.create_user(
            email='user', password = hashPassword('user'), roles=[user_role]
        )
    admin_role = user_datastore.find_or_create_role('admin')
    if user_datastore.get_user('root') == None:
        user_datastore.create_user(
            email='root', password = hashPassword('root'), roles=[admin_role]
        )
    guest_role = user_datastore.find_or_create_role('guest')
    if user_datastore.get_user('guest') == None:
        user_datastore.create_user(
            email='guest', password = hashPassword('guest'), roles=[guest_role]
        )
        
def insert_data(event):
    if col.find_one({"eventName":event["eventName"]}) is None:
        event['location'] = getlatlng(event['eventLocation'])
        col.insert_one(event)
        print('insert success')
    #else:
        #print(col.find_one({"eventName":event["eventName"]}))
@app.route('/newCompany', methods=['GET', 'POST'])
def newCompany():
    return render_template("newCompany.html")

@app.route('/addCompany', methods=['GET', 'POST'])
@login_required
def addCompany():
    db = client['localCompany']
    col = db['company']
    company = request.values.to_dict()
    col.insert_one(company)
    return redirect("localCompany")

@app.route('/localCompany', methods=['GET','POST'])
def find_all_company():
    db = client['localCompany']
    col = db['company']
    result = col.find({},{"_id":0,"companyName":1,"companyDetail":1})
    tmp = list(result)
    print(tmp)
    return render_template("localCompany.html", company = tmp)

@app.route('/register_user',methods=['GET','POST'])
def register_user():
    create_user = request.values.to_dict()

    user_role = user_datastore.find_or_create_role('user')
    if user_datastore.get_user(create_user['username']) == None:
        user_datastore.create_user(
            email = create_user['username'], password = hashPassword(create_user['password']), roles=[user_role]
        )
        return redirect('/login')
#    repeat_text = "該使用者已被註冊"
    return redirect('register')

@app.route('/register.html',methods=['GET','POST'])
def register_page():
    return render_template("Register.html")


        
@app.route('/')
@app.route('/login', methods=['GET', 'POST']) 
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_Use():
    try:
        nowUser = request.values.to_dict()
        print(nowUser)
        userdb =client['flaskTest']
        user_col=userdb['user']
        print(user_col.find_one({'email':nowUser['email']}))
        user_in_db =user_col.find_one({'email':nowUser['email']})
        if user_in_db is None or bcrypt.check_password_hash(user_in_db['password'], nowUser['password']) is False:
            print(user_in_db)
            print(bcrypt.check_password_hash(user_in_db['password'], nowUser['password']))
            return redirect('/login')
        
    #    設置session
        session['username'] = nowUser['email']
        session.permanent = True
        
        nowUser=user_datastore.get_user(nowUser['email'])
        login_user(nowUser)
        return redirect('index')
    except:
        return redirect('/login')
           
@app.route('/logout_user', methods=['GET','POST'])
def logout_Use():
    logout_user()
    session['username'] = False
    return redirect('/index')
           
@app.route('/index', methods=['GET','POST'])
def home():
    strNow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    isLogin = session.get('username')
    result = col.aggregate([
                {
                    "$project":
                    {
                        "eventName": 1,
                        "eventM_F": { "$substr": [ "$eventM_F", 0, 16 ] },
                        "eventM_B": {"$substr": ["$eventM_B", 0, 16 ]},
                    }
                },
                {
                    "$match": {'eventM_F':{'$gte':strNow}}
                },
                {   
                    "$sort": { "eventM_B": 1 }
                },
                { "$limit" : 10 }
                ])
    return render_template("index.html", bulletin=list(result), isLogin = isLogin)

@app.route('/loginSession',methods=['GET','POST'])
def get_login_session():   
    isLogin = {'user':session.get('username')}
    return jsonify(isLogin)
@app.route('/upLoadEvent')
@login_required
@roles_accepted('admin')
def element():
    return render_template("upLoadEvent.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/complete', methods=['GET','POST'])
def complete():
    #activity_data是使用者輸入表單的資料    
    activity_data = request.values.to_dict()
    randomSeedByNow = datetime.now()
    eventID = str(ObjectId.from_datetime(randomSeedByNow))
    
    activity_data['eventID'] = eventID
    
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], activity_data['eventID']+".jpg"))
    return render_template('eventsBuild.html',title='MyActivity', activity=activity_data)

@app.route('/search', methods=['GET'])
def searchPage():
    return render_template('search.html')


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
#                            'http':searchEvent['email_'],
                            'eventM_B' : searchEvent['eventM_B'],
                            'eventLocation' : searchEvent['eventLocation'],
                            'eventID' : searchEvent['eventID']
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
            for word in remainderWords:
                findEvents = col.find({"eventName" : {'$regex' : ".*"+word+".*"}})
                for match in findEvents:
                    events={
                        'eventName' :match['eventName'],
#                        'email':match['email_'],
                        'eventM_B' : match['eventM_B'].replace("T"," "),
                        'eventLocation' : match['eventLocation'],
                        'eventID' :match['eventID']
                    }
                    searchEvents.append(events)
            return jsonify(searchEvents)
        #3 Latest event 
        if data['type']=='recently':
            strNow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            lastupload = col.aggregate([{"$match":{'eventM_F':{'$gte':strNow}}},{ "$sort": { "eventM_B": 1 }}])
            count = 0
            for match in lastupload:
                count+=1
                events={
                    'eventName' :match['eventName'],
#                    'email':match['email_'],
                    'eventM_B' : match['eventM_B'].replace("T"," "),
                    'eventLocation' : match['eventLocation'],
                    'eventID' : match['eventID']
                }
                searchEvents.append(events)
                if count == 15:
                    break
            return jsonify(searchEvents)
            
            
        # #3 earlist upload time
        if data['type']=='upLoadTime':
            print('here')
            lastupload = col.find().skip(col.count() - 15)
            for match in lastupload:
                events={
                    'eventName' :match['eventName'],
#                    'email':match['email_'],
                    'eventM_B' : match['eventM_B'].replace("T"," "),
                    'eventLocation' : match['eventLocation'],
                    'eventID' : match['eventID']
                }
                print(events)
                searchEvents.append(events)
            return jsonify(searchEvents)
        if data['type'] =='byLocation':
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
            for word in remainderWords:
                findEvents = col.find({"eventLocation" : {'$regex' : ".*"+word+".*"}})
                for match in findEvents:
                    events={
                        'eventName' :match['eventName'],
#                        'email':match['email_'],
                        'eventM_B' : match['eventM_B'].replace("T"," "),
                        'eventLocation' : match['eventLocation'],
                        'eventID' :match['eventID']
                    }
                    searchEvents.append(events)
            return jsonify(searchEvents)
@app.route('/eventdetails',methods=['GET','POST'])
def showEvents():
    data= request.values.to_dict()
    print(data)
    activity_data=col.find_one({"eventName":data["eventName"]})
    # tempB=activity_data['eventM_B']
    # tempF=activity_data['eventM_F']
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
    result = Map.FindNearLocation(data['lat'], data['lng'])
    return jsonify(result)

@app.route('/map')
def map():
    return render_template("map.html")

app.run(host="140.121.199.231", port=27018)
#testDate = datetime.strptime('2019-12-28T13:30:00', "%Y-%m-%dT%H:%M:%S")

