from flask import Flask, jsonify, json, request, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)


from mydiary import app, app_db, now_time, jwt


@app.route('/')
def landing():
    """ This endpoint loads the landing page """
    return render_template('index.html')
    # return jsonify({"message": "welcome"}), 200

@app.route('/login')
def login():
    # return jsonify({"message": "welcome"}), 200
    return render_template('login.html')