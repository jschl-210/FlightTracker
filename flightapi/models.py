from sqlalchemy import Column, Integer, String, JSON, Computed, Numeric, VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class Airports(Base):
    """
    The Airports class represents airports in the system.

    Attributes:
        id (int): The primary key of the airport.
        code (str): The IATA code of the airport.
        name (str): The name of the airport.
        city (str): The city the airport is located in.
        country (str): The country the airport is located in.
        latitude (float): The latitude of the airport.
        longitude (float): The longitude of the airport.
        geom (shapely.geometry.Point): The location of the airport as a shapely point.
        departing_flights (list): A list of flights that depart from this airport.
        arriving_flights (list): A list of flights that arrive at this airport.
    """
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
    """
    The Airlines class represents airlines in the system.

    Attributes:
        id (int): The primary key of the airline.
        code (str): The IATA code of the airline.
        name (str): The name of the airline.
    """
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Flights(Base):
    """
      The Flights class represents flights in the system.

      Attributes:
          id (int): The primary key of the flight.
          flight_status (str): The status of the flight.
          flight_number (str): The flight number of the flight.
          available_seats (str): The available seats of the flight.
          departure_airport_id (int): The ID of the departure airport.
          arrival_airport_id (int): The ID of the arrival airport.
          departure_date (str): The departure date of the flight.
          arrival_date (str): The arrival date of the flight.
          duration (int): The duration of the flight in minutes.
          fare (float): The fare of the flight.

      Methods:
          get_departure_airport(): Returns the departure airport of the flight.
          get_arrival_airport(): Returns the arrival airport of the flight.
      """
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


class Passengers(Base):
    """
    The Passengers class represents passengers in the system.

    Attributes:
        id (int): The primary key of the passenger.
        flight_id (int): The ID of the flight the passenger is on.
        first_name (str): The first name of the passenger.
        last_name (str): The last name of the passenger.
        date_of_birth (str): The date of birth of the passenger.
        passport_number (str): The passport number of the passenger.

    Methods:
        get_flight(): Returns the flight the passenger is on.
    """
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey('flights.id'), index=True)
    first_name = Column(VARCHAR(255), index=True)
    last_name = Column(VARCHAR(255), index=True)
    date_of_birth = Column(String, index=True)
    passport_number = Column(VARCHAR(255), index=True)

    departure_airport = relationship("Flights", backref="passenger_flights", foreign_keys=[flight_id])

