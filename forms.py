from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """ Form to register a new user """

    username = StringField("Username:", validators=[InputRequired(message="This field cannot be left blank")])
    password = PasswordField("Password:", validators=[InputRequired(message="This field cannot be left blank")])
    email = StringField("Email:", validators=[InputRequired(message="This field cannot be left blank")])
    first_name = StringField("First Name:", validators=[InputRequired(message="This field cannot be left blank")])
    last_name = StringField("Last Name:", validators=[InputRequired(message="This field cannot be left blank")])

class LoginForm(FlaskForm):
    """ Form to log in existing user """

    username = StringField("Username:", validators=[InputRequired(message="This field cannot be left blank")])
    password = PasswordField("Password:", validators=[InputRequired(message="This field cannot be left blank")])

class FeedbackForm(FlaskForm):
    """ Form to add/edit feedback """

    title = StringField("Title:", validators=[InputRequired(message="This field cannot be left blank")])
    content = StringField("Content:", validators=[InputRequired(message="This field cannot be left blank")])


