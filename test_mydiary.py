"""
Contains the tests for the apis
"""
from flask import json, jsonify
import unittest
import os

from mydiary import app, now_time
from mydiary.db import MyDiaryDatabase


test_user_1 = {
			"name": "first user",
			"email": "firstuser@email.com",
			"password": "password",
			"confirmpassword": "password"
}

test_user_2 = {
			"name": "second user",
			"email": "seconduser@email.com",
			"password": "password",
			"confirmpassword": "password"
}

test_user_5 = {
			"name": "fifth user",
			"email": "fifthuser@email.com",
			"password": "password",
			"confirmpassword": "password"
}

test_user_6 = {
			"name": "sixth user",
			"email": "sixthuser@email.com",
			"password": "password",
			"confirmpassword": "password"
}

test_entry_1 = {
			"entrydata": "Test Entry Title 1",
			"entrytitle": "This is the first entry for my tests"
}

test_entry_2 = {
			"entrydata": "Test Entry Title 2",
			"entrytitle": "This is the second entry for my tests"
}

test_entry_3 = {
			"entrydata": "Test Entry Title 3",
			"entrytitle": "This is the third entry for my tests"
}

def userInputFields(name, email, password, confirmpassword):
	test_user = {
				name: "third user",
				email: "thirduser@email.com",
				password: "password",
				confirmpassword: "password"
	}
	return test_user

def userInputFields2(email, password):
	test_user = {
				email: "firstuser@email.com",
				password: "password"
	}
	return test_user

def userCreds(name, email, password, password2):
	test_user = {
				"name": name,
				"email": email,
				"password": password,
				"confirmpassword": password2
	}
	return test_user

def userCreds2(email, password):
	login_details = {
				"email": email,
				"password": password
	}
	return login_details

def entryInputFields(entrydata, entrytitle):
	test_user = {
				entrydata: "Test Entry Title 3",
				entrytitle: "This is the third entry for my tests"
	}
	return test_user


def entryData(entrydata, entrytitle):
	test_user = {
				"entrydata": "firstuser@email.com",
				"entrytitle": "password"
	}
	return test_user


