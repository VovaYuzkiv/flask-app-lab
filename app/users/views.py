from . import user_bp
from flask import request, redirect, url_for, render_template, flash, session, make_response
from .models import User
from .forms import LoginForm, RegisterForm
from app import db, bcrypt, loginManager
from flask_login import login_user, current_user, logout_user, login_required

@user_bp.route('/')
def main():
    return render_template("base.html")

@user_bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@user_bp.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newUser = User(username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('.login'))
    flash('Invalid:', 'danger')
    return render_template("register.html",form=form)

@user_bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".account"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash("Login successful","success")
            return redirect(url_for(".profile"))
        flash("Invalid: Не вірний логін або пароль.","danger")
    return render_template("login.html",form=form)

@user_bp.route("/account")
@login_required
def account():
    return render_template("account.html",user=current_user)

@user_bp.route("/profile", methods=["GET","POST"])
def profile():
    if "user" in session:
        user = session["user"]
        color_scheme = request.cookies.get("color_schem", "light")
        flash(f"Success: Вітання. {user}","success")
        if request.method == "POST" and "cookieInfo" in request.form:
            key = request.form["cookieKey"]
            value = request.form["cookieInfo"]
            life_time = request.form["cookieLifeTime"]
            max_age = int(life_time) if life_time else None
            response = make_response(redirect(url_for(".profile")))
            response.set_cookie(key,value,max_age=max_age)
            flash(f'Кукі "{key}" успішно додано.', 'success')
            return response
        
        if request.method == "POST" and "cookieKey" in request.form:
            key = request.form["cookieKey"]
            response = make_response(redirect(url_for(".profile")))
            response.set_cookie(key,'',max_age=0)
            flash(f'Кукі "{key}" успішно видалино.', 'success')
            return response
        
        if request.method == "POST" and "deletAllCookie" in request.form:
            response = make_response(redirect(url_for(".profile")))
            for keys in request.cookies.keys():
                response.set_cookie(keys,'',max_age=0)
            flash(f'Всі кукі успішно видалино.', 'success')
            return response
        return render_template("profile.html", user = user, color_scheme=color_scheme)
    return redirect(url_for(".login"))
    
@user_bp.route("logout")
def logout():
    logout_user()
    session.pop("user",None)
    return redirect(url_for(".login"))

@user_bp.route("/set_color/<scheme>")
def set_color_scheme(scheme):
    if scheme not in ["light", "dark"]:
        flash("Невірна кольорова схема", "error")
        return redirect(url_for("profile"))
    response = make_response(redirect(url_for(".profile")))
    response.set_cookie("color_schem", scheme)
    flash(f'Кольорова схема змінена на {scheme}.', "success")
    return response

@user_bp.route('/all_users')
def get_accounts():
    stmt= db.select(User).order_by(User.id)
    accounts = db.session.scalars(stmt).all()
    return render_template("user/all_register_account.html", accounts=accounts)

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))