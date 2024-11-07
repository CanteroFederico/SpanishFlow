from flask import Flask

application = Flask(__name__)

from capp.home.routes import home
from capp.business.routes import business
from capp.spanishflow_app.routes import spanishflow_app




application.register_blueprint(home)
application.register_blueprint(business)
application.register_blueprint(spanishflow_app)


