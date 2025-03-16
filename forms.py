from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, Length
from models import Product

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

class CheckoutForm(FlaskForm):
    name = StringField('Full Name')
    address = StringField('Shipping Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('Zip Code')
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

# Temporary hardcoded categories for development
categories = ['All', 'Electronics', 'Clothing', 'Food']

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(max=80)])
    description = TextAreaField("Description")
    stock = IntegerField("Stock", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("electronics", "Electronics"),
            ("clothing", "Clothing"),
            ("home", "Home & Living"),
            ("other", "Other"),
        ],
    )
    image = FileField("Product Image")

class SearchForm(FlaskForm):
    search = StringField('Search')
    category = SelectField(
        'Category',
        choices=[(None, 'All')] + [(c.lower(), c) for c in categories]
    )
    sort_by = SelectField(
        'Sort By',
        choices=[
            (None, 'Relevance'),
            ('price', 'Price Low to High'),
            ('-price', 'Price High to Low'),
            ('name', 'Name A-Z'),
            ('-name', 'Name Z-A')
        ]
    )
