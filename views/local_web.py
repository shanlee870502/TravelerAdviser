from flask import Blueprint, render_template, redirect, request, url_for

local_web = Blueprint("local_web",__name__)

@local_web.route('/localCompany',methods=['GET','POST'])
def local_company():
    return render_template('localCompany.html')