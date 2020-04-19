from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, PasswordField,BooleanField
from wtforms.fields.html5 import EmailField

from fight_booking.model import UserReister


class FormRegister(Form):
    """依照Model來建置相對應的Form

    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(5, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(8, 20),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')


    def validate_email(self, field):
        if UserReister.query.filter_by(user_email=field.data).first():
            raise validators.ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if UserReister.query.filter_by(user_username=field.data).first():
            raise  validators.ValidationError('UserName already register by somebody')

class FormLogin(Form):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')

class FormChangePWD(Form):
    """
    使用者變更密碼
    舊密碼、新密碼與新密碼確認
    """
    #  舊密碼
    password_old = PasswordField('Now PassWord', validators=[
        validators.DataRequired()
    ])
    #  新密碼
    password_new = PasswordField('New PassWord', validators=[
        validators.DataRequired(),
        validators.Length(8, 20),
        validators.EqualTo('password_new_confirm', message='PASSWORD NEED MATCH')
    ])
    #  新密碼確認
    password_new_confirm = PasswordField('New Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Change Password')

class FormResetPasswordMail(Form):
    """應用於密碼遺失申請時輸入郵件使用"""
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])
    submit = SubmitField('Send Confirm EMAIL')

    def validate_email(self, field):
        """
        驗證是否有相關的EMAIL在資料庫內，若沒有就不寄信
        """
        if not UserReister.query.filter_by(user_email=field.data).first():
            raise validators.ValidationError('No Such EMAIL, Please Check!')

class FormResetPassword(Form):
    """使用者申請遺失密碼"""
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_confirm', message='PASSWORD NEED MATCH')
    ])
    password_confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Reset Password')
