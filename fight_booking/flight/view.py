from fight_booking.main import main
from fight_booking import app
from fight_booking import db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from fight_booking.main.form import FormUserInfo


