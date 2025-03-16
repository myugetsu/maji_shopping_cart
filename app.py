from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models import db, User as Usdb, ShoppingCart, CartItem, Product, Order, OrderItem
from forms import AddToCartForm, CheckoutForm, LoginForm, RegistrationForm, SearchForm, ProductForm
from flask_login import LoginManager,  UserMixin, login_user, logout_user, login_required, current_user
import os
import logging
from logging import FileHandler, Formatter
from mpesa import initiate_stk_push

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

file_handler = FileHandler('error.log')
file_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

# class User(UserMixin):
#     def __init__(self, id, username, email, password, role):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.password = password
#         self.role = role

# # Replace this with your actual user storage mechanism (e.g., database)
# users = {
#     1: User(id=1, username='admin', email='admin@example.com', password='adminpass', role='admin'),
# }

@login_manager.user_loader
def load_user(user_id):
    return Usdb.query.filter_by(id=user_id).first()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@app.route('/')
def home():
    form = SearchForm()
    query = Product.query

    # Filter by category
    if request.args.get('category'):
        query = query.filter_by(category=request.args.get('category'))

    # Sort results
    sort_by = request.args.get('sort_by')
    if sort_by:
        if sort_by == 'price':
            query = query.order_by(Product.price)
        elif sort_by == '-price':
            query = query.order_by(Product.price.desc())
        elif sort_by == 'name':
            query = query.order_by(Product.name)
        elif sort_by == '-name':
            query = query.order_by(Product.name.desc())

    products = query.all()
    return render_template('home.html', form=form, products=products)

# cart routes
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    form = AddToCartForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        # Get the product and user's cart
        product = Product.query.get_or_404(product_id)
        cart = ShoppingCart.query.filter_by(user=current_user).first()
        if not cart:
            cart = ShoppingCart(user=current_user)
            db.session.add(cart)
            db.session.commit()
        # Check if item already exists in the cart
        existing_item = CartItem.query.filter_by(cart=cart, product_id=product.id).first()
        if existing_item:
            existing_item.quantity += quantity
            db.session.merge(existing_item)
        else:
            new_item = CartItem(
                cart=cart,
                product_id=product.id,
                quantity=quantity
            )
            db.session.add(new_item)
        db.session.commit()
        flash('Product added to cart successfully.')
        return redirect(url_for('home'))
    return render_template('add_to_cart.html', form=form)

@app.route('/cart')
@login_required
def view_cart():
    cart = ShoppingCart.query.filter_by(user=current_user).first()
    items = []
    if cart:
        items = CartItem.query.filter_by(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in items) if items else 0
    return render_template('cart.html', items=items, total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    cart = ShoppingCart.query.filter_by(user=current_user).first()
    items = CartItem.query.filter_by(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in items) if items else 0
    if form.validate_on_submit():
        phone_number = form.phone_number.data  # Add a phone number field to your form
        response = initiate_stk_push(phone_number, total_price)
        if response.get('ResponseCode') == '0':
            # Create an order and store the checkout_request_id
            order = Order(
                user_id=current_user.id,
                total_amount=total_price,
                checkout_request_id=response['CheckoutRequestID']
            )
            db.session.add(order)
            db.session.commit()
            flash('Payment initiated successfully. Please complete the payment on your phone.')
        else:
            flash('Failed to initiate payment. Please try again.')
        return redirect(url_for('home'))
    return render_template('checkout.html', form=form, items=items, total_price=total_price)


# register, login and logout routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email is already registered
        if Usdb.query.filter_by(email=form.email.data).first():
            flash('Email address is already in use.')
            return redirect(url_for('register'))

        # Create new user
        user = Usdb(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data  # Consider using bcrypt for secure password storage
        )
        db.session.add(user)
        db.session.commit()

        flash(f'Welcome, {form.username.data}! Your account has been created.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data

        # This is a simplified check; in real apps, use proper database queries
        form = LoginForm()
        user = Usdb.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

# admin routes
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usdb.query.filter_by(email=form.email.data).first()
        if user and user.role == "admin":
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials or not an admin account.", "error")
    return render_template("login.html", form=form)

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)

@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            stock=form.stock.data,
            price=form.price.data,
            category=form.category.data,
        )
        # Handle image upload
        if form.image.data:
            filename = form.image.data.filename
            product.image_url = os.path.join("static/images", filename)
            form.image.data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db.session.add(product)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/add_product.html", form=form)

@app.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # Update product details
        product.name = form.name.data
        product.description = form.description.data
        product.stock = form.stock.data
        product.price = form.price.data
        product.category = form.category.data

        # Handle image update
        if form.image.data:
            filename = form.image.data.filename
            product.image_url = os.path.join("static/images", filename)
            form.image.data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/edit_product.html", form=form, product=product)

@app.route("/admin/products/delete/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    # Process the callback data
    result_code = data['Body']['stkCallback']['ResultCode']
    result_desc = data['Body']['stkCallback']['ResultDesc']
    merchant_request_id = data['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
    amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    mpesa_receipt_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    phone_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']

    if result_code == 0:
        # Payment was successful
        # Update your database with the payment details
        order = Order.query.filter_by(checkout_request_id=checkout_request_id).first()
        if order:
            order.status = 'Paid'
            order.mpesa_receipt_number = mpesa_receipt_number
            db.session.commit()
        print(f"Payment successful: {amount} from {phone_number}")
    else:
        # Payment failed
        print(f"Payment failed: {result_desc}")

    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


if __name__ == '__main__':
    app.run(debug=True)
