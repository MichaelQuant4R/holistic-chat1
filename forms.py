from flask_wtf import FlaskForm
from wtforms import (BooleanField, SubmitField, StringField,
                     IntegerField, SelectField, TextAreaField,
                     PasswordField)

from wtforms.validators import (DataRequired, Email, EqualTo,
                                Length)


class RegisterForm(FlaskForm):
    
    
    username = StringField("username", validators = [DataRequired(),
                                                     Length(min=3, max=25)],
                           render_kw = {"placeholder": "Enter a username..."})
    
    
    email = StringField("email", validators = [DataRequired(),
                                                     Email(),
                                                     Length(min=10, max=35)],
                           render_kw = {"placeholder": "Enter a email..."})
    
    
    password = PasswordField("password", validators = [DataRequired(),
                                                     Length(min=3, max=25)],
                           render_kw = {"placeholder": "Enter a password..."})
    
    
        
    confirm_password = PasswordField("confirm_password", validators = [DataRequired(),
                                 EqualTo("password", message="Passwords must match!")],
                           render_kw = {"placeholder": "Enter a confirm password..."})
    
    submit = SubmitField("Sign up")
    
    
    
class LoginForm(FlaskForm):
    
    email = StringField("email", validators = [DataRequired(),
                                                     Email(),
                                                     Length(min=10, max=35)],
                           render_kw = {"placeholder": "Enter your email..."})
    
    
    password = PasswordField("password", validators = [DataRequired(),
                                                     Length(min=3, max=25)],
                           render_kw = {"placeholder": "Enter your password..."})
    
    

    submit = SubmitField("Sign in")
    
    
    
class ChatRoomForm(FlaskForm):
    
    
    rooms = SelectField(choices = [("Python", "Python"),
                                   ("Javascript", "Javascript"),
                                   ("Java", "Java"),
                                   ("C#", "C#"),
                                   ("CSS", "CSS"),],
                        default = ("C++", "C++"))
    


    room = SubmitField("Room")
    
    