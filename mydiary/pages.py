from flask import Flask, jsonify, json, request, render_template
from flask_jwt_extended import (
    jwt_required
)


from mydiary import app, app_db, now_time, jwt


@app.route('/')
def landingpage():
    """ This endpoint loads the landing page """
    return render_template('index.html'), 200

@app.route('/registration')
def signuppage():
    return render_template('registration.html'), 200

@app.route('/login')
def loginpage():
    return render_template('login.html'), 200

@app.route('/home')
def homepage():
    return render_template('home.html'), 200

@app.route('/edit')
def editpage():
    return render_template('edit.html'), 200

@app.route('/userprofile')
@jwt_required
def profilepage():
    return render_template('profile.html'), 200
