from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import database
from authlib.integrations.flask_client import OAuth
import datetime
import os

uri = os.environ.get("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

year = datetime.datetime.now().year
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bug_tracker.db' or uri
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    acess_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/home")
@login_required
def home():
    return render_template("home.html", year=year)


@app.route("/admin")
@login_required
def admin():
    if current_user.role == "Admin":
        users = database.get_all_users()
        return render_template("admin.html", users=users, year=year)


@app.route("/all_projects", methods=["POST", "GET"])
@login_required
def all_projects():
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        projects = database.get_all_projects()
        return render_template("all_projects.html", projects=projects, year=year)


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if not database.check_email_exist(request.form["email"]):
            flash("The email you have entered is incorrect.")
            return redirect(url_for("login"))
        user = User.query.filter_by(email=request.form["email"]).first()
        if database.check_password(request.form):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("The password you have entered is incorrect.")
            return redirect(url_for("login"))
    return render_template("login.html", year=year)


@app.route("/log_in_demo_user/<id>")
def log_in_demo_user(id):
    if int(id) == 2:
        user = User.query.filter_by(email="test@test.com").first()
        if database.login_demo_admin():
            login_user(user)
            return redirect(url_for("home"))
    elif int(id) == 3:
        user = User.query.filter_by(email="admin@email.com").first()
        if database.login_demo_project_manager():
            login_user(user)
            return redirect(url_for("home"))
    else:
        user = User.query.filter_by(email="admin@email.comm").first()
        if database.login_demo_developer():
            login_user(user)
            return redirect(url_for("home"))


@app.route('/google_login')
def google_login():
    google = oauth.create_client("google")
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    res = google.get('userinfo', token=token)
    res.raise_for_status()
    user_info = res.json()
    is_registered = database.check_email_exist(user_info["email"])
    if not is_registered:
        database.register_google_account(user_info)
        user = User.query.filter_by(email=user_info["email"]).first()
        login_user(user)
    else:
        user = User.query.filter_by(email=user_info["email"]).first()
        login_user(user)
    return redirect('home')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if database.check_email_exist(request.form["email"]):
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:
            user = User.query.filter_by(email=request.form["email"]).first()
            database.register_account(request.form, user)
            return redirect(url_for("home"))
    return render_template("register.html", year=year)


@app.route("/project/<id>")
@login_required
def project(id):
    database.delete_duplicate_devs_from_projects()
    devs = database.get_project_devs(id)
    project = database.get_project_by_id(id)
    tickets = database.get_tickets_by_project_id(id)
    all_users = database.get_all_users()
    return render_template("project.html", project=project, all_users=all_users, devs=devs, tickets=tickets, year=year)


@app.route("/add_project", methods=["POST"])
@login_required
def add_project():
    print(current_user.role)
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if request.method == "POST":
            database.add_project(request.form, current_user)
            return redirect(url_for("all_projects"))


@app.route("/edit_project", methods=["POST"])
@login_required
def edit_project():
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if request.method == "POST":
            if int(request.form["id"]) == 1:
                flash("Sorry but you can not edit anything from this project.")
                return redirect(url_for("project", id=request.form["id"]))
            else:
                database.update_project(request.form)
                return redirect(url_for("project", id=request.form["id"]))


@app.route("/delete_project/<id>")
@login_required
def delete_project(id):
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if int(id) == 1:
            flash("Sorry but you can not delete this project.")
            return redirect(url_for("project", id=id))
        else:
            database.delete_project_by_id(id)
            return redirect(url_for("all_projects"))


@app.route("/ticket/<id>")
@login_required
def ticket(id):
    current_ticket = database.get_ticket_by_id(id)
    devs = database.get_project_devs(current_ticket[10])
    comments = database.get_comments_by_ticket_id(id)
    return render_template("ticket.html", ticket=current_ticket, comments=comments, devs=devs, year=year)


@app.route("/add_ticket", methods=["POST"])
@login_required
def add_ticket():
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if request.method == "POST":
            if int(request.form["project_id"]) == 1:
                flash("Sorry but you can not add new tickets to this project.")
                return redirect(url_for("project", id=request.form["project_id"]))
            else:
                database.add_ticket(request.form, current_user)
                return redirect(url_for("project", id=request.form["project_id"]))


@app.route("/edit_ticket", methods=["POST"])
@login_required
def edit_ticket():
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if request.method == "POST":
            if int(request.form["project_id"]) == 1:
                flash("Sorry but you can not edit anything from this project.")
                return redirect(url_for("project", id=request.form["project_id"]))
            else:
                database.update_ticket(request.form)
                return redirect(url_for("ticket", id=request.form["ticket_id"]))


@app.route("/delete_ticket/<project_id>/<id>")
@login_required
def delete_ticket(project_id, id):
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if int(project_id) == 1:
            flash("Sorry but you can not delete this Ticket.")
            return redirect(url_for("project", id=project_id))
        else:
            database.delete_ticket_by_id(id)
            return redirect(url_for("project", id=project_id))


@app.route("/add_project_dev/<project_id>", methods=["POST"])
@login_required
def add_project_dev(project_id):
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if request.method == "POST":
            full_name = request.form["dev"].split()
            first_name = full_name[0]
            last_name = full_name[1]
            user_id = database.get_account_by_fullname(
                first_name, last_name)[0]
            database.add_dev_to_project(user_id, project_id)
            return redirect(url_for("project", id=project_id, year=year))


@app.route("/delete_dev_project/<project_id>/<id>")
@login_required
def delete_dev_project(project_id, id):
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if int(project_id) == 1:
            flash("Sorry but you can not delete devs from this project.")
            return redirect(url_for("project", id=project_id))
        else:
            database.delete_dev_from_project_by_user_id(id)
            return redirect(url_for("project", id=project_id))


@app.route("/add_comment", methods=["POST"])
@login_required
def add_comment():
    if request.method == "POST":
        database.add_comment(request.form, current_user)
        return redirect(url_for("ticket", id=request.form["ticket_id"]))


@app.route("/delete_comment/<ticket_id>/<comment_id>/<project_id>")
@login_required
def delete_comment(ticket_id, comment_id, project_id):
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if int(project_id) == 1:
            flash("Sorry but you can not delete any comments from this project.")
            return redirect(url_for("project", id=project_id))
        else:
            database.delete_comment_from_ticket(ticket_id, comment_id)
            return redirect(url_for("ticket", id=ticket_id))


@app.route("/user_projects")
@login_required
def user_projects():
    projects = database.get_user_projects_by_user_id(current_user.id)
    return render_template("my_projects.html", projects=projects, year=year)


@app.route('/update_user', methods=["POST"])
@login_required
def update_user():
    if current_user.role == "Admin" or current_user.role == "Project Manager":
        if current_user.id == 2:
            flash("Sorry but you can not edit users.")
        else:
            database.update_user(request.form)
        return redirect(url_for("admin"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