class Test_apis(unittest.TestCase):
    """ This class holds all api tests  """


    def setUp(self):
        os.environ["db_name"] = "testdb"
        pass
    
    def entryTestPrep(self, tester, testuser):
        response = tester.post('/auth/signup',\
                        data=json.dumps(testuser), \
                        content_type='application/json')
        response2 = tester.post('/auth/login', \
                        data=json.dumps(testuser), \
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        return mytoken
    	

    def test_user_registration(self):
    	""" Test registers a test user successfully """
    	tester = app.test_client(self)
        response_reg = tester.post('/auth/signup',\
                        data=json.dumps(test_user_1), \
                        content_type='application/json')
        self.assertEqual(response_reg.status_code, 201)
    
    def test_registration_not_json(self):
    	""" Test checks response when request isn't in json format """
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=(test_user_2), \
                        content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_registration_no_name_field(self):
    	""" Test checks response when "name" field isn't included """
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userInputFields(
                        	"", "email", "password", "confirmpassword")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter your name', str(response.data))

    def test_registration_no_email_field(self):
    	""" Test checks response when "email" field isn't included """
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userInputFields(
                        	"name", "", "password", "confirmpassword")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter your email address', str(response.data))

    def test_registration_no_password_field(self):
    	""" Test checks response when "password" field isn't included """
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userInputFields(
                        	"name", "email", "", "confirmpassword")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter your password', str(response.data))

    def test_registration_no_password_confirm_field(self):
    	""" Test checks response when "password" field isn't included """
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userInputFields(
                        	"name", "email", "password", "")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please confirm your password', str(response.data))

    def test_registration_user_already_exits(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(test_user_2), \
                        content_type='application/json')
        response2 = tester.post('/auth/signup',\
                        data=json.dumps(test_user_2), \
                        content_type='application/json')
        self.assertEqual(response2.status_code, 409)
        self.assertIn('This user already exists!', str(response2.data))
                        
    def test_registration_invalid_names(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userCreds(
                        	"t u", "thirduser@email.com", "password", "password")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid first and last name', str(response.data))

    def test_registration_only_one_name_given(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userCreds(
                        	"third", "thirduser@email.com", "password", "password")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid first and last name', str(response.data))

    def test_registration_invalid_name_3(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userCreds(
                        	"third us!er", "thirduser@email.com", "password", "password")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid character. Please enter a valid first and last name', str(response.data))

    def test_registration_invalid_email(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userCreds(
                        	"third user", "thirduseremail.com", "password", "password")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid email address', str(response.data))
    
    def test_registration_invalid_password(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps(userCreds(
                        	"third user", "thirduser@email.com", "pw", "pw")), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 411)
        self.assertIn('Password too short', str(response.data))

    def test_login_wrong_password(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login', \
                        data=json.dumps(userCreds2("firstuser@email.com", "wrongpassword")), \
                        content_type='application/json')
        self.assertIn('Sorry, incorrect credentials', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_login_no_account(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login', \
                        data=json.dumps(userCreds2("thirduser@email.com", "password")), \
                        content_type='application/json')
        self.assertIn('Sorry, incorrect credentials', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_login_no_email_field(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login', \
                        data=json.dumps(userInputFields2("", "password")), \
                        content_type='application/json')
        self.assertIn('Cannot find email. Please provide valid login credentials', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_login_no_password_field(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login', \
                        data=json.dumps(userInputFields2("email", "")), \
                        content_type='application/json')
        self.assertIn('Cannot find password. Please provide valid login credentials', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_login_successful(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps(test_user_2), \
                        content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        response2 = tester.post('/auth/login', \
                        data=json.dumps(test_user_2), \
                        content_type='application/json')
        self.assertIn('access_token', str(response2.data))
        self.assertEqual(response2.status_code, 200)

    def test_add_new_entry(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps(test_entry_1),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertIn('Entry added successfully', str(response3.data))
        self.assertEqual(response3.status_code, 201)
 
    def test_add_new_entry_wrong_data_format(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps(test_entry_3),\
                        content_type='html/text',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('please input json data', str(response3.data))

    def test_add_new_entry_no_entrydata_field(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps(entryInputFields("", "entrytitle")),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('Please enter a title', str(response3.data))

    def test_add_new_entry_no_entrytitle_field(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps(entryInputFields("entrydata", "")),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('Cannot find diary title', str(response3.data))
        
    def test_add_new_entry_repeated_entry(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response1 = tester.post('/api/v1/entries',\
                        data=json.dumps(test_entry_2),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response1.status_code, 201)
        response2 = tester.post('/api/v1/entries',\
                        data=json.dumps(test_entry_2),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response2.status_code, 409)
        self.assertIn('Entry already exists', str(response2.data))

    def test_get_one_entry(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response2 = tester.get('/api/v1/entries/1',\
                        content_type='application/json', \
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertIn('This is the first entry for my tests', str(response2.data))
        self.assertEqual(response2.status_code, 200)

    def test_get_one_entry_non_existent_entry_id(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response = tester.get('/api/v1/entries/5',\
                    content_type='application/json', \
                    headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertIn('The specified entry cannot be found', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_get_all_entries(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_5)
        response = tester.get('/api/v1/entries',\
                        content_type='application/json', \
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response.status_code, 200)
        self.assertIn('This is the first entry for my tests', str(response.data))
        self.assertIn('This is the second entry for my tests', str(response.data))

    def test_edit_entry_data(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        mytoken = self.entryTestPrep(tester, test_user_6)
        response1 = tester.post('/api/v1/entries',
                        data=json.dumps(test_entry_1),
                        content_type='application/json',
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response1.status_code, 201)
        response = tester.put('/api/v1/entries/3',
                        data=json.dumps({"entrydata": "Testing the put method",
                        "entrytitle": "Test Entry Title 1"}),
                        content_type='application/json',
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Testing the put method', str(response.data))
        self.assertNotIn("This is the first entry for my tests", str(response.data))

if __name__ == '__main__':
    #setUp()
    unittest.main()
