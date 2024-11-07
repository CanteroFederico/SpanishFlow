from flask import render_template, Blueprint

spanishflow_app=Blueprint('spanishflow_app',__name__)


@spanishflow_app.route('/app/spanishflow_app')
def spanishflow_app_home():
    return render_template('/app/spanishflow_app.html', title= 'App')







@spanishflow_app.route('/app/pro/professional')
def professional_home():
    return render_template('/app/pro/professional.html', title= 'professional')

@spanishflow_app.route('/app/pro/professional_words')
def professional_words():
    return render_template('/app/pro/professional_words.html', title= 'professional_words')

@spanishflow_app.route('/app/pro/professional_phrases')
def professional_phrases():
    return render_template('/app/pro/professional_phrases.html', title= 'professional_phrases')

@spanishflow_app.route('/app/pro/professional_conversation')
def professional_conversation():
    return render_template('/app/pro/professional_conversation.html', title= 'professional_conversation')

@spanishflow_app.route('/app/pro/professional_test')
def professional_test():
    return render_template('/app/pro/professional_test.html', title= 'professional_test')






@spanishflow_app.route('/app/stu/student')
def student_home():
    return render_template('/app/stu/student.html', title= 'student')

@spanishflow_app.route('/app/stu/student_words')
def student_words():
    return render_template('/app/stu/student_words.html', title= 'student_words')

@spanishflow_app.route('/app/stu/student_phrases')
def student_phrases():
    return render_template('/app/stu/student_phrases.html', title= 'student_phrases')

@spanishflow_app.route('/app/stu/student_conversation')
def student_conversation():
    return render_template('/app/stu/student_conversation.html', title= 'student_conversation')

@spanishflow_app.route('/app/stu/student_test')
def student_test():
    return render_template('/app/stu/student_test.html', title= 'student_test')





@spanishflow_app.route('/app/tur/turist')
def turist_home():
    return render_template('/app/tur/turist.html', title= 'turist')

@spanishflow_app.route('/app/tur/turist_words')
def turist_words():
    return render_template('/app/tur/turist_words.html', title= 'turist_words')

@spanishflow_app.route('/app/tur/turist_phrases')
def turist_phrases():
    return render_template('/app/tur/turist_phrases.html', title= 'turist_phrases')

@spanishflow_app.route('/app/tur/turist_conversation')
def turist_conversation():
    return render_template('/app/tur/turist_conversation.html', title= 'turist_conversation')

@spanishflow_app.route('/app/tur/turist_test')
def turist_test():
    return render_template('/app/tur/turist_test.html', title= 'turist_test')
