from flask import Blueprint
bp = Blueprint('home',__name__)

@bp.route('/')
def index():
    return '这是是前台首页'