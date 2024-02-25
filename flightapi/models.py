from sqlalchemy import Column, Integer, String, JSON, Computed, Numeric, VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class Airports(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    # IATA Code
    code = Column(VARCHAR(3), unique=True, index=True)
    name = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    country = Column(VARCHAR(255))
    # latitude = Column(Numeric, nullable=False, index=True)
    # longitude = Column(Numeric, nullable=False, index=True)
    # geom = Column(Geometry(geometry_type='POINT', srid=4326),
    #               server_onupdate=Computed('ST_GeomFromEWKT(ST_MakePoint(longitude, latitude))'))

    # departing_flights = relationship("Flights", backref="departing_airport",
    #                                  foreign_keys=[Column('departing_airport_id')])
    # arriving_flights = relationship("Flights", backref="arrival_airport",
    #                                 foreign_keys=[Column('arrival_airport_id')])


class Airlines(Base):
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Flights(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_status = Column(String, index=True)
    flight_number = Column(String, index=True)
    available_seats = Column(String, index=True)
    departure_airport_id = Column(Integer, ForeignKey('airports.id'), index=True)
    arrival_airport_id = Column(Integer, ForeignKey('airports.id'), index=True)
    departure_date = Column(String, index=True)
    arrival_date = Column(String, index=True)
    duration = Column(Integer, index=True)
    fare = Column(Numeric, index=True)

    departure_airport = relationship("Airports", backref="departing_flights", foreign_keys=[departure_airport_id])
    arrival_airport = relationship("Airports", backref="arriving_flights", foreign_keys=[arrival_airport_id])

    # __table_args__ = (
    #     UniqueConstraint('departure_airport_id', 'arrival_airport_id', name='unique_flight_airports'),
    # )


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(255), unique=True, index=True)
    email = Column(VARCHAR(255), unique=True, index=True)
    password = Column(VARCHAR(255))


class Passengers(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey('flights.id'), index=True)
    first_name = Column(VARCHAR(255), index=True)
    last_name = Column(VARCHAR(255), index=True)
    date_of_birth = Column(String, index=True)
    passport_number = Column(VARCHAR(255), index=True)

    departure_airport = relationship("Flights", backref="passenger_flights", foreign_keys=[flight_id])

