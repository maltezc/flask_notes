from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """connects this database to provided flask app"""
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
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

    @classmethod
    def register(cls,username, password, email, first_name, last_name):
        """Register user /hashed password & return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        #return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed,
        email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """authetnicates that the name and password is a correct match"""

        user = cls.query.get_or_404(username)
        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False


class Note(db.Model):
    """creates table for notes"""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    owner = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )
    user = db.relationship("User", backref="notes")