from flask import Blueprint

#  定義
main = Blueprint('main', __name__)
#  關聯
from . import view, errorhandler