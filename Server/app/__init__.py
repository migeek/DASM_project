from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
sio = SocketIO(app)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
files = {}

from app import routes, models, connections


# @sio.on('setup')
# def test_event(message):
#     print('received message: ' + str(message))
#     emit('return message', {'data': str(message['data'])})
