from flask import Flask, jsonify, json, request, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


from mydiary import app, app_db, now_time, jwt


@app.route('/')
def landingpage():
    """ This endpoint loads the landing page """
    return render_template('index.html')

@app.route('/registration')
def signuppage():
    return render_template('registration.html'), 200

@app.route('/login')
def loginpage():
    return render_template('login.html'), 200

@app.route('/home')
@jwt_required
def homepage():
    return render_template('home.html'), 200

@app.route('/edit')
@jwt_required
def editpage():
    return render_template('edit.html'), 200

@app.route('/userprofile')
@jwt_required
def profilepage():
    return render_template('profile.html'), 200

@app.route('/400')
def error400():
    return render_template('400.html'), 200

@app.route('/401')
def error401():
    return render_template('401.html'), 200

@app.route('/403')
def error403():
    return render_template('403.html'), 200

@app.route('/404')
def error404():
    return render_template('404.html'), 200

@app.route('/405')
def error405():
    return render_template('405.html'), 200

@app.route('/408')
def error408():
    return render_template('408.html'), 200

@app.route('/410')
def error410():
    return render_template('410.html'), 200

@app.route('/500')
def error500():
    return render_template('500.html'), 200

@app.route('/501')
def error501():
    return render_template('501.html'), 200

@app.route('/503')
def error503():
    return render_template('503.html'), 200

@app.route('/504')
def error504():
    return render_template('504.html'), 200




