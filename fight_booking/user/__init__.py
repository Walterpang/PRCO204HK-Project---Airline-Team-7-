from flask import Blueprint

#  定義
user = Blueprint('user', __name__)
#  關聯
from . import view