from fight_booking.main import main
from fight_booking import app
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from fight_booking.main.form import FormUserInfo
from fight_booking.user.model import UserReister


@main.route('/')
@main.route('/index')
@app.route('/')
@login_required
def index():
    """
    首頁
    :return:
    """
    return render_template('index.html')

@main.route('/edituserinfo', methods=['GET', 'POST'])
@login_required
def edituserinfo():
    form = FormUserInfo()
    if form.validate_on_submit():
        current_user.user_fullname = form.user_fullname.data
        current_user.address = form.address.data
        current_user.gender = form.gender.data
        current_user.passportID = form.passportID.data
        current_user.contactNo = form.contactNo.data
        db.session.add(current_user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('main.userinfo', username=current_user.user_username))
    form.user_fullname.data = current_user.user_fullname
    form.address.data = current_user.address
    form.contactNo.data = current_user.contactNo
    form.gender.data = current_user.gender
    return render_template('main/editUserInfo.html', form=form)

@main.route('/userinfo/<username>')
@login_required
def userinfo(username):
    user = UserReister.query.filter_by(user_username= username).first()
    if user is None:
        abort(404)
    return render_template('main/UserInfo.html', user=user)
