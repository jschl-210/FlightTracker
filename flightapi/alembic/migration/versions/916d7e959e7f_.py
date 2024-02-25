"""empty message

Revision ID: 916d7e959e7f
Revises: 
Create Date: 2024-02-25 19:26:01.548050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '916d7e959e7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('airlines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('airports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.VARCHAR(length=3), nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('city', sa.VARCHAR(length=255), nullable=True),
    sa.Column('country', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_airports_code'), 'airports', ['code'], unique=True)
    op.create_index(op.f('ix_airports_id'), 'airports', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), nullable=True),
    sa.Column('password', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('flights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_status', sa.String(), nullable=True),
    sa.Column('flight_number', sa.String(), nullable=True),
    sa.Column('available_seats', sa.String(), nullable=True),
    sa.Column('departure_airport_id', sa.Integer(), nullable=True),
    sa.Column('arrival_airport_id', sa.Integer(), nullable=True),
    sa.Column('departure_date', sa.String(), nullable=True),
    sa.Column('arrival_date', sa.String(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('fare', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['arrival_airport_id'], ['airports.id'], ),
    sa.ForeignKeyConstraint(['departure_airport_id'], ['airports.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flights_arrival_airport_id'), 'flights', ['arrival_airport_id'], unique=False)
    op.create_index(op.f('ix_flights_arrival_date'), 'flights', ['arrival_date'], unique=False)
    op.create_index(op.f('ix_flights_available_seats'), 'flights', ['available_seats'], unique=False)
    op.create_index(op.f('ix_flights_departure_airport_id'), 'flights', ['departure_airport_id'], unique=False)
    op.create_index(op.f('ix_flights_departure_date'), 'flights', ['departure_date'], unique=False)
    op.create_index(op.f('ix_flights_duration'), 'flights', ['duration'], unique=False)
    op.create_index(op.f('ix_flights_fare'), 'flights', ['fare'], unique=False)
    op.create_index(op.f('ix_flights_flight_number'), 'flights', ['flight_number'], unique=False)
    op.create_index(op.f('ix_flights_flight_status'), 'flights', ['flight_status'], unique=False)
    op.create_index(op.f('ix_flights_id'), 'flights', ['id'], unique=False)
    op.create_table('passengers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('date_of_birth', sa.String(), nullable=True),
    sa.Column('passport_number', sa.VARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passengers_date_of_birth'), 'passengers', ['date_of_birth'], unique=False)
    op.create_index(op.f('ix_passengers_first_name'), 'passengers', ['first_name'], unique=False)
    op.create_index(op.f('ix_passengers_flight_id'), 'passengers', ['flight_id'], unique=False)
    op.create_index(op.f('ix_passengers_id'), 'passengers', ['id'], unique=False)
    op.create_index(op.f('ix_passengers_last_name'), 'passengers', ['last_name'], unique=False)
    op.create_index(op.f('ix_passengers_passport_number'), 'passengers', ['passport_number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_passengers_passport_number'), table_name='passengers')
    op.drop_index(op.f('ix_passengers_last_name'), table_name='passengers')
    op.drop_index(op.f('ix_passengers_id'), table_name='passengers')
    op.drop_index(op.f('ix_passengers_flight_id'), table_name='passengers')
    op.drop_index(op.f('ix_passengers_first_name'), table_name='passengers')
    op.drop_index(op.f('ix_passengers_date_of_birth'), table_name='passengers')
    op.drop_table('passengers')
    op.drop_index(op.f('ix_flights_id'), table_name='flights')
    op.drop_index(op.f('ix_flights_flight_status'), table_name='flights')
    op.drop_index(op.f('ix_flights_flight_number'), table_name='flights')
    op.drop_index(op.f('ix_flights_fare'), table_name='flights')
    op.drop_index(op.f('ix_flights_duration'), table_name='flights')
    op.drop_index(op.f('ix_flights_departure_date'), table_name='flights')
    op.drop_index(op.f('ix_flights_departure_airport_id'), table_name='flights')
    op.drop_index(op.f('ix_flights_available_seats'), table_name='flights')
    op.drop_index(op.f('ix_flights_arrival_date'), table_name='flights')
    op.drop_index(op.f('ix_flights_arrival_airport_id'), table_name='flights')
    op.drop_table('flights')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_airports_id'), table_name='airports')
    op.drop_index(op.f('ix_airports_code'), table_name='airports')
    op.drop_table('airports')
    op.drop_table('airlines')
    # ### end Alembic commands ###
