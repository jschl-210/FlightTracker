from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import Json
import json

from .schemas import airports, flights, passengers, airlines
from .models import Flights, Airports, Passengers, Airlines


def create_airports(db: Session, airport: airports.AirportsCreate):
    """
    Create a new airport in the database

    Args:
        db (Session): The database session
        airport (airports.AirportsCreate): The airport to create

    Returns:
        airports.Airports: The created airport
    """
    db_airports = Airports(**airport.model_dump())
    db.add(db_airports)
    db.commit()
    db.refresh(db_airports)
    return db_airports


def check_airports_exists(db: Session,
                          airports_id: int) -> bool:
    return db.query(Airports.id).filter_by(id=airports_id).first() is not None


def get_airports(db: Session,
                 airport_id: [int] = None,
                 city: [str] = None,
                 country: [str] = None,
                 limit: int = 100):
    """
        Get a list of airports based on the provided filters.

        Args:
            db (Session): The database session
            airport_id (list, optional): A list of airport IDs. Defaults to None.
            city (list, optional): A list of cities. Defaults to None.
            country (list, optional): A list of countries. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to 100.

        Returns:
            list: A list of airports that match the provided filters.
        """
    return db.query(Airports) \
        .filter_if(airport_id is not None,
                   Airports.id.in_(airport_id if airport_id is not None else [])) \
        .filter_if(city is not None, Airports.city.in_(city if city is not None else [])) \
        .filter_if(country is not None, Airports.country.in_(country if country is not None else [])) \
        .limit(limit).all()


def create_airlines(db: Session, airline: airlines.AirlinesCreate):
    """
    Create a new airline in the database

    Args:
        db (Session): The database session
        airline (airlines.AirlinesCreate): The airline to create

    Returns:
        airlines.Airlines: The created airline
    """
    db_airlines = Airports(**airline.model_dump())
    db.add(db_airlines)
    db.commit()
    db.refresh(db_airlines)
    return db_airlines


def check_airlines_exists(db: Session,
                          airlines_id: int) -> bool:
    return db.query(Airlines.id).filter_by(id=airlines_id).first() is not None


def get_airlines(db: Session,
                 airline_id: [int] = None,
                 name: [str] = None,
                 alliance: [str] = None,
                 limit: int = 100) -> Airlines:
    return db.query(Airlines) \
        .filter_if(airline_id is not None,
                   Airlines.id.in_(airline_id if airline_id is not None else [])) \
        .filter_if(name is not None, Airlines.name.in_(name if name is not None else [])) \
        .filter_if(alliance is not None, Airlines.alliance.in_(alliance if alliance is not None else [])) \
        .limit(limit).all()


def get_flights(db: Session,
                departure_airport: [str] = None,
                arrival_airport: [str] = None,
                departure_date: [str] = None,
                arrival_date: [str] = None,
                limit: int = 100):
    """
        Get a list of flights based on the provided filters.

        Args:
            db (Session): The database session
            departure_airport (list, optional): A list of departure airport IATA codes.
                Defaults to None.
            arrival_airport (list, optional): A list of arrival airport IATA codes.
                Defaults to None.
            departure_date (list, optional): A list of departure dates in YYYY-MM-DD format.
                Defaults to None.
            arrival_date (list, optional): A list of arrival dates in YYYY-MM-DD format.
                Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to 100.

        Returns:
            list: A list of flights that match the provided filters.
        """
    return db.query(Flights) \
        .filter_if(departure_airport is not None,
                   Flights.id.in_(departure_airport if departure_airport is not None else [])) \
        .filter_if(arrival_airport is not None,
                   Flights.id.in_(arrival_airport if arrival_airport is not None else [])) \
        .filter_if(departure_date is not None,
                   Flights.id.in_(departure_date if departure_date is not None else [])) \
        .filter_if(arrival_date is not None, Flights.id.in_(arrival_date if arrival_date is not None else [])) \
        .limit(limit).all()


def check_flights_exists(db: Session,
                         flight_id: int) -> bool:
    return db.query(Flights.id).filter_by(id=flight_id).first() is not None


def create_flights(db: Session, flight: flights.FlightsCreate):
    db_flights = Flights(**flight.model_dump())
    db.add(db_flights)
    db.commit()
    db.refresh(db_flights)
    return db_flights


def get_flight_by_id(db: Session, flight_id: int):
    return db.query(Flights).filter_by(id=flight_id).first()


def update_flights(db: Session, flight_id: int, flight_update: flights.FlightsUpdate):
    flight = get_flight_by_id(db=db, flight_id=flight_id)
    if not flight:
        raise ValueError(f"Flight with id {flight_id} does not exist")
    flight.update(**flight_update.model_dump())
    db.commit()
    db.refresh(flight)
    return Flights.from_orm(flight)


def delete_flights(db: Session, flight_id: int):
    flight = get_flight_by_id(db=db, flight_id=flight_id)
    if flight:
        db.delete(flight)
        db.commit()
    else:
        raise ValueError(f"Passenger with id {flight_id} does not exist")


def create_passengers(db: Session, passenger: passengers.PassengersCreate):
    db_passengers = Passengers(**passenger.model_dump())
    db.add(db_passengers)
    db.commit()
    db.refresh(db_passengers)
    return db_passengers


def check_passengers_exists(db: Session,
                            flight_id: int) -> bool:
    return db.query(Passengers.id).filter_by(id=flight_id).first() is not None


def get_passengers(db: Session,
                   passenger_id: [int] = None,
                   first_name: [str] = None,
                   last_name: [str] = None,
                   passport_number: [str] = None,
                   limit: int = 100):
    return db.query(Passengers) \
        .filter_if(passenger_id is not None,
                   Passengers.id.in_(passenger_id if passenger_id is not None else [])) \
        .filter_if(first_name is not None,
                   Passengers.first_name.in_(first_name if first_name is not None else [])) \
        .filter_if(last_name is not None,
                   Passengers.last_name.in_(last_name if last_name is not None else [])) \
        .filter_if(passport_number is not None,
                   Passengers.passport_number.in_(passport_number if passport_number is not None else [])) \
        .limit(limit).all()


def get_passenger_by_id(db: Session, passenger_id: int):
    return db.query(Passengers).filter_by(id=passenger_id).first()


def update_passengers(db: Session, passenger_id: int,
                      passenger_update: passengers.PassengersUpdate) -> passengers.Passengers:
    passenger = get_passenger_by_id(db=db, passenger_id=passenger_id)
    if not passenger:
        raise ValueError(f"Passenger with id {passenger_id} does not exist")
    passenger.update(**passenger_update.model_dump())
    db.commit()
    db.refresh(passenger)
    return Passengers.from_orm(passenger)


def delete_passengers(db: Session, passenger_id: int) -> None:
    passenger = get_passenger_by_id(db=db, passenger_id=passenger_id)
    if passenger:
        db.delete(passenger)
        db.commit()
    else:
        raise ValueError(f"Passenger with id {passenger_id} does not exist")
