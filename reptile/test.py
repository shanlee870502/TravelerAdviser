# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 14:53:02 2019

@author: Liao
"""

import requests
import urllib.request
from pymongo import MongoClient
import os
import time

client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
db = client['EventResourse']
colEvent = db['newEvent2']

html = requests.get("https://api.accupass.com/v3/events/1911081542391256360274")
brief = html.json()

brief = brief["organizer"]["brief"]
print(brief)
print('Done')   




