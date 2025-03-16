from app import app
from models import db, User

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password="adminpass",  # You should hash this in production
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
