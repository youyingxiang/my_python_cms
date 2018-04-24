from flask import Blueprint,request
from utils import test
bp = Blueprint('common',__name__,url_prefix='/common')

@bp.route('/')
def index():
    key = int(request.args.get('key'))
    val = int(request.args.get('val'))
    res = test.jinz2(key, val)
    print(res)
    return res