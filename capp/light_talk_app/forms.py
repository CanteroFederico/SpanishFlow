from flask_wtf import FlaskForm
from wtforms import  SubmitField,  SelectField,  FloatField, StringField
from wtforms.validators import InputRequired

class AddForm(FlaskForm):
  incorrect_sentence = StringField('Frase Incorrecta', [InputRequired()])
  correct_sentence_one = StringField('Frase Correcta 1', [InputRequired()], default="none")
  correct_sentence_two = StringField('Frase Correcta 2', [InputRequired()], default="none")
  correct_sentence_three = StringField('Frase Correcta 3', [InputRequired()], default="none")
  objective = SelectField('Objetivo', [InputRequired()], 
    choices=[('Genero', 'Genero'), ('Número', 'Número')])
  source = SelectField('Fuente', [InputRequired()], 
    choices=[('Inteligencia Artificial', 'Inteligencia Artificial'), ('Persona', 'Persona'), ('Lingüista', 'Lingüista')])
  submit = SubmitField('Añadir')

class SelectForm(FlaskForm):
  objective = SelectField('Objetivo', [InputRequired()], 
    choices=[('Genero', 'Genero'), ('Número', 'Número'), ('Otro', 'Otro')])
  source = SelectField('Fuente', [InputRequired()], 
    choices=[('Inteligencia Artificial', 'Inteligencia Artificial'), ('Persona', 'Persona'), ('Lingüista', 'Lingüista')])
  submit = SubmitField('Seleccionar')

class VerifyForm1(FlaskForm):
  incorrect_sentence = StringField('Frase Incorrecta', [InputRequired()])
  your_sentence = StringField('¿Cuál es la frase correcta?', [InputRequired()])
  objective = StringField('Objetivo', [InputRequired()])
  source = StringField('Fuente', [InputRequired()])
  submit = SubmitField('Verifica')

class VerifyForm2One(FlaskForm):
  incorrect_sentence = StringField('Frase Incorrecta', [InputRequired()])
  correct_sentence_one = StringField('Frase Correcta', [InputRequired()])
  your_sentence = StringField('Tu frase es:', [InputRequired()])
  result_string = StringField('Resultado:', [InputRequired()])
  objective = StringField('Objetivo', [InputRequired()])
  source = StringField('Fuente', [InputRequired()])

class VerifyForm2Two(FlaskForm):
  incorrect_sentence = StringField('Frase Incorrecta', [InputRequired()])
  correct_sentence_one = StringField('Frase Correcta 1', [InputRequired()])
  correct_sentence_two = StringField('Frase Correcta 2', [InputRequired()])
  your_sentence = StringField('Tu frase es:', [InputRequired()])
  result_string = StringField('Resultado:', [InputRequired()])
  objective = StringField('Objetivo', [InputRequired()])
  source = StringField('Fuente', [InputRequired()])

class VerifyForm2Three(FlaskForm):
  incorrect_sentence = StringField('Frase Incorrecta', [InputRequired()])
  correct_sentence_one = StringField('Frase Correcta 1', [InputRequired()])
  correct_sentence_two = StringField('Frase Correcta 2', [InputRequired()])
  correct_sentence_three = StringField('Frase Correcta 3', [InputRequired()])
  your_sentence = StringField('Tu frase es:', [InputRequired()])
  result_string = StringField('Resultado:', [InputRequired()])
  objective = StringField('Objetivo', [InputRequired()])
  source = StringField('Fuente', [InputRequired()])
