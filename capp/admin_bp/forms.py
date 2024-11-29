from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminModelView(ModelView):
    def is_accessible(self):
        # Only allow access if the current user is authenticated and an admin
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect non-admin users to the login page
        return redirect(url_for('admin_bp.admin_dashboard'))

# Admin Login Form
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
# Category Form for adding categories
class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

# Add Section Form for adding sections under categories
class AddSectionForm(FlaskForm):
    section_name = StringField('Section Name', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    icon = StringField('Font Awesome Icon Class')
    submit = SubmitField('Add Section')

# Add Sentence Form
class AddSentenceForm(FlaskForm):
    english_sentence = StringField('English Sentence', validators=[DataRequired()])
    spanish_sentence = StringField('Spanish Sentence', validators=[DataRequired()])
    explanation_english = StringField('Explanation (English)', validators=[DataRequired()])
    explanation_spanish = StringField('Explanation (Spanish)', validators=[DataRequired()])
    image_path = StringField('Image Path (optional)', validators=[Optional()])
    category = SelectField('Select Category', coerce=int, validators=[DataRequired()])
    section = SelectField('Select Section', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Sentence')




