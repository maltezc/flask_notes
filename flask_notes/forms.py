
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Sets up form for user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """Form for just CSRF Protection"""

class AddNoteForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = title = StringField("Content", validators=[InputRequired()])
