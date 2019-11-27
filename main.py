import os
import flask
from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from flask_security import Security, MongoEngineUserDatastore ,login_user, logout_user, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import jieba
from views import index_web,search_api,search_web,event_web,local_web


app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config.from_object('app.config')

# client = MongoClient('mongodb+srv://Liao:871029@cluster0-sk2jk.mongodb.net')
# db = client['EventResourse']
# col = db['Event']
# db = MongoEngine(app)

def register_web():
    app.register_blueprint(index_web.index_web, url_prefix = '/')
    app.register_blueprint(search_web.search_web, url_prefix = '/')
    app.register_blueprint(event_web.event_web, url_prefix = '/')
    app.register_blueprint(local_web.local_web, url_prefix = '/')

def register_api():
    app.register_blueprint(search_api.search_api, url_prefix ='/')

def run():
    register_web()
    register_api()
    app.run(debug=True)

if __name__ == '__main__':
    run()