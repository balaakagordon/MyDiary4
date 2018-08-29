from flask import Flask, jsonify, json, request, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)


from mydiary import app, app_db, now_time, jwt


@app.route('/')
def landing():
    """ This endpoint helps to load the landing page """
    return render_template('templates/index.html')
    # return jsonify({"message": "welcome"}), 200

@app.route('/login')
def welcome():
    return render_template('templates/login.html')