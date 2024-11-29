from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os, logging

logging.basicConfig(level=logging.INFO)
application = Flask(__name__)

### Secret Key GitHub
# application.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

### Secret Key Computer
application.config['SECRET_KEY'] = 'c131b9e6952a36ead01aadafd3b500d3'

# Base de datos GitHub
DBVAR = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"

application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR 
application.config['SQLALCHEMY_BINDS'] ={'sentence': DBVAR}
db = SQLAlchemy(application)


# Flask app configuration
#DBVAR = 'sqlite:///user.db'
#application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR  # Principal base de datos (sentences)
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilitar seguimiento de modificaciones



# Inicialización de la base de datos
db = SQLAlchemy(application)



# Bcrypt
bcrypt = Bcrypt(application)

# Login User
login_manager = LoginManager(application)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# Login Admin
admin = Admin(application, name='Admin', template_mode='bootstrap3')

from capp.admin_bp.routes import admin_bp
from capp.business.routes import business
from capp.home.routes import home
from capp.spanishflow_app.routes import spanishflow_app
from capp.users.routes import users

# Blueprint Registration
application.register_blueprint(admin_bp)
application.register_blueprint(business)
application.register_blueprint(home)
application.register_blueprint(spanishflow_app)
application.register_blueprint(users)


class CustomAdminModelView(ModelView):
    """Custom AdminModelView with extended functionality."""
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    def __init__(self, model, session, **kwargs):
        # Dynamically configure searchable fields based on the model
        if model.__name__ == "User":
            self.column_searchable_list = ['username', 'email']
        elif model.__name__ == "Category":
            self.column_searchable_list = ['name']
        elif model.__name__ == "Section":
            self.column_searchable_list = ['name', 'description']  # Adjust fields for Section
        elif model.__name__ == "Sentence":
            self.column_searchable_list = ['english_sentence', 'spanish_sentence']
        super().__init__(model, session, **kwargs)

from capp.models import User, Category, Section, Sentence

admin.add_view(CustomAdminModelView(User, db.session, name='Users'))
admin.add_view(CustomAdminModelView(Category, db.session, name='Categories'))
admin.add_view(CustomAdminModelView(Section, db.session, name='Sections'))
admin.add_view(CustomAdminModelView(Sentence, db.session, name='Sentences'))

