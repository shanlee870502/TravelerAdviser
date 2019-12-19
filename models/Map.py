# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:07:27 2019

@author: ntou-nlp
"""

import math
from pymongo import MongoClient

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
db = client['EventResourse']

colEvent= db['newEvent2']

def myGetDistance(p1,p2):
    lat1 = (math.pi/180)*p1['lat']
    lat2 = (math.pi/180)*p2['lat']
    
    lng1 = (math.pi/180)*p1['lng']
    lng2 = (math.pi/180)*p2['lng']
    
    #地球半徑
    R =6371
    
    return math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lng2-lng1))*R

def FindNearLocation(lat, lng):
    distances = {}
    for event in colEvent.find():
        try:
            distance = myGetDistance({'lat':lat,'lng':lng},event['location'])
            distances[event['eventName']] = distance
        except:
            continue
    
    distances = sorted(distances.items(), key=lambda x:x[1])
    eventResult =[]
    for i in range(5):
        result = colEvent.aggregate([
                            {"$match":{"eventName":distances[i][0]}},
                            {"$project":{'eventName':1, 'eventLocation':1,
                                         'location':1,'_id':0,'eventM_B':1,
                                         'eventM_F':1}}
                        ])
        eventResult.append(list(result))
    return eventResult