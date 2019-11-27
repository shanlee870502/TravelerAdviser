from flask import Blueprint, render_template, redirect, request, url_for
from pymongo import MongoClient
from flask_mongoengine import MongoEngine

search_api= Blueprint("search_api",__name__)

#這部分要改成db模組也可以----------------

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net/flaskTest')
db = client['EventResourse']
col = db['Event']
#------------------------------

@search_api.route('/searchcomplete', methods=['GET','POST'])
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