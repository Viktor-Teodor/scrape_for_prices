from datetime import date

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# Create an SQLite database
engine = create_engine('sqlite:///flats.db')  

class Base(DeclarativeBase):
    pass

# Define the Property model
class Property(Base):
    __tablename__ = 'properties'

    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    address:Mapped[str] = mapped_column(String, nullable=False)
    num_rooms:Mapped[int] = mapped_column(Integer)
    surface:Mapped[float] = mapped_column(Float)  # Assuming surface area in square meters
    price:Mapped[float] = mapped_column(Float, nullable=False)
    currency:Mapped[str] = mapped_column(String, nullable=False)
    listing_type:Mapped[str] = mapped_column(String, nullable=False)  # 'rent' or 'sale'
    date_posted:Mapped[int] = mapped_column(int, nullable=False) #UNIX time

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine) 
session = Session()

# Query the data (optional)
all_properties = session.query(Property).all()
for property in all_properties:
    print(property.address, property.price)

