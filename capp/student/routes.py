from flask import render_template, Blueprint

student=Blueprint('student',__name__)


@student.route('/student')
def student_home():
    return render_template('student.html', title= 'student')