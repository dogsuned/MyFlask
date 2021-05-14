from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

basedir = os.path.abspath(os.path.dirname(__file__))

FILE_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ij234i23i4u3jff8sdwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
app.config['UPLOAD_FOLDER'] = FILE_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config.from_object(__name__)

db = SQLAlchemy(app)
db.create_all()
bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"

from app import views
