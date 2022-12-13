from flask import Flask, render_template, redirect, jsonify, request

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
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
@app.route("/register", method=["GET", "POST"])
def register_user():
"""display and registers a user"""










Make sure you are using WTForms and that your password input hides the characters that the user is typing!

POST /register
Process the registration form by adding a new user. Then redirect to /secret
GET /login
Show a form that when submitted will login a user. This form should accept a username and a password.

Make sure you are using WTForms and that your password input hides the characters that the user is typing!

POST /login
Process the login form, ensuring the user is authenticated and going to /secret if so.
GET /secret
Return the text “You made it!” (don’t worry, we’ll get rid of this soon)