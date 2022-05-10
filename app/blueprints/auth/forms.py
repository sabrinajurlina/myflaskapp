from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User

class LoginForm(FlaskForm):
    email = StringField('Enter Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Password Must Match')])#must equal password]
    submit = SubmitField('Register')

#my avatar is generated with the users initials, so i don't need random int
    # r1=random.randint(1, 1000)
    # r2=random.randint(1001, 2000)
    # r3=random.randint(2001, 3000)
    # r4=random.randint(3001, 4000)

    # icon = f'{first_name} {last_name}'

    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()

        if same_email_user:
            raise ValidationError("That email is already registered. Please use another email or select 'Forgot Password' to reset your password")


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Password Must Match')])#must equal password]
    submit = SubmitField('Update')
    # icon = f'{first_name}+{last_name}'
            