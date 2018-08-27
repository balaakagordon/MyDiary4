# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import datetime

from .models import MyDiary, Entries
from mydiary import app, app_db, now_time, jwt


my_diary_object = MyDiary()
my_diary_object.user_entries = Entries()


def reg_validation(data):
    """ This method validates user inputs during registration """
    nums = "0123456789"
    invalid_str = ",.;:!][)(><+-=}{"
    user_name=data["name"]
    name_error = False
    if len(user_name) <= 4:
        error_msg = "Please enter a valid first and last name"
        name_error = True
    elif len(user_name.split()) < 2:
        error_msg = "Please enter a valid first and last name"
        name_error = True
    for letter in user_name:
        if letter in invalid_str or letter in nums:
            error_msg = "Invalid character. Please enter a valid first and last name"
            name_error = True
    if name_error:
        return ["error", error_msg, 400]
    user_email=request.json.get('email', "")
    email_error = False
    if "@" not in user_email:
        email_error = True
    elif user_email[0] in invalid_str:
        email_error = True
    if email_error:
        return ["error", "Please enter a valid email address", 400]
    user_password=request.json.get('password', "")
    if len(user_password) <= 5:
        return ["error", "Password too short", 411]
    confirm_password=request.json.get('confirmpassword', "")
    if user_password != confirm_password:
        return ["error", "Passwords do not match", 400]
    return [user_name, user_email, user_password]

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    token = decrypted_token['jti']
    blacklisted = my_diary_object.inBlacklist(token)
    return blacklisted


@app.route('/auth/signup', methods=['GET', 'POST'])
def register():
    """ This method accepts user information to create a profile """
    if request.method == 'POST':
        input_error = False
        if not request.json:
            error_msg = "invalid data type"
            input_error = True
        elif 'email' not in request.json:
            error_msg = "Please enter your email address"
            input_error = True
        elif 'name' not in request.json:
            error_msg = "Please enter your name"
            input_error = True
        elif 'password' not in request.json:
            error_msg = "Please enter your password"
            input_error = True
        elif 'confirmpassword' not in request.json:
            error_msg = "Please confirm your password"
            input_error = True
        if input_error:
            return jsonify({"Input error": error_msg}), 400
        data = request.get_json()
        signup_data = reg_validation(data)
        if signup_data[0] == "error":
            return jsonify({"message": "Invalid input", "error": signup_data[1]}), signup_data[2]
        add_user = my_diary_object.addUser(signup_data[0], signup_data[1], signup_data[2], now_time)
        if add_user == "Registered Successfully!":
            user = {
                'name': signup_data[0],
                'email': signup_data[1],
            }
            return jsonify({"message": add_user, "user": user}), 201
        return jsonify({"message": add_user}), 409

""" links to the login page """
@app.route('/auth/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        input_error = False
        if not request.json:
            input_error = True
            error_msg = "Wrong input data format"
        if 'email' not in request.json:
            input_error = True
            error_msg = "Cannot find email. Please provide valid login credentials"
        if 'password' not in request.json:
            input_error = True
            error_msg = "Cannot find password. Please provide valid login credentials"
        if input_error:
            return jsonify({"input error": error_msg}), 400
        login_email=request.json.get('email', "")
        login_password=request.json.get('password', "")
        user_id = get_jwt_identity()
        logged_in = my_diary_object.userLogin(login_email, login_password, now_time, user_id)
        if type(logged_in) == int:
            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=logged_in, expires_delta=expires)
            return jsonify({"message": "Login successful", "access_token": access_token}), 200
        return jsonify({"message" : logged_in}), 401

@app.route('/profile', methods=['GET'])
@jwt_required
def userProfile():
    user_id = get_jwt_identity()
    userData = my_diary_object.checkUserDetails(user_id)
    return jsonify({"userdata": userData}), 200

@app.route('/logout', methods=['GET'])
@jwt_required
def logout():
    token = get_raw_jwt()['jti']
    user_id = get_jwt_identity()
    logout = my_diary_object.userLogout(token, user_id)
    if logout == "Successfully logged out":
        return jsonify({"msg": logout}), 200
    else:
        return jsonify({"msg": "logout failed"}), 400
