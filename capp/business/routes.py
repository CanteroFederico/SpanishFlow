from flask import render_template, Blueprint

business=Blueprint('business',__name__)

@business.route('/business')
def business_home():
  return render_template('business.html', title='business')