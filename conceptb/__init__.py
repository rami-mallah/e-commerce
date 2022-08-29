from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from conceptb.models import User, Order

app = Flask(__name__)
app.config["SECRET_KEY"] = '7692j479263qj972z3694329ja9jzoqopiwealp82'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# if len(User.query.filter_by(is_admin=True).all()) == 0:
#     admin = User(email='admin@admin.com', phone='03123456', location='ConceptB', password='', is_admin=True)
#     order = Order(status='In progress', user=admin)
#     db.session.add_all([admin, order])
#     db.session.commit()

from conceptb import routes