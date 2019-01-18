from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import config

app = Flask(__name__)


app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + config.user + ':@' + config.host \
                                        + ":" + str(config.port) + "/" + config.db

db = SQLAlchemy(app)
Bootstrap(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return database.UserList.query.get(int(user_id))


from app import md2html
from app import database
from app import auth
