'''This module represents the base test class'''
import json
import unittest

from datetime import datetime

from app import create_app
from app.api.v1.utils.utility import Utility
from app.api.v1.models.meetup_model import MEETUPS
from app.api.v1.models.question_model import QUESTIONS
from app.api.v1.models.user_model import USERS, UserModel

class BaseTestCase(unittest.TestCase):
    '''Base class for other test classes'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.user_registration = dict(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="username",
            is_admin=False,
            password="12345"
        )

        self.admin_registration = dict(
            firstname="admin_first",
            lastname="admin_last",
            email="admin@example.com",
            username="test_admin",
            is_admin=True,
            password="901sT"
        )

        self.digit_username = dict(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="1234",
            is_admin=False,
            password="12345"
        )


        self.empty_username = dict(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="",
            is_admin=False,
            password="12345"
        )

        self.empty_password = dict(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="username",
            is_admin=False,
            password=""
        )

        self.wrong_email_registration = dict(
            firstname="test_first",
            lastname="test_last",
            email="testexample.com",
            username="test",
            is_admin=False,
            password="12345"
        )

        self.user_login = dict(username="username", password="12345")
        self.wrong_password = dict(username="username", password="abcde")

        self.admin_login = dict(username="test_admin", password="901sT")

        self.meetup = dict(
            location="Test Location",
            images=[],
            topic="Test Topic",
            happening_on="Jan 10 2019 3:30PM",
            tags=["Sports", "study"]
        )

        self.new_meetup = dict(
            location="Test New Location",
            images=[],
            topic="Test New Topic",
            happening_on="Jan 15 2019 11:00AM",
            tags=["Sports", "study"]
        )

        self.question = dict(
            title="test title",
            body="test body"
        )

        self.rsvp = dict(response="maybe")

    def tearDown(self):
        del QUESTIONS[:]
        del MEETUPS[:]
        del USERS[:]
        self.app_context.pop()

    def get_accept_content_type_headers(self):
        '''Return the content type headers for the body'''
        content_type = {}
        content_type['Accept'] = 'application/json'
        content_type['Content-Type'] = 'application/json'
        return content_type

    def get_authentication_headers(self, access_token):
        '''Return the authentication header'''
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = "Bearer {}".format(access_token)
        return authentication_headers

    def get_access_token(self, user_registration, user_login):
        '''Fetch access token from user login'''
        self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_registration)
        ) # User Registration
        res = self.client().post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_login)
        ) # User Log In
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        return access_token

    def create_meetup(self, access_token, meetup):
        '''Create a meetup record'''
        self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(meetup)
        )

    def create_question(self, access_token, question):
        '''Create a question record'''
        self.client().post(
            '/api/v1/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(question)
        )

    def test_serialize_function(self):
        '''Test the function serialize() converts an object to a dictionary'''
        user = UserModel(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="username",
            is_admin=False,
            password="12345"
        )
        serialized_user_obj = Utility.serialize(user)
        user_dict = dict(
            firstname="test_first",
            lastname="test_last",
            email="test@example.com",
            username="username",
            is_admin=False,
            password="12345"
        )
        self.assertTrue(serialized_user_obj, user_dict)
        now_date = datetime.utcnow()
        serialized_date = Utility.serialize(now_date)
        self.assertTrue(serialized_date, now_date.isoformat())

if __name__ == "__main__":
    unittest.main()