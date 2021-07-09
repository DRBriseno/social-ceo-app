# Create your tests here.

from unittest import TestCase
from datetime import date
from social_ceo_app import app, db, bcrypt
from social_ceo_app.models import Business_Name, State, User
"""
Run these tests with the command:
python3 -m unittest social_ceo_app.auth.tests
"""

#################################################
# Setup
#################################################


def create_states():
    # business_name and state required to create a user
    bnA = Business_Name(name='Boss Babe Inc.')
    stA = State(name='California',
                     address='555 Hollywood Blvd., Los Angeles', business_name=bnA)

    db.session.add(bnA)
    db.session.add(stA)
    db.session.commit()


def create_user():
   # user >> state 
    st_A = State.query.filter_by(name='California').one()

    first_user_obj = {
        'email': 'blahblahblah@ceo.com',
        'password': 'first_password1234',
        'full_name': 'test_A',
        'birthdate': date(1986, 3, 22),
        'state_id': st_A.id,
        'position': 'founder'
    }

    first_password_hash_A = bcrypt.generate_password_hash(
        first_user_obj['password']).decode('utf-8')
    first_user_obj['password'] = first_password_hash_A

    user = User(
        email=first_user_obj['email'],
        password=first_user_obj['password'],
        name=first_user_obj['full_name'],
        dob=first_user_obj['birthdate'],
        state_id=first_user_obj['state_id'],
        position=first_user_obj['position']
    )
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class AuthTests(TestCase):
    """(login & signup)"""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        create_states()
        bnA = Business_Name.query.filter_by(name='Boss Babes Inc.').one()
        stA = State.query.filter_by(name='California').one()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234',
            'confirm_password': 'first_password1234',
            'full_name': 'test_A',
            'birthdate': date(1986, 3, 22),
            'business_name': bnA.id,
            'state': stA.id,
            'position': 'founder'
        }

        self.app.post('/signup', data=data)

        user = User.query.filter_by(email='blahblahblah@ceo.com').first()

        self.assertIsNotNone(user)
        self.assertEqual('blahblahblah@ceo.com', user.email)

    def test_signup_existing_user(self):
        create_states()
        bnA = Business_Name.query.filter_by(name='Boss Babe Inc.').one()
        stA = State.query.filter_by(name='California').one()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234',
            'confirm_password': 'first_password1234',
            'full_name': 'test_A',
            'birthdate': date(1986, 3, 22),
            'business_name': bnA.id,
            'state': stA.id,
            'position': 'founder'
        }

        self.app.post('/signup', data=data)

        response = self.app.post('/signup', data=data)
        response_text = response.get_data(as_text=True)

        self.assertIn(
            'It appears this email is attached to another account. Please use another email.', response_text)

    def test_login_correct_password(self):
      
        create_states()
        create_user()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234'
        }

        response = self.app.post(
            '/login', data=data,  follow_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertNotIn('Log In', response_text)
        self.assertIn('Profile', response_text)

    def test_login_nonexistent_user(self):
        create_states()
        create_user()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234',
        }

        sta = self.app.post('/login', data=data,  follow_redirects=True)
        sta_text = sta.get_data(as_text=True)

        self.assertNotIn('Log Out', sta_text)
        self.assertIn('User does not exist.', sta_text)

    def test_login_incorrect_password(self):
        create_states()
        create_user()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234',
        }

        sta = self.app.post('/login', data=data,  follow_redirects=True)
        sta_text = sta.get_data(as_text=True)

        self.assertNotIn('Log Out', sta_text)
        self.assertIn(
            "Password does not match.", sta_text)

    def test_logout(self):
        create_states()
        create_user()

        data = {
            'email': 'blahblahblah@ceo.com',
            'password': 'first_password1234',
        }

        self.app.post('/login', data=data,  follow_redirects=True)

        sta = self.app.get('/logout', follow_redirects=True)
        sta_text = sta.get_data(as_text=True)
        self.assertIn('Log In', sta_text)