from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from conceptb.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Home Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        num = phone.data
        if num.startswith('+'):
            num = num[1:]
        if num.isnumeric() == False:
            raise ValidationError('That phone number is invalid. Please verify it.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    location = StringField('Home Address', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        num = phone.data
        if num.startswith('+'):
            num = num[1:]
        if num.isnumeric() == False:
            raise ValidationError('That phone number is invalid. Please verify it.')

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price in USD', validators=[DataRequired()])
    image = FileField('Image :', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add product')

class ConfirmOrderForm(FlaskForm):
    location = StringField('Your address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_phone(self, phone):
        num = phone.data
        if num.startswith('+'):
            num = num[1:]
        if num.isnumeric() == False:
            raise ValidationError('That phone number is invalid. Please verify it.')