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
    # return jsonify({"message": "welcome"}), 200

@app.route('/signup')
def signuppage():
    return render_template('registration.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/home')
@jwt_required
def homepage():
    return render_template('home.html')

@app.route('/edit')
@jwt_required
def editpage():
    return render_template('edit.html')

@app.route('/userprofile')
@jwt_required
def profilepage():
    return render_template('profile.html')