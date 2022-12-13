import flask_bcrypt

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """connects this database to provided flask app"""
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User:
    """creates table for users"""
    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True, #pk handles nullable = false
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(30),
        nullable = False
    )

    last_name = db.Column(
        db.String(30),
        nullable = False
    )
