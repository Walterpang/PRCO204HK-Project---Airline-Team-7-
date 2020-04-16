from fight_booking import app
from fight_booking import db
from flask import render_template,flash, redirect, url_for, request
from fight_booking.model import UserReister
from fight_booking.form import FormRegister , FormLogin
from fight_booking.sendmail import send_mail
from flask_login import login_user, current_user, login_required

@app.route('/register', methods=['GET', 'POST'])
def register():
    form =FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            user_username=form.username.data,
            user_email=form.email.data,
            user_password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        #  產生用戶認證令牌
        token = user.create_confirm_token()
        #  寄出帳號啟動信件
        send_mail(sender='Sender@domain.com',
                  recipients=['recipients@domain.com'],
                  subject='Activate your account',
                  template='mail/welcome',
                  mailtype='html',
                  user=user,
                  token=token)

        return 'Check Your Email and Activate Your Account'
    return render_template('register.html', form=form)

@app.route('/user_confirm/<token>')
def user_confirm(token):
    user = UserReister()
    data = user.validate_confirm_token(token)
    if data:
        user = UserReister.query.filter_by(id=data.get('user_id')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()
        return 'Thands For Your Activate'
    else:
        return 'wrong token'


@app.route('/test')
def test_index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserReister.query.filter_by(email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                return 'Welcome'
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong Email or Password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    return 'Here is Logout'


@app.route('/userinfo')
def userinfo():
    return 'Here is UserINFO'