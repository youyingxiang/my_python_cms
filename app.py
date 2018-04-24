from flask import Flask
from exts import db,mail
from apps.admin import bp as adminbp
from apps.common import bp as commonbp
from apps.home import bp as homebp
import config
from flask_wtf import CSRFProtect

app = Flask(__name__)

app.config.from_object(config)
app.register_blueprint(adminbp)
app.register_blueprint(commonbp)
app.register_blueprint(homebp)

db.init_app(app)
mail.init_app(app)
CSRFProtect(app)

if __name__ == '__main__':
    app.run()
