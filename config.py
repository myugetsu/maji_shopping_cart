import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///shoppingcart.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'your-secret-key-here'
UPLOAD_FOLDER = os.path.join(os.path.abspath("."), "static/images")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maximum file size: 16MB
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

MPESA_CONSUMER_KEY = 'your_consumer_key'
MPESA_CONSUMER_SECRET = 'your_consumer_secret'
MPESA_SHORTCODE = 'your_shortcode'
MPESA_PASSKEY = 'your_passkey'
MPESA_CALLBACK_URL = 'https://yourdomain.com/mpesa/callback'

# config.py

# import os

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key"
#     SQLALCHEMY_DATABASE_URI = (
#         os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(os.path.abspath('.'), 'instance/shoppingcart.db')}"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = os.path.join(os.path.abspath("."), "static/images")
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maximum file size: 16MB
#     ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
