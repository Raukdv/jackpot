import requests as rq
from django.test import TestCase

class TestAccount(TestCase):
    def setUp(self):
        self.signup_data = {
            'email':'test@gmail.com',
            'password1':'test010203',
            'password2':'test010203',
            'first_name':'Test',
            'last_name':'User'
        }
    
        self.fake_response = rq.post('http://127.0.0.1:8000/api/account/signup/', data=self.signup_data)
        
        self.login_data = {
            'email':'test@gmail.com',
            'password': 'test010203'
        }

    def test_failed_signup(self):
        expected_dict = {'email': ['A user with that email already exists.']}
        
        response = rq.post('http://127.0.0.1:8000/api/account/signup/', data=self.signup_data)
        json_response = response.json()

        self.assertDictEqual(expected_dict, json_response)

    def test_login(self):
        response = rq.post('http://127.0.0.1:8000/api/account/login/', data=self.login_data)
        json_response = response.json()

        self.assert_('refresh' in json_response)
        self.assert_('access' in json_response)