from fight_booking.user import user
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request
from fight_booking.user.model import UserReister
from fight_booking.user.form import FormRegister, FormLogin, FormChangePWD, FormResetPasswordMail, FormResetPassword
from fight_booking.sendmail import send_mail
from flask_login import login_user, current_user, login_required, logout_user


@user.route('/')
@login_required
def index():
    return 'Hello ' + current_user.user_username + ' Welcome My HomePage'


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            user_username=form.username.data,
            user_email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        #  產生用戶認證令牌
        token = user.create_confirm_token()
        #  寄出帳號啟動信件
        send_mail(sender='Sender@domain.com',
                  recipients=[form.email.data],
                  subject='Activate your account',
                  template='mail/welcome',
                  mailtype='html',
                  user=user,
                  token=token)

        return 'Check Your Email and Activate Your Account'
    return render_template('register.html', form=form)


@user.route('/user_confirm/<token>')
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


@user.route('/test')
def test_index():
    return render_template('base.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserReister.query.filter_by(user_email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                #  加入參數『記得我』
                login_user(user, form.remember_me.data)
                #  使用者登入之後，將使用者導回來源url。
                #  利用request來取得參數next
                next = request.args.get('next')
                #  自定義一個驗證的function來確認使用者是否確實有該url的權限
                if not next_is_valid(next):
                    #  如果使用者沒有該url權限，那就reject掉。
                    return 'Bad Boy!!'
                return redirect(next or url_for('index'))
                # return 'Welcome' + current_user.username
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('user.login'))


@user.route('/userinfo')
@login_required
def userinfo():
    return 'Here is UserINFO'


#  加入function
def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True


@user.before_app_request
def before_request():
    """
    在使用者登入之後，需做一個帳號是否啟動的驗證，啟動之後才能向下展開相關的應用。
    條件一：需登入
    條件二：未啟動
    條件三：endpoint不等於static，這是避免靜態資源的取用異常，如icon、js、css等..
    :return:
    """
    if (current_user.is_authenticated and
            not current_user.user_confirm and
            request.endpoint not in ['re_userconfirm', 'logout', 'user_confirm', 'resetpassword'] and
            request.endpoint != 'static'):
        #  條件滿足就引導至未啟動說明
        flash('Hi, please activate your account first.')
        return render_template('unactivate.html')


@user.route('/reusreconfirm')
@login_required
def re_userconfirm():
    """
    當使用者點擊重新寄送的時候就引導到這個route
    因為已經使用current_user綁定user了，所以可以直接透過current_user使用user的相關方法
    重新寄送啟動信件必需要登入狀態
    :return:
    """
    #  產生用戶認證令牌
    token = current_user.create_confirm_token()
    #  寄出帳號啟動信件
    send_mail(sender='Your Mail@hotmail.com',
              recipients=['Your Mail@gmail.com'],
              subject='Activate your account',
              template='mail/welcome',
              mailtype='html',
              user=current_user,
              token=token)
    flash('Please Check Your Email..')
    return redirect(url_for('index'))


@user.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = FormChangePWD()
    if form.validate_on_submit():
        #  透過current_user來使用密碼認證，確認是否與現在的密碼相同
        if current_user.check_password(form.password_old.data):
            current_user.password = form.password_new.data
            db.session.add(current_user)
            db.session.commit()
            flash('You Have Already Change Your Password, Please Login Again.')
            return redirect(url_for('logout'))
        else:
            flash('Wrong Password...')
    return render_template('changepassword.html', form=form)


@user.route('/resetpassword', methods=['GET', 'POST'])
def reset_password():
    form = FormResetPasswordMail()
    if form.validate_on_submit():
        return 'RESET'
    return render_template('resetpasswordemail.html', form=form)


@user.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password_recive(token):
    """使用者透過申請連結進來之後，輸入新的密碼設置，接著要驗證token是否過期以及是否確實有其user存在
    這邊使用者並沒有登入，所以記得不要很順手的使用current_user了。
    """
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = FormResetPassword()

    if form.validate_on_submit():
        user = UserReister()
        data = user.validate_confirm_token(token)
        if data:
            #  如果未來有需求的話，還要確認使用者是否被停權了。
            #  如果是被停權的使用者，應該要先申請復權。
            #  下面注意，複製過來的話記得改一下id的取得是reset_id，不是user_id
            user = UserReister.query.filter_by(id=data.get('reset_id')).first()
            #  再驗證一次是否確實的取得使用者資料
            if user:
                user.password = form.password.data
                db.session.commit()
                flash('Sucess Reset Your Password, Please Login')
                return redirect(url_for('login'))
            else:
                flash('No such user, i am so sorry')
                return redirect(url_for('login'))
        else:
            flash('Worng token, maybe it is over 24 hour, please apply again')
            return redirect(url_for('login'))
    return render_template('author/resetpassword.html', form=form)
