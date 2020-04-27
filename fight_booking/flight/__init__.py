from flask import Blueprint
#  定義
flight = Blueprint('flight', __name__)
#  關聯
from . import view
from . import model