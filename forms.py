from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField





class SearchPageForm(FlaskForm):
    """ Search pages based on input """
    
    search = StringField('Search Page:')


class LoginUserForm(FlaskForm):
    """ Form to login user """

    username = StringField('Username:')
    password = PasswordField('Password:')



class SignupNewUserForm(FlaskForm):
    """ Form for new user signup """

    username = StringField('Username:')
    password = PasswordField('Password:')