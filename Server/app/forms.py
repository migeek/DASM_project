from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Family Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BoxRegistrationForm(FlaskForm):
    owner = StringField('Device Owner', validators=[DataRequired()])
    bid = StringField('BOX I.D.', validators=[DataRequired()])
    submit = SubmitField('Register')


class BoxDeletionForm(FlaskForm):
    to_delete = SelectField(label='Box to delete', validators=[DataRequired()],
                            coerce=int)
    submit = SubmitField('Delete')
