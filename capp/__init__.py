from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

application = Flask(__name__)

### Secret Key GitHub
# application.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

### Secret Key Computer
application.config['SECRET_KEY'] = '3oueqkfdfas8ruewqndr8ewrewrouewrere44554'

# Base de datos GitHub
DBVAR = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"

application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR 
application.config['SQLALCHEMY_BINDS'] ={'sentence': DBVAR}
db = SQLAlchemy(application)


## Base de datos ordenador
#DBVAR = 'sqlite:///user.db'
#application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR
#application.config['SQLALCHEMY_BINDS'] ={'sentence': 'sqlite:///sentence_table.db'}
#db = SQLAlchemy(application)

# Bcrypt
bcrypt = Bcrypt(application)

# Login
login_manager= LoginManager(application)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from capp.home.routes import home
from capp.business.routes import business
from capp.light_talk_app.routes import light_talk_app
from capp.users.routes import users

application.register_blueprint(home)
application.register_blueprint(business)
application.register_blueprint(light_talk_app)
application.register_blueprint(users)

