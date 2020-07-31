from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()


@app.route("/")
def get_root_route():
    user_id = session.get("user_id")
    if user_id :
        user = User.query.get(user_id)
        return redirect(f"/users/{user.username}")

    return redirect('/register')

@app.route("/register", methods=["GET", "POST"])
def show_register_form():
    form = RegisterForm()

    if form.validate_on_submit() : # Checks if post request AND if it's coming from our form.

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # show page that only authenticated users can see
        return redirect(f'/users/{user.username}')

    else :
        return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        typed_password = form.password.data

        authenticated_user = User.authenticate(username, typed_password)

        if authenticated_user :
            session["user_id"] = authenticated_user.id # logs in user by adding the user to session cookie
            return redirect(f'/users/{authenticated_user.username}')
        else :
            return redirect("/")

    else :
        return render_template("login.html", form=form)

@app.route("/users/<username>")
def show_secret_page(username):
    """ Shows a page only authenticated users can see """
    if "user_id" not in session:
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).first()
        return render_template("secret.html", user=user)

@app.route("/logout")
def logout_user():
    """ Logs user out when they hit this route """
    
    session.pop("user_id")

    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if user.id == session.get("user_id") :

        db.session.delete(user)
        db.session.commit()

        session.pop("user_id")

        return redirect("/")
    
    else :
        return reditect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ Shows form to add feedback. If post, handles form """

    if "user_id" not in session:
        return redirect("/")
    
    form = FeedbackForm()
    user = User.query.get(session["user_id"])

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        

        newFeedback = Feedback(title=title, content=content, user=user)

        db.session.add(newFeedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")
    
    else :
        return render_template("addfeedback.html", form = form, user=user)

@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def edit_feedback(id):
    """ Shows form to edit feedback. If post, handles form """

    feedback = Feedback.query.get(id)

    if feedback.user.id != session.get("user_id") :
        return redirect("/")
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else : 
        return render_template("addfeedback.html", form=form, user=feedback.user)

@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):

    feedback = Feedback.query.get(id)

    if feedback.user.id != session.get("user_id") :
        return redirect("/")
    

    db.session.delete(feedback)
    db.session.commit()

    return redirect("/")

    
