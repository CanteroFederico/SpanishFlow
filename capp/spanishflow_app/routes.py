from flask import render_template, Blueprint

spanishflow_app=Blueprint('spanishflow_app',__name__)


@spanishflow_app.route('/spanishflow_app')
def spanishflow_app_home():
    return render_template('spanishflow_app.html', title= 'App')
