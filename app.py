import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-before-deployment")
database_url = os.environ.get("DATABASE_URL", "sqlite:///service_requests.db")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    requests = db.relationship("ServiceRequest", backref="citizen", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class RegisterForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email address", validators=[DataRequired(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Use at least 8 characters.")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match.")])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError("An account with this email already exists.")


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RequestForm(FlaskForm):
    title = StringField("Short title", validators=[DataRequired(), Length(min=4, max=120)])
    category = SelectField("Category", choices=[
        ("Roads", "Roads and streetlights"),
        ("Water", "Water supply"),
        ("Waste", "Garbage collection"),
        ("Public safety", "Public safety"),
        ("Other", "Other")
    ], validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), Length(min=3, max=180)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10, max=2000)])


class StatusForm(FlaskForm):
    status = SelectField("Status", choices=[
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved")
    ], validators=[DataRequired()])


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}


@app.route("/")
def index():
    recent_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).limit(3).all()
    return render_template("index.html", recent_requests=recent_requests)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(full_name=form.full_name.data.strip(),
                    email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Your account is ready. You can now submit a service request.", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome back.", "success")
            return redirect(url_for("admin_dashboard" if user.is_admin else "dashboard"))
        flash("The email or password is incorrect.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for("admin_dashboard"))
    requests_list = ServiceRequest.query.filter_by(user_id=current_user.id).order_by(
        ServiceRequest.created_at.desc()).all()
    return render_template("dashboard.html", requests_list=requests_list)


@app.route("/requests/new", methods=["GET", "POST"])
@login_required
def new_request():
    if current_user.is_admin:
        return redirect(url_for("admin_dashboard"))
    form = RequestForm()
    if form.validate_on_submit():
        item = ServiceRequest(
            title=form.title.data.strip(),
            category=form.category.data,
            location=form.location.data.strip(),
            description=form.description.data.strip(),
            user_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash(f"Request #{item.id} has been submitted.", "success")
        return redirect(url_for("dashboard"))
    return render_template("new_request.html", form=form)


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    all_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    total = len(all_requests)
    pending = sum(item.status == "Pending" for item in all_requests)
    in_progress = sum(item.status == "In Progress" for item in all_requests)
    resolved = sum(item.status == "Resolved" for item in all_requests)
    return render_template("admin.html", requests_list=all_requests, total=total,
                           pending=pending, in_progress=in_progress, resolved=resolved)


@app.route("/admin/requests/<int:request_id>", methods=["POST"])
@login_required
@admin_required
def update_request(request_id):
    item = db.get_or_404(ServiceRequest, request_id)
    form = StatusForm()
    if form.validate_on_submit():
        item.status = form.status.data
        db.session.commit()
        flash(f"Request #{item.id} was updated.", "success")
    else:
        flash("Please select a valid status.", "danger")
    return redirect(url_for("admin_dashboard"))


@app.errorhandler(403)
def forbidden(_error):
    return render_template("error.html", code=403,
                           message="You do not have permission to view this page."), 403


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404,
                           message="The page or request could not be found."), 404


def initialise_database():
    with app.app_context():
        db.create_all()
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com").strip().lower()
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if admin_password and not User.query.filter_by(email=admin_email).first():
            admin = User(full_name="System Administrator", email=admin_email, is_admin=True)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()


initialise_database()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
