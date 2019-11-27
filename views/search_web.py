from flask import Blueprint, render_template, redirect, request, url_for

search_web = Blueprint("search_web",__name__)

@search_web.route('/search', methods=['GET'])
def searchPage():
    return render_template('search.html')