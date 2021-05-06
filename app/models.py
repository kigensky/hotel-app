from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    '''Class to handle user'''
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), unique = True)
    email = db.Column(db.String(255), unique = True, index=True)
    role = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    # bio = db.Column(db.String())
    # profile_pic_path = db.Column(db.String())
    bookings = db.relationship('Booking',backref = 'user',lazy="dynamic")
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
 
    def isAdmin(self):
        '''return true if user is admin otherwise false'''

        user = User.query.get(int(self.id))
        if user.role == 'admin':
            return True
        else:
            return False


    def isCustomer(self):
        '''return true if user is customer otherwise false'''
        
        user = User.query.get(int(self.id))
        if user.role == 'customer':
            return True
        else:
            return False


    def __repr__(self):
        return f'User {self.username} {self.email}'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer,primary_key = True)
    classification = db.Column(db.String(255), unique = True)
    details = db.Column(db.Text)
    cost = db.Column(db.String(255))
    units = db.Column(db.Integer)
    image = db.Column(db.Text)
    bookings = db.relationship('Booking',backref = 'room',lazy="dynamic")

    def get_booked_units(self):
        units_booked = 0

        for booking in self.bookings:
            units_booked+=booking.units
        
        return units_booked

    def __repr__(self):
        return f'Room {self.classification} {self.cost} {self.units}'
        

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer,primary_key = True)
    units = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    from_date = db.Column(db.Text)
    to_date = db.Column(db.Text)
    rooms_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.Text)
    
    def __repr__(self):
        return f'Booking {self.user.username} {self.units}'
    
    
    
    