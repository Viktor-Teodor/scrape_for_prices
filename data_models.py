from datetime import date

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
from sqlalchemy import create_engine
from typing import List

# Create an SQLite database
engine = create_engine('sqlite:///flats.db', echo=True)  

class Base(DeclarativeBase):
    pass

# Define the Property model
class Property(Base):
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(primary_key = True)
    external_id: Mapped[int] = mapped_column(nullable = False)
    title: Mapped[str] = mapped_column(nullable = False, index = True)
    address:Mapped[str] = mapped_column(nullable = False)
    floor_number: Mapped[int] = mapped_column(nullable = False)
    construction_year: Mapped[int] = mapped_column(nullable = False)
    ammenities: Mapped[List[str]] = mapped_column(nullable = False)
    description: Mapped[str]
    num_rooms:Mapped[int] = mapped_column(nullable = False)
    surface:Mapped[float] = mapped_column(nullable = False)  # Assuming surface area in square meters
    price:Mapped[float] = mapped_column(nullable = False)
    currency:Mapped[str] = mapped_column(nullable = False)
    listing_type:Mapped[str] = mapped_column(nullable = False)  # 'rent' or 'sale'
    property_type: Mapped[str] = mapped_column(nullable = False) # flat, penthouse, house 
    compartment_types: Mapped[str] = mapped_column(nullable = False) # Semi-detached, Open-plan, Closed-plan
    date_posted:Mapped[int] = mapped_column(nullable = False) #UNIX time

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
session = Session(engine)

# Query the data (optional)
all_properties = session.query(Property).all()
for property in all_properties:
    print(property.address, property.price)

