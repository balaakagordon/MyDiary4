"""
Contains the tests for the apis
"""
from flask import json, jsonify
import unittest
import os

from mydiary import app, now_time
from mydiary.db import MyDiaryDatabase


def setUp():
    os.environ["db_name"] = "testdb"
    pass

class Test_apis(unittest.TestCase):
    """ This class holds all api tests  """

    def test_registration_successful(self):
        tester = app.test_client(self)
        response_reg = tester.post('/auth/signup',\
                        data=json.dumps({"name": "regtest user",\
                        "email": "email@regtest1.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response_reg.status_code, 201)
    
    def test_registration_not_json(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data={"name": "test user",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}, \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_no_name_field(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"nme": "test user",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_no_email_field(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "em": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_no_password_field(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@test.com", \
                        "pass":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_registration_user_already_exits(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        response2 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response2.status_code, 409)
        self.assertIn('This user already exists!', str(response2.data))
                        
    def test_registration_invalid_name(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "t u",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid first and last name', str(response.data))

    def test_registration_invalid_name_2(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid first and last name', str(response.data))

    def test_registration_invalid_name_3(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test us!er",\
                        "email": "email@test.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid character. Please enter a valid first and last name', str(response.data))

    def test_registration_invalid_email(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "emailtest.com", \
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a valid email address', str(response.data))
    
    def test_registration_invalid_password(self):
        tester = app.test_client(self)
        response = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@test.com", \
                        "password":"pas",
                        "confirmpassword":"pas"}), \
                        content_type='application/json')
        self.assertEqual(response.status_code, 411)
        self.assertIn('Password too short', str(response.data))

    def test_login_successful(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup', \
                        data=json.dumps({"name": "logtest user",\
                        "email": "email@logtest1.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        response2 = tester.post('/auth/login', \
                        data=json.dumps({"email": "email@logtest1.com",\
                        "password":"testpass"}), \
                        content_type='application/json')
        self.assertIn('access_token', str(response2.data))
        self.assertEqual(response2.status_code, 200)

    def test_login_wrong_password(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup', \
                        data=json.dumps({"name": "logtest user",\
                        "email": "email@logtest2.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        response2 = tester.post('/auth/login', \
                        data=json.dumps({"email": "email@logtest2.com",\
                        "password":"wrongpass"}), \
                        content_type='application/json')
        self.assertIn('Sorry, incorrect credentials', str(response2.data))
        self.assertEqual(response2.status_code, 401)

    def test_login_no_account(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login', \
                        data='{"email": "email@logtest3.com",\
                        "password":"testpass"}', \
                        content_type='application/json')
        self.assertIn('Sorry, incorrect credentials', str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_login_no_email_field(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup', \
                        data=json.dumps({"name": "logtest user",\
                        "email": "email@logtest4.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        response2 = tester.post('/auth/login', \
                        data=json.dumps({"eml": "email@logtest4.com",\
                        "password":"testpass"}), \
                        content_type='application/json')
        self.assertIn('Cannot find email. Please provide valid login credentials', str(response2.data))
        self.assertEqual(response2.status_code, 400)

    def test_login_no_password_field(self):
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup', \
                        data=json.dumps({"name": "logtest user",\
                        "email": "email@logtest5.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}), \
                        content_type='application/json')
        response2 = tester.post('/auth/login', \
                        data=json.dumps({"email": "email@logtest5.com",\
                        "pass":"testpass"}), \
                        content_type='application/json')
        self.assertIn('Cannot find password. Please provide valid login credentials', str(response2.data))
        self.assertEqual(response2.status_code, 400)

    def test_add_new_entry(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@addtest1.com",\
                        "password": "testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@addtest1.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for adding a new entry",\
                        "entrytitle": "New entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 201)
 
    def test_add_new_entry_wrong_data_format(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@addtest2.com",\
                        "password": "testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@addtest2.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for adding a new entry in the wrong format",\
                        "entrytitle": "New entry test"}),\
                        content_type='html/text',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('please input json data', str(response3.data))

    def test_add_new_entry_no_entrydata_field(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@addtest3.com",\
                        "password": "testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@addtest3.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"data": "Test for adding a new entry",\
                        "entrytitle": "New entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('Please enter a title', str(response3.data))

    def test_add_new_entry_no_entrytitle_field(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@addtest4.com",\
                        "password": "testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@addtest4.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for adding a new entry",\
                        "title": "New entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 400)
        self.assertIn('Cannot find diary title', str(response3.data))
        
    def test_add_new_entry_repeated_entry(self):
        """ a test for the status code returned by the post method """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@addtest5.com",\
                        "password": "testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@addtest5.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for repeating an entry",\
                        "entrytitle": "New entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        response4 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for repeating an entry",\
                        "entrytitle": "New entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response4.status_code, 409)
        self.assertIn('Entry already exists', str(response4.data))

    def test_get_one_entry(self):
        """ a test for the data returned by the get method and an index """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@gettest1.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@gettest1.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "Test for returning a single entry",\
                        "entrytitle": "Get entry test"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        response4 = tester.get('/api/v1/entries/6',\
                        content_type='application/json', \
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertIn('Test for returning a single entry', str(response4.data))
        self.assertEqual(response4.status_code, 200)

    def test_get_all_entries_data_no_entries(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@getalltest2.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@getalltest2.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.get('/api/v1/entries',\
                        content_type='application/json', \
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response3.status_code, 200)

    def test_get_one_entry_non_existent_entry_id(self):
            """ a test for the data returned by the get method and an index """
            tester = app.test_client(self)
            response1 = tester.post('/auth/signup',\
                            data=json.dumps({"name": "test user",\
                            "email": "email@gettest2.com",
                            "password":"testpass",
                            "confirmpassword":"testpass"}),\
                            content_type='application/json')
            response2 = tester.post('/auth/login',\
                            data=json.dumps({"email": "email@gettest2.com",\
                            "password":"testpass"}),\
                            content_type='application/json')
            tokendata = json.loads(response2.data)
            mytoken = tokendata["access_token"]
            response3 = tester.post('/api/v1/entries',\
                            data=json.dumps({"entrydata": "Test for returning a single entry with invalid id",\
                            "entrytitle": "Get entry test"}),\
                            content_type='application/json',\
                            headers={"authorization": 'Bearer ' + str(mytoken)})
            response4 = tester.get('/api/v1/entries/6798',\
                            content_type='application/json', \
                            headers={"authorization": 'Bearer ' + str(mytoken)})
            self.assertIn('The specified entry cannot be found', str(response4.data))
            self.assertEqual(response4.status_code, 400)

    def test_get_all_entries_data(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@get1.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@get1.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "test getting all entries",\
                        "entrytitle": "test get method"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        response4 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "test getting all user entries",\
                        "entrytitle": "test get method again"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        response5 = tester.get('/api/v1/entries',\
                        content_type='application/json', \
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response5.status_code, 200)
        self.assertIn('test getting all entries', str(response5.data))
        self.assertIn('test getting all user entries', str(response5.data))

    def test_edit_entry_data(self):
        """ a test for the data returned by the get method and no entry index """
        tester = app.test_client(self)
        response1 = tester.post('/auth/signup',\
                        data=json.dumps({"name": "test user",\
                        "email": "email@getalltest2.com",
                        "password":"testpass",
                        "confirmpassword":"testpass"}),\
                        content_type='application/json')
        response2 = tester.post('/auth/login',\
                        data=json.dumps({"email": "email@getalltest2.com",\
                        "password":"testpass"}),\
                        content_type='application/json')
        tokendata = json.loads(response2.data)
        mytoken = tokendata["access_token"]
        response3 = tester.post('/api/v1/entries',\
                        data=json.dumps({"entrydata": "initial put test data",\
                        "entrytitle": "test put method"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        response4 = tester.put('/api/v1/entries/3',\
                        data=json.dumps({"entrydata": "test editing an entry",\
                        "entrytitle": "test put method"}),\
                        content_type='application/json',\
                        headers={"authorization": 'Bearer ' + str(mytoken)})
        self.assertEqual(response4.status_code, 201)
        self.assertIn('test editing an entry', str(response4.data))
        self.assertNotIn("initial put test data", str(response4.data))
    

if __name__ == '__main__':
    #setUp()
    unittest.main()
