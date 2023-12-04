from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dadosgerais.db"
app.config["SECRET_KEY"] = "A2b9C1d8E3fG4h6I7j0Kl2Mn4OpQr5TuVxY"
app.config["UPLOAD_FOLDER"] = "static/arquivos"


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from SolucaoWeb import routes