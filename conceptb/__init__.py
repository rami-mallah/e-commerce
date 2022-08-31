from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = '7692j479263qj972z3694329ja9jzoqopiwealp82'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://ramimallah:password@localhost/flask_db'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://xkfsmnufmedxpz:20da52d446f0586861b77b33ad96555412aac11796550dab7a50d570c8378e72@ec2-54-172-175-251.compute-1.amazonaws.com:5432/d1501ikq99489h'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from conceptb.models import User, Order

if len(User.query.filter_by(is_admin=True).all()) == 0:
    admin = User(email='admin@admin.com', phone='03123456', location='ConceptB', password='$2b$12$koQjI10KBhcXUhEND/Xoe.Jgr4G90IDCF17csMzAKo.4YShisRCSm', is_admin=True)
    order = Order(status='In progress', user=admin)
    db.session.add_all([admin, order])
    db.session.commit()

from conceptb import routes