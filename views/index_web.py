from flask import Blueprint, render_template, redirect, request, url_for

index_web = Blueprint("index_web",__name__)

@index_web.route('/index', methods=['GET'])
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
