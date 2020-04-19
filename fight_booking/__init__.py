from flask import Flask, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager,UserMixin, login_user, current_user, login_required, logout_user

from sqlalchemy import create_engine
from config import Config
import os

#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

#db.drop_all()

#from fight_booking import model
#db.session.commit()

from fight_booking import view
