from flask import render_template, request, redirect, url_for, abort,flash
from . import main
from ..models import User, Room
from .. import photos
from flask_login import login_required, current_user
from .forms import RoomForm
# from datetime import datetime
# import bleach
from .. import db
# from ..requests import get_quote
# from ..email import welcome_message, notification_message

@main.route("/")
def home():
    rooms = Room.query.all()

    return render_template("index.html", rooms=rooms)


@main.route('/addroom', methods = ["GET","POST"])
@login_required
def addroom():
    if current_user.isAdmin() == False:         #check if user is admin
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))
        
    form = RoomForm()
    form.classification.choices=[('','-select-'),('executive','Executive'),('suite','Suite')]

    if form.validate_on_submit():
        room = Room(classification=form.classification.data,
                    details=form.details.data,
                    cost=form.cost.data,
                    units=form.units.data)
                    
        filename = photos.save(form.image.data)
        path = f'photos/{filename}'
        room.image = path

        db.session.add(room)
        db.session.commit()
        
        flash('Room added successfully','success')
        return redirect( url_for('main.home'))

    return render_template('addroom.html',  room_form=form)