from flask import render_template, Blueprint

turist=Blueprint('turist',__name__)


@turist.route('/turist')
def turist_home():
    return render_template('turist.html', title= 'turist')