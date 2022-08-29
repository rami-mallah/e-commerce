from conceptb import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.phone}', '{self.location}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    imageURL = db.Column(db.String, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    items = db.relationship('OrderItem', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    date_ordered = db.Column(db.DateTime)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def get_num_items(self):
        count = 0
        for item in self.items:
            count += item.quantity
        return count

    def get_full_price(self):
        price = 0
        for item in self.items:
            price += item.quantity * (Product.query.get(item.product_id).price)
        return price

    def __repr__(self):
        return f"Order(OrderID:'{self.id}', UserID:'{self.user_id}, '{self.status}', Date:'{self.date_ordered}')"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"OrderItem(OrderID:'{self.order_id}', ProductID:'{self.product_id}', Quantity:'{self.quantity}')"
