import datetime

from faker import Faker
from faker_airtravel import AirTravelProvider
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flightapi.db_config import DATABASE_URL
from flightapi.models import Airports, Flights, Passengers

if __name__ == "__main__":
    engine = create_engine(
        DATABASE_URL, echo=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

faker = Faker()

faker.add_provider(AirTravelProvider)

num_airports = 10
num_airlines = 15
num_flights = 50
num_passengers = 25

# airports_code = faker.airports_object()

for i in range(num_airports):
    airports_code = faker.airport_object()
    code = faker.airport_iata()
    unique_code = [i for i in code if code.count(i) == 1]
    name = airports_code.get('airport')
    city = airports_code.get('city')
    country = airports_code.get('country')
    session.add_all(
        [
            Airports(
                code=code,
                name=name,
                city=city,
                country=country,
            )
        ]
    )

for i in range(num_flights):
    airport = faker.flight()
    print(airport)
    departure_airport = random.choice(airport['origin'].get('iata'))
    arrival_airport = random.choice(airport['destination'].get('iata'))
    print(departure_airport)
    arrival_airport_code = airport.get('iata')
    departure_date = faker.date_this_year(after_today=True)
    arrival_date = departure_date + datetime.timedelta(days=random.randint(1, 12))
    session.add_all(
        [
            Flights(
                # airline_id=random.randint(1, num_airlines),
                flight_status=random.choice(["On Time", "Delayed", "Cancelled"]),
                flight_number= random.randint(100, 900),
                available_seats=faker.text(max_nb_chars=5),
                departure_airport_id=random.randint(1, num_airports),
                arrival_airport_id=random.randint(1, num_airports),
                departure_date=departure_date.strftime("%Y-%m-%d"),
                arrival_date=arrival_date.strftime("%Y-%m-%d"),
                duration=random.randint(30, 360),
                fare=random.randint(1000, 100000),

            )
            ]
    )
for i in range(num_passengers):
    session.add_all(
        [
            Passengers(
                flight_id=random.randint(1, num_flights),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                date_of_birth=faker.date_this_year(after_today=True).strftime("%Y-%m-%d"),
                passport_number=faker.passport_number(),
            )
        ]
    )

session.commit()
