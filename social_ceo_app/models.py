from sqlalchemy.orm import backref
from social_ceo_app import db
from flask_login import UserMixin


class Business_Name(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(80), nullable=False)
  # one-to-many relation
  states = db.relationship('State', back_populates='business_name')

  def __str__(self):
    return f'<Business_Name: {self.full_name}>'

  def __repr__(self):
    return f'<Business_Name: {self.full_name}>'

class State(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(80), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  business_name_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
  # one-to-many relation
  business_name = db.relationship('Business_Name', back_populates='states')
  # one-to-many relation
  users = db.relationship('User', back_populates='state')

  def __str__(self):
    return f'<State: {self.full_name}>'

  def __repr__(self):
    return f'<State: {self.full_name}>'


user_followers = db.Table('user_followers',
    db.Column('user_follower_id', db.Integer, primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  full_name = db.Column(db.String(80), nullable=False)
  status = db.Column(db.String(80), nullable=False, default='Available')
  birthdate = db.Column(db.Date, nullable=False)
  position = db.Column(db.String(80), nullable=False)
  state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
  state = db.relationship('State', back_populates='users')
  current_followers = db.relationship(
  'User',
  secondary=user_followers,
  primaryjoin=id==user_followers.c.following_id,
  secondaryjoin=id==user_followers.c.follower_id,
  backref=backref('following')
  )

  def __str__(self):
        return f'<User: {self.email}>'

  def __repr__(self):
        return f'<User: {self.email}>'
