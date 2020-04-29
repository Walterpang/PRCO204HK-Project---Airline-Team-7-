from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

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
login.login_view = 'user.login'


db.drop_all()
#from fight_booking import model
#db.session.commit()

from fight_booking.user import user
app.register_blueprint(user, url_prefix='/user')
from fight_booking.main import main
app.register_blueprint(main, url_prefix='/main')
from fight_booking.flight import flight
app.register_blueprint(flight, url_prefix='/flight')

db.create_all()