from sqlalchemy import PrimaryKeyConstraint

from fight_booking import db
from datetime import  datetime



class Flight(db.Model):
    __tablename__ = 'tbl_flight'
    __table_args__ = (
        PrimaryKeyConstraint('flightID'),
    )
    flightID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    #flightID = db.Column(db.String(30), unique=True, nullable=False)
    airlineName = db.Column(db.String(30), nullable=False)
    flightNo = db.Column(db.String(30), nullable=False)
    airplacneModel = db.Column(db.String(30), nullable=False)
    from_place = db.Column(db.String(30), nullable=False)
    to_place = db.Column(db.String(30), nullable=False)
    depart_at_from = db.Column(db.DateTime, nullable=False)
    arrival_at_to = db.Column(db.DateTime, nullable=False)
    seat_no = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    off = db.Column(db.Integer, nullable=False)
    collected = db.Column(db.Integer, nullable=False)

    users = db.relationship("UserReister", secondary="booking" , back_populates="Flights" )

    def __str__(self):
        return str(self.flight) + str(self.from_place) + str(self.to_place) + str(self.depart_at_from) + str(
            self.arrival_at_to)

    @property
    def flightNo(self):
        raise AttributeError('Flight No is not a readable attribute')

    @flightNo.setter
    def flightNo(self):
        self.flightNo = airline.airline_short + self.flightID

class airline(db.model):
    __table_args__ = (
        PrimaryKeyConstraint('airlineiD'),
    )
    airlineID   = db.Column(db.Integer, autoincrement=True , primark_key=True)
    airlineName = db.Column(db.String(30), unique=True, nullable=False)
    airline_short = db.Column(db.String(5), unique=True, nullable=False)

class Airport(db.model):
    __table_args__ = (
        PrimaryKeyConstraint('airportiD'),
    )
    airportID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    airportNname = db.Column(db.String(30), unique=True, nullable=False)
    airport_localtion = db.Column(db.String(30), nullable=False)

class airplacnes(db.model):
    __table_args__ = (
        PrimaryKeyConstraint('airplacneID'),
    )
    airplacneID = db.Column(db.Integer, autoincrement=True, primark_key=True)
    airlineName = db.Column(db.String(30), unique=True)
    airplacneModel = db.Column(db.String(30), nullable=False)
    airplacneTotalSeats = db.Column(db.Integer, nullable=False)

class booking(db.model):
    __tablename__ = 'booking'
    Booking_ID = db.Column(db.Integer, autoincrement=True , primark_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.user_id'), primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flight.flightID'), primary_key=True)


db.create_all()