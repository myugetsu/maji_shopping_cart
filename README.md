# Shopping Cart Application

This is a Flask-based shopping cart application that allows users to browse products, add them to their cart, and proceed to checkout using M-Pesa STK Push for payments.

## Features

- User registration and login
- Browse products by category
- Add products to the shopping cart
- View and manage the shopping cart
- Checkout with M-Pesa STK Push
- Admin dashboard to manage products

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/shopping_cart.git
    cd shopping_cart
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Configure the application:

    Create a `config.py` file with your configuration settings, including your M-Pesa credentials.

    ```python
    # filepath: /Users/myugetsu/python_workbench/shopping_cart/config.py
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shopping_cart.db'
    SECRET_KEY = 'your_secret_key'
    MPESA_CONSUMER_KEY = 'your_consumer_key'
    MPESA_CONSUMER_SECRET = 'your_consumer_secret'
    MPESA_SHORTCODE = 'your_shortcode'
    MPESA_PASSKEY = 'your_passkey'
    MPESA_CALLBACK_URL = 'https://yourdomain.com/mpesa/callback'
    UPLOAD_FOLDER = 'static/images'
    ```

6. Run the application:

    ```sh
    flask run
    ```

## Usage

- Visit `http://127.0.0.1:5000/` to access the home page.
- Register a new user or log in with an existing account.
- Browse products and add them to your cart.
- View your cart and proceed to checkout.
- Complete the payment using M-Pesa STK Push.

## Admin Dashboard

- Visit `http://127.0.0.1:5000/admin` to access the admin dashboard.
- Log in with an admin account to manage products.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
