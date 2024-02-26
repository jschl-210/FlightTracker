import os
from contextlib import asynccontextmanager
from logging import basicConfig, DEBUG, getLogger
from sys import stdout
from typing import Annotated, Optional

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sqlalchemy.orm import Session

from . import crud, config
from .crud import check_flights_exists, check_airports_exists
from .database import get_db
from .schemas import flights, airports, passengers

basicConfig(stream=stdout, level=DEBUG)
logger = getLogger()


def run_migrations():
    alembic_cfg = Config("flightapi/alembic/alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Running db migration")
    run_migrations()
    yield
    logger.info("Done")


app = FastAPI(
    title="Flight API - one stop shop to track flights and book them",
    description="The Flight API will allow users to interact with flight data and figure out the best one to book",
    version="1.0",
    lifespan=lifespan,
)


@app.get("/healthchecker")
def home():
    return {"message": "Flight API is up and running"}


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    logger.info("Flight Tracker API '/docs' accessed.")
    return get_swagger_ui_html(
        openapi_url=os.path.join(config.SERVICE_CONFIG.api.root_path, "openapi.json"),
        title=app.title,
        # swagger_js_url="static/swagger-ui-bundle.js",
        # swagger_css_url="static/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    logger.info("Flight Tracker API '/redoc' accessed.")
    return get_redoc_html(
        openapi_url=os.path.join(config.SERVICE_CONFIG.api.root_path, "openapi.json"),
        title=app.title,
        redoc_js_url="static/redoc.standalone.js",
    )


@app.get(
    "/airports/list",
    response_model=list[airports.Airports],
    summary="Return airport data",
    tags=["Airports"],
)
def get_airports(
        airport_id: Annotated[Optional[list[int]], Query()] = None,
        city: Annotated[Optional[list[str]], Query()] = None,
        country: Annotated[Optional[list[str]], Query()] = None,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
        Get a list of airports based on the provided filters.

        Args:
            airport_id (Optional[List[int]]): A list of airport IDs to filter by.
            city (Optional[List[str]]): A list of cities to filter by.
            country (Optional[List[str]]): A list of countries to filter by.
            limit (int, optional): The maximum number of results to return. Defaults to 100.
            db (Session): The database session to use.

        Returns:
            List[airports.Airports]: A list of airport objects that match the provided filters.
        """
    airport_result = crud.get_airports(
        db,
        airport_id=airport_id,
        city=city,
        country=country,
        limit=limit
    )
    return airport_result


# We should only check to see if the departing airport exists in order to create a flight
@app.post(
    "/flights/create",
    response_model=flights.Flights,
    summary="Create a new flight",
    tags=["Flights"],
)
def create_flights(flight: flights.FlightsCreate, db: Session = Depends(get_db)):
    """
    Create a new flight.

    Args:
        flight (FlightsCreate): The flight to create.
        db (Session): The database session to use.

    Returns:
        Flights: The created flight.

    Raises:
        HTTPException: If the departure airport does not exist.
    """
    if not check_airports_exists(db, flight.departure_airport_id):
        raise HTTPException(status_code=400, detail="Departure airport does not exist")
    return crud.create_flights(db, flight)


# Return all flights or a specific flight
@app.get(
    "/flights/list",
    response_model=list[flights.Flights],
    summary="Return flight data",
    tags=["Flights"],
)
def get_flights(
        departure_airport: Annotated[Optional[list[str]], Query()] = None,
        arrival_airport: Annotated[Optional[list[str]], Query()] = None,
        departure_date: Annotated[Optional[list[str]], Query()] = None,
        arrival_date: Annotated[Optional[list[str]], Query()] = None,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
    Get a list of flights based on the provided filters.

    Args:
        departure_airport (Optional[List[str]]): A list of departure airports to filter by.
        arrival_airport (Optional[List[str]]): A list of arrival airports to filter by.
        departure_date (Optional[List[str]]): A list of departure dates to filter by.
        arrival_date (Optional[List[str]]): A list of arrival dates to filter by.
        limit (int, optional): The maximum number of results to return. Defaults to 100.
        db (Session): The database session to use.

    Returns:
        List[flights.Flights]: A list of flight objects that match the provided filters.
    """
    flight_results = crud.get_flights(
        db,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        departure_date=departure_date,
        arrival_date=arrival_date,
        limit=limit
    )
    return flight_results


@app.put(
    "/flights/update/{flight_id}",
    response_model=flights.Flights,
    summary="Update a flight",
    tags=["Flights"],
)
def update_flight(flight_id: int, flight: flights.FlightsUpdate, db: Session = Depends(get_db)):
    """
    Update an existing flight.

    Args:
        flight_id (int): The ID of the flight to update.
        flight (FlightsUpdate): The updated flight information.
        db (Session): The database session to use.

    Returns:
        Flights: The updated flight information.

    Raises:
        HTTPException: If the flight does not exist.
    """
    existing_flight = crud.get_flights(db, flight_id)
    if not existing_flight:
        raise HTTPException(
            status_code=400,
            detail=f"Flight ={flight_id} does not exist",
        )
    updated_flight = crud.update_flights(db, flight_id, flight)
    return updated_flight


@app.delete(
    "/flights/delete/{flight_id}",
    summary="Delete a flight",
    tags=["Flights"],
)
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    crud.delete_flights(db, flight_id)
    return None


# When we create a new passenger, we need to check if the flight exists
@app.post(
    "/passengers/create",
    response_model=passengers.Passengers,
    summary="Create a new passenger",
    tags=["Passengers"],
)
def create_passengers(passenger: passengers.PassengersCreate, db: Session = Depends(get_db)
                      ):
    """
    Create a new passenger.

    Args:
        passenger (PassengersCreate): The passenger to create.
        db (Session): The database session to use.

    Returns:
        Passengers: The created passenger.

    Raises:
        HTTPException: If the flight does not exist.
    """
    if not check_flights_exists(db, passenger.flight_id):
        raise HTTPException(
            status_code=400,
            detail=f"Flight ={passenger.flight_id} does not exist",
        )
    return crud.create_passengers(db, passenger)


# We can return all passengers or a specific passenger by id
@app.get(
    "/passengers/list",
    response_model=list[passengers.Passengers],
    summary="Return passenger data",
    tags=["Passengers"],
)
def get_passengers(
        passenger_id: Annotated[Optional[list[int]], Query()] = None,
        first_name: Annotated[Optional[list[str]], Query()] = None,
        last_name: Annotated[Optional[list[str]], Query()] = None,
        passport_number: Annotated[Optional[list[str]], Query()] = None,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
        Get a list of passengers based on the provided filters.

        Args:
            passenger_id (Optional[List[int]]): A list of passenger IDs to filter by.
            first_name (Optional[List[str]]): A list of first names to filter by.
            last_name (Optional[List[str]]): A list of last names to filter by.
            passport_number (Optional[List[str]]): A list of passport numbers to filter by.
            limit (int, optional): The maximum number of results to return. Defaults to 100.
            db (Session): The database session to use.

        Returns:
            List[passengers.Passengers]: A list of passenger objects that match the provided filters.
        """
    passenger_result = crud.get_passengers(
        db,
        passenger_id=passenger_id,
        first_name=first_name,
        last_name=last_name,
        passport_number=passport_number,
        limit=limit
    )
    return passenger_result


# Update a passenger by id
@app.put(
    "/passengers/update/{passenger_id}",
    response_model=passengers.Passengers,
    summary="Update a passenger",
    tags=["Passengers"],
)
def update_passenger(passenger_id: int, passenger_update: passengers.PassengersUpdate, db: Session = Depends(get_db)):
    """
    Update a passenger.

    Args:
        passenger_id (int): The ID of the passenger to update.
        passenger_update (PassengersUpdate): The updated passenger information.
        db (Session): The database session to use.

    Returns:
        Passengers: The updated passenger information.

    Raises:
        HTTPException: If the passenger does not exist.
    """
    # Check if the passenger exists
    existing_passenger = crud.get_passengers(db, passenger_id=passenger_id)
    if not existing_passenger:
        raise HTTPException(
            status_code=400,
            detail=f"Passenger ={passenger_id} does not exist",
        )
    updated_passenger = crud.update_passengers(db, passenger_id, passenger_update)
    return updated_passenger


# Delete a passenger by id
@app.delete(
    "/passengers/delete/{passenger_id}",
    response_model=None,
    summary="Delete a passenger",
    tags=["Passengers"],
)
def delete_passenger(passenger_id: int, db: Session = Depends(get_db)):
    # Check if the passenger exists
    crud.delete_passengers(db, passenger_id)
    return None