from flask import Flask

application = Flask(__name__)

from capp.home.routes import home
from capp.business.routes import business
from capp.spanishflow_app.routes import spanishflow_app
from capp.turist.routes import turist
from capp.professional.routes import professional
from capp.student.routes import student

application.register_blueprint(home)
application.register_blueprint(business)
application.register_blueprint(spanishflow_app)
application.register_blueprint(student)
application.register_blueprint(turist)
application.register_blueprint(professional)