from flask import render_template, request, redirect, url_for, abort,flash
from . import main
from ..models import User, Room
from .. import photos
from flask_login import login_required, current_user
from .forms import RoomForm, BookingForm
# from datetime import datetime
# import bleach
from .. import db
# from ..requests import get_quote
# from ..email import welcome_message, notification_message

choices = [('','-select-'),('executive','Executive'),('suite','Suite'),('single room','Single Room'),('double room','Double Room')]

@main.route("/")
def home():
    rooms = Room.query.all()

    user= None
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.id))

    return render_template("index.html", rooms=rooms, user=user)


@main.route('/addroom', methods = ["GET","POST"])
@login_required
def addroom():
    if current_user.isAdmin() == False:         #check if user is admin
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))
        
    form = RoomForm()
    form.classification.choices=choices

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



@main.route('/editroom/<id>', methods = ["GET","POST"])
@login_required
def editroom(id):
    if current_user.isAdmin() == False:         #check if user is admin
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))

    room = Room.query.get(int(id))

    form = RoomForm()
    form.classification.choices=choices
    # form.classification.render_kw = {'disabled': 'disabled'}
    form.classification(disabled='disabled')

    

    if form.validate_on_submit():
        room = Room.query.get(int(id))
        room.classification=form.classification.data
        room.details=form.details.data
        room.cost=form.cost.data
        room.units=form.units.data
                    
        filename = photos.save(form.image.data)
        path = f'photos/{filename}'
        room.image = path

        db.session.add(room)
        db.session.commit()
        
        flash('Edit was successful','success')
        return redirect( url_for('main.home'))

    form.classification.data = room.classification
    form.details.data = room.details
    form.cost.data = room.cost
    form.units.data = room.units

    return render_template('addroom.html',  room_form=form)



@main.route('/deleteroom/<id>')
@login_required
def deleteroom(id):
    if current_user.isAdmin() == False:         #check if user is admin
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))

    room = Room.query.get(int(id))

    db.session.delete(room)
    db.session.commit()

    flash('Room deleted successfully','success')

    return redirect( url_for('main.home'))
    


@main.route('/book/<id>', methods = ["GET","POST"])
@login_required
def book(id):
    form = BookingForm()
    return render_template('booking.html', booking_form = form)


