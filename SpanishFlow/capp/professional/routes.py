from flask import render_template, Blueprint

professional=Blueprint('professional',__name__)


@professional.route('/professional')
def professional_home():
    return render_template('professional.html', title= 'professional')