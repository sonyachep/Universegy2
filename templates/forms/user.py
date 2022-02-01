from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    style = {'class': 'ourClasses',
             'style': 'width: 80%; margin-bottom: 25px; height: 40px !important; border-radius: 5px; outline: 0; -moz-outline-style: none; background: white;'}
    style_btn = {'class': 'ourClasses',
                 'style': 'color: rgb(82, 82, 122); background-color: rgb(217, 247, 255); border: 1px solid  rgb(82, 82, 122); border-radius: 5px; font-size: 18px; font-weight: 200; cursor: pointer; transition: box-shadow .4s ease;'}
    login = StringField('Логин', validators=[DataRequired()], render_kw=style)
    password = PasswordField('Ключ доступа', validators=[DataRequired()], render_kw=style)
    submit = SubmitField('Войти', render_kw=style_btn)
    remember_me = BooleanField('Запомнить меня')
