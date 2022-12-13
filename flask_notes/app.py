from flask import Flask, render_template, redirect, jsonify, request, session, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


#####################################RENDER ROUTES#######################
""" GET /
Redirect to /register. """
@app.get('/')
def direct_to_register():
    """redirects to register"""

    return redirect("/register")


# GET /register
# Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name.
@app.route("/register", methods=["GET", "POST"])
def register_user():
    """display and registers a user"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # on successful login, redirect to secret page
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.get("/secret")
def render_secret_page():
    """returns the secrets"""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        return render_template("secrets.html")




