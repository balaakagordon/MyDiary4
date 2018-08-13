# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime

from .models import MyDiary, Entries
from mydiary import app, app_db, now_time


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
    return [user_name, user_email, user_password]


@app.route('/auth/signup', methods=['GET', 'POST'])
def register():
    """ This method accepts user information to create a profile """
    if request.method == 'POST':
        input_error = False
        if not request.json:
            error_msg = "invalid data type"
            input_error = True
        elif 'email' not in request.json:
            error_msg = "Please provide an email address"
            input_error = True
        elif 'name' not in request.json:
            error_msg = "Please provide a name for the user"
            input_error = True
        elif 'password' not in request.json:
            error_msg = "Please provide a user password"
            input_error = True
        if input_error:
            return jsonify({"Input error": error_msg}), 400
        data = request.get_json()
        signup_data = reg_validation(data)
        if signup_data[0] == "error":
            return jsonify({"Invalid input": signup_data[1]}), signup_data[2]
        add_user = my_diary_object.addUser(signup_data[0], signup_data[1], signup_data[2])
        if add_user == "Added successfully":
            user = {
                'name':signup_data[0],
                'email':signup_data[1],
            }
            return jsonify({"user":user}), 201
        return jsonify({"message": add_user}), 409

""" links to the login page """
@app.route('/auth/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        if not request.json:
            return jsonify({"input error": "Wrong input data format"}), 401
        if 'email' not in request.json:
            return jsonify({"input error": "Cannot find email. Please provide valid login credentials"}), 400
        if 'password' not in request.json:
            return jsonify({"input error": "Cannot find password. Please provide valid login credentials"}), 400
        login_email=request.json.get('email', "")
        login_password=request.json.get('password', "")
        logged_in = my_diary_object.userLogin(login_email, login_password)
        if type(logged_in) == int:
            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=logged_in, expires_delta=expires)
            return json.dumps({"access_token": access_token}), 200
        return jsonify({'login' : logged_in}), 401
