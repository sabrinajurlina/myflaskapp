from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



#initializing
app = Flask(__name__)
app.config.from_object(Config)

#register plug-ins
login = LoginManager(app)

#configure some settings
login.login_view ='login'
login.login_message = 'You must log in to create your team'
login.login_message_category = 'warning'

# init my DB manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes