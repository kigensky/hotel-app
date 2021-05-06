from flask import render_template, request, redirect, url_for, abort,flash
from . import main
from ..models import User, Room, Booking
from .. import photos
from flask_login import login_required, current_user
from .forms import RoomForm, BookingForm
# from datetime import datetime
# import bleach
from .. import db
from datetime import datetime
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
    if current_user.isCustomer() == False:         #check if user is or isnt customer
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))

    form = BookingForm()

    if form.validate_on_submit():
        
        room = Room.query.get(int(id))

        available_rooms = int(room.units) - int(room.get_booked_units()) #check available rooms

        if int(form.units.data) <= available_rooms:
            from_date_timestamp = datetime.strptime(str(form.from_date.data),'%Y-%m-%d' ).timestamp()
            to_date_timestamp = datetime.strptime(str(form.to_date.data),'%Y-%m-%d' ).timestamp()
            timestamp_diff = to_date_timestamp - from_date_timestamp

            days_stayed = int(timestamp_diff)//86400  #one day = 86400 sec
            
            total_cost = int(room.cost) * days_stayed * int(form.units.data)    # cost of room*day_stayed*units booked

            booking = Booking(units= form.units.data,
                              cost=total_cost,
                              from_date=datetime.fromtimestamp(int(from_date_timestamp)).strftime('%d-%m-%Y'),
                              to_date = datetime.fromtimestamp(int(to_date_timestamp)).strftime('%d-%m-%Y'),
                              rooms_id = room.id,
                              users_id = current_user.id,
                              created_at = datetime.today().strftime('%d-%m-%Y %H:%M'))


            db.session.add(booking)
            db.session.commit()

            flash('Booking was successful','success')

            return redirect(url_for('main.mybookings',id=current_user.id))
        else:
            flash('Either rooms are fully booked or you are booking more than available units','danger')

    return render_template('booking.html', booking_form = form)



@main.route('/mybookings/<id>')
@login_required
def mybookings(id):
    if current_user.isCustomer() == False:         #check if user is or isnt customer
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))


    bookings = Booking.query.filter_by(users_id = int(id)).all()


    return render_template('mybookings.html', bookings=bookings)



@main.route('/editbooking/<id>',methods = ["GET","POST"])
@login_required
def editbooking(id):
    if current_user.isCustomer() == False:         #check if user is or isnt customer
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))

    booking = Booking.query.get(int(id))

    form = BookingForm()    
    form.units.data = booking.units
    form.from_date.data = datetime.strptime(booking.from_date ,'%d-%m-%Y' )
    form.to_date.data = datetime.strptime(booking.to_date ,'%d-%m-%Y' )

    previous_units = booking.units

    if form.validate_on_submit():
        if form.units.data > (booking.room.units - booking.room.get_booked_units()+ previous_units ):
            flash('You are booking more than available units','danger')

            return redirect( url_for('main.home'))
        else:
            from_date_timestamp = datetime.strptime(str(form.from_date.data),'%Y-%m-%d  %H:%M:%S' ).timestamp()
            to_date_timestamp = datetime.strptime(str(form.to_date.data),'%Y-%m-%d  %H:%M:%S' ).timestamp()
            timestamp_diff = to_date_timestamp - from_date_timestamp

            days_stayed = int(timestamp_diff)//86400  #one day = 86400 sec
            
            total_cost = int(booking.room.cost) * days_stayed * int(form.units.data)    # cost of room*day_stayed*units booked

            booking = Booking.query.filter_by(id=int(id)).update({'units': form.units.data,
                                                        'cost':total_cost,
                                                        'from_date':datetime.fromtimestamp(int(from_date_timestamp)).strftime('%d-%m-%Y'),
                                                        'to_date': datetime.fromtimestamp(int(to_date_timestamp)).strftime('%d-%m-%Y'),
                                                        'created_at': datetime.today().strftime('%d-%m-%Y %H:%M')})
         
            db.session.commit()

            flash('Update was successful','success')

            return redirect(url_for('main.mybookings',id=current_user.id))


    return render_template('booking.html',booking_form = form)



@main.route('/deletebooking/<id>')
@login_required
def deletebooking(id):
    if current_user.isCustomer() == False:         #check if user is or isnt customer
        flash('Permission denied.','danger')
        return redirect( url_for('main.home'))

    booking = Booking.query.get(int(id))

    db.session.delete(booking)
    db.session.commit()

    flash('Booking deleted successfully','success')

    return redirect(url_for('main.mybookings',id=current_user.id))

