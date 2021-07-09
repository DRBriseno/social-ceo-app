from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#auth/__init__.py

#import sys
#sys.path.insert(1,"..")    # Directly add this pathway to current file's lookup
#from ..config import Config
#import config 
#import Config
#import config.Config

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from .. import config
print("The value of config.count is {0}".format(config.count))


#from ... import Config
#from social_ceo_app.config import Config
import os


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

def create_app(config):
    app = Flask(__name__)
    db.init_app(app)

   

###########################
# Authentication
###########################

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


#import sys
#sys.path.insert(1, '.')
from . import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

    

bcrypt = Bcrypt(app)

###########################
# Blueprints
###########################

from social_ceo_app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from social_ceo_app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()
