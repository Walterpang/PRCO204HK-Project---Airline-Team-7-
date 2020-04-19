from sqlalchemy import PrimaryKeyConstraint
from fight_booking import db,bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app
from flask_login import UserMixin
from fight_booking import login

class UserReister(UserMixin, db.Model):
    """記錄使用者資料的資料表"""
    __tablename__ = 'tbl_user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id'),
    )
    user_id = db.Column(db.Integer, primark_key=True)
    user_username = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(80), unique=True, nullable=False)
    #user_password = db.Column(db.String(50), nullable=False)
    user_confirm = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(50), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        """
        密碼驗證，驗證使用者輸入的密碼跟資料庫內的加密密碼是否相符
        :param password: 使用者輸入的密碼
        :return: True/False
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def create_confirm_token(self, expires_in=3600):
        """
        利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
        :param expiration: 有效時間，單位為秒
        :return: 回傳令牌，參數為該註冊用戶的id
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id})

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data

    def get_id(self):
        return (self.user_id)

    def create_reset_token(self, expires_in=3600):
        """
        提供申請遺失密碼認證使用的token
        :param expires_in: 有效時間(秒)
        :return:token
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'reset_id': self.id})

    def __repr__(self):
        return 'user_username:%s, user_email:%s' % (self.user_username, self.user_email)

@login.user_loader
def load_user(user_id):
    return UserReister.query.get(int(user_id))

class Travelling(db.Model):
    __tablename__ = 'tbl_Travelling'
    __table_args__ = (
        PrimaryKeyConstraint('flight'),
    )
    flight = db.Column(db.String(30),unique=True, nullable=False)
    from_place = db.Column(db.String(30), nullable=False)
    to_place = db.Column(db.String(30), nullable=False)
    depart_at_from = db.Column(db.DateTime, nullable=False)
    arrival_at_to = db.Column(db.DateTime, nullable=False)
    seat_no = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    off = db.Column(db.Integer, nullable=False)
    collected = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return str(self.flight)+str(self.from_place)+str(self.to_place) + str(self.depart_at_from) + str(self.arrival_at_to)

#class Booking(db.Model):
    #__tablename__ = 'tbl_Booking'
    #booked = db.Column(db.boolean ,db.ForeignKey(UserReister))
    #no_of_seats = db.Column(db.Integer, nullable=False)
    #Travelling = db.ForeignKey(Travelling)
    #cost = db.IntegerField(default=0)
    #def __str__(self):
        #return str(self.Travelling)+str(self.booked)+str(self.no_of_seats)

db.create_all()