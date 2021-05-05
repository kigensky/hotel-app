from flask import render_template, request, redirect, url_for, abort
from . import main
# from ..models import User, Comment, Post, Subscribers
# from flask_login import login_required, current_user
# from .forms import (UpdateProfile, PostForm, CommentForm, UpdatePostForm)
# from datetime import datetime
# import bleach
# from .. import db
# from ..requests import get_quote
# from ..email import welcome_message, notification_message

@main.route("/")
def home():
    return render_template("index.html")