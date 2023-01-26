from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
	username = StringField('Username', 
	    validators=[DataRequired(), Length(min=2)])
	password = PasswordField('Password',  
		validators=[DataRequired(), Length(min=2)])
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	username = StringField('Username', 
	    validators=[DataRequired(), Length(min=2)])
	password = PasswordField('Password',  
		validators=[DataRequired(), Length(min=2)])
	submit = SubmitField('Log in')


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[DataRequired()])
    submit = SubmitField("Upload File")