from flask import (render_template, redirect, url_for,flash, request)
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import SignUpForm, LoginForm
from .. import db
from ..email import mail_message


@auth.route("/signup", methods = ["GET", "POST"])
def register():
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        user = User(username = signup_form.username.data, 
                    email = signup_form.email.data,
                    password = signup_form.password.data,
                    role = "customer")
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to our Hotel Booking App","email/welcome",user.email,user=user)
       
        return redirect(url_for("auth.login"))
    title = "Sign Up to 60 Seconds"
    return render_template("auth/signup.html", 
                            signup_form = signup_form,
                            title = title)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get("next") or url_for("main.home"))

        flash("Invalid Username or Password")
    
    title = "Login to 60 Seconds"
    return render_template("auth/login.html",
                            login_form = login_form,
                            title = title)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))