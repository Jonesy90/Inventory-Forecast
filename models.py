from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory-forecast.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Bookings(Base):
    __tablename__ = "Bookings"

    id = Column(Integer, primary_key=True)
    campaign_external_id = Column('Campaign External ID', String)
    campaign_name = Column('Campaign Name', String)
    start_date = Column('Start Date', Date)
    end_date = Column('End Date', Date)
    booked_impressions = Column('Booked Impressions', Integer)
    delivered_impressions = Column('Delivered Impressions', Integer)
    daily_impressions = Column('Daily Impressions', Integer)

    def __repr__(self):
        return f'<Bookings(Campaign External ID={self.campaign_external_id}, Campaign Name={self.campaign_name}, Start Date={self.start_date}, End Date={self.end_date}, Booked Impressions={self.booked_impressions}, Delivered Impressions={self.delivered_impressions}, Daily Impressions={self.daily_impressions})>'

    
class Forecast(Base):
    __tablename__ = 'Forecast'

    id = Column(Integer, primary_key=True)
    date = Column('Date', Date)
    inventory_available = Column('Inventory Available', Integer)
    inventory_used = Column('Inventory Used', Integer)
    inventory_remaining = Column('Inventory Remaining', Integer)

    def __repr__(self):
        return f'<Forecast(Date={self.date}, Inventory Available={self.inventory_available}, Inventory Used={self.inventory_used}, Inventory Remaining={self.inventory_remaining})>'