from flask import render_template, url_for, flash, redirect, request, abort
from conceptb import app, db, bcrypt
from conceptb.forms import RegistrationForm, LoginForm, UpdateAccountForm
from conceptb.models import User, Order, OrderItem, Product
from flask_login import login_user, current_user, logout_user, login_required
from pytz import timezone
from datetime import datetime

def num_items():
    if current_user.is_authenticated:
        order = Order.query.filter_by(user=current_user, status='In progress').first()
        no_items = order.get_num_items()
    else:
        no_items = 0
    return no_items

# normal routes

@app.route('/')
@app.route('/home')
def home():
    no_items = num_items()
    products = Product.query.filter_by(is_deleted=False).all()
    return render_template('home.html', no_items=no_items, products=products)

@app.route('/about')
def about():
    no_items = num_items()
    return render_template('about.html', no_items=no_items)

@app.route('/contact')
def contact():
    no_items = num_items()
    if current_user.is_authenticated:
        email = current_user.email
    else:
        email = ''
    return render_template('contact.html', no_items=no_items, email=email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, phone=form.phone.data, location=form.location.data, password=hashed_password)
        order = Order(status='In progress', user=user)
        db.session.add_all([user, order])
        db.session.commit()
        login_user(user)
        flash('Account created! Start shopping now', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.is_admin:
                return redirect(url_for('orders', genre='ordered'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    no_items = num_items()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.location.data = current_user.location
        admin = current_user.is_admin
        orders = []
        for order in current_user.orders:
            if order.status in ['Ordered', 'Delivered']:
                orders.append(order)
        
        def date_ord(order):
            return order.date_ordered
        orders.sort(reverse=True, key=date_ord)

    return render_template('account.html', form=form, no_items=no_items, admin=admin, orders=orders)

@app.route('/cart')
@login_required
def cart():
    no_items = num_items()
    order = Order.query.filter_by(status='In progress', user=current_user).first()
    order_price = order.get_full_price()
    return render_template('cart.html', no_items=no_items, order_id=order.id, order_price=order_price, items=order.items)

@app.route('/add-product/<int:product_id>/<int:quantity>')
@login_required
def add_product(product_id, quantity):
    order = Order.query.filter_by(status='In progress', user=current_user).first()
    product = Product.query.get(product_id)
    already_present = False
    for item in order.items:
        if item.product_id == product_id:
            already_present = True
            item_to_update = item
    if already_present:
        item_to_update.quantity += quantity
    else:
        new_item = OrderItem(order=order, product=product, quantity=quantity)
        db.session.add(new_item)
    db.session.commit()
    flash('Item has been added to your cart', 'success')
    return redirect(url_for('home'))

@app.route('/delete-item/<int:item_id>')
@login_required
def delete_item(item_id):
    item_to_delete = OrderItem.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/update-item/<int:item_id>/<int:new_quantity>')
@login_required
def update_item(item_id, new_quantity):
    if new_quantity <= 0:
        return redirect(url_for('cart'))
    item_to_update = OrderItem.query.get(item_id)
    item_to_update.quantity = new_quantity
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/confirm-order/<int:order_id>')
@login_required
def confirm(order_id):
    order = Order.query.get(order_id)
    order.status = 'Ordered'
    lebanon = timezone('Asia/Beirut')
    order.date_ordered = datetime.now(lebanon)
    new_order = Order(status='In progress', user=current_user)
    db.session.add(new_order)
    db.session.commit()
    flash('Your order has been confirmed!', 'success')
    return redirect(url_for('home'))

@app.route('/thank')
def thank():
    flash('Your message has been sent. Thank you!', 'success')
    return redirect('home')

@app.route('/orders/<genre>')
@login_required
def orders(genre):
    if current_user.is_admin == False:
        abort(403)
    if genre in ['ordered', 'delivered']:
        orders = Order.query.filter_by(status=genre.title()).order_by(Order.date_ordered.desc()).all()
        if genre == 'ordered':
            orders.reverse()
    else:
        abort(404)
    return render_template('orders.html', genre=genre, orders=orders)

@app.route('/delivered/<int:order_id>')
@login_required
def delivered(order_id):
    if current_user.is_admin == False:
        abort(403)
    Order.query.get(order_id).status = 'Delivered'
    db.session.commit()
    return redirect(url_for('orders', genre='ordered'))

@app.route('/ordered/<int:order_id>')
@login_required
def ordered(order_id):
    if current_user.is_admin == False:
        abort(403)
    Order.query.get(order_id).status = 'Ordered'
    db.session.commit()
    return redirect(url_for('orders', genre='delivered'))

@app.route('/update-products')
@login_required
def update_products():
    if current_user.is_admin == False:
        abort(403)
    products = Product.query.filter_by(is_deleted=False).all()
    return render_template('update_products.html', products=products)

@app.route('/update-product/<int:product_id>/<new_name>/<int:new_price>')
@login_required
def update_product(product_id, new_name, new_price):
    if current_user.is_admin == False:
        abort(403)
    product = Product.query.get(product_id)
    product.name = new_name
    product.price = new_price
    db.session.commit()
    return redirect(url_for('update_products'))

@app.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.is_admin == False:
        abort(403)
    Product.query.get(product_id).is_deleted = True
    db.session.commit()
    return redirect(url_for('update_products'))

# errors

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500