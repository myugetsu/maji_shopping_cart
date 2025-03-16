from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)  # Consider using bcrypt for better security
    role = db.Column(db.Enum('admin', 'user'), default='user')
    cart = db.relationship('ShoppingCart', backref='user', uselist=False)

    def is_active(self):
        return True

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)
    total_price = db.Column(db.Float)  # Added field to store the total price of cart
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    size = db.Column(db.String(20))  # Added field for size
    color = db.Column(db.String(20))  # Added field for color

    product = db.relationship('Product', backref='cart_items')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=1)
    category = db.Column(db.String(50))  # Added field for product category
    image_url = db.Column(db.String(200))  # Added field for product image URL
    brand = db.Column(db.String(80))  # Added field for product brand
    size = db.Column(db.String(20))  # Added field for product size
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.name}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    mpesa_receipt_number = db.Column(db.String(100), nullable=True)
    checkout_request_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
