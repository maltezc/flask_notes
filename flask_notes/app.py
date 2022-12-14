from flask import Flask, render_template, redirect, jsonify, request, session, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note

from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm

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

@app.get('/')
def direct_to_register():
    """redirects to register"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """display and registers a user"""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_name"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{name}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)
        if user:
            session["user_name"] = user.username  # keep logged in
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.get("/users/<username>")
def render_user_page(username):
    """returns the user"""

    if "user_name" not in session or session["user_name"] != username:
        # if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect("/")


    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    return render_template("user.html", user=user, form=form)

@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_name" if present, but no errors if it wasn't
        session.pop("user_name", None)
    return redirect("/")


@app.post("/users/<username>/delete")
def delete(username):
    """deletes username, all associated notes, and user's session"""

    form = CSRFProtectForm()
    user = User.query.get(username)

    if form.validate_on_submit():
        # db.session.delete(user.notes)
        # db.session.commit()

        db.session.delete(user)
        db.session.commit()

        session.clear()

        return redirect("/")



# GET /users/<username>/notes/add
# Display a form to add notes.

# POST /users/<username>/notes/add
# Add a new note and redirect to /users/<username>
@app.route('users/<username>/notes/add', methods=["GET","POST"])
def add_note(username):
    """Add a note"""

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title,content)

        db.session.add(note)
        db.session.commit()

        render_template("add_note.html", form=form)
    else:
        redirect(f'users/{username}')




# GET /notes/<note-id>/update
# Display a form to edit a note.


# POST /notes/<note-id>/update
# Update a note and redirect to /users/<username>.


# POST /notes/<note-id>/delete
# Delete a note and redirect to /users/<username>.



# As with the logout and delete routes, make sure you have CSRF protection for this.


