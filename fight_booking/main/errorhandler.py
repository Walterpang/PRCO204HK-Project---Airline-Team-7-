from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    """
    自定義異常頁面，範例可於官網取得
    """
    return render_template('404.html'), 404