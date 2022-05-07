from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory-forecast.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Bookings(Base):
    __tablename__ = "Bookings"

    id = Column(Integer, primary_key=True)
    campaign_external_id = Column('Campaign External ID', String, nullable=False)
    campaign_name = Column('Campaign', String)
    start_date = Column('Campaign Start Date', Date)
    end_date = Column('Campaign End Date', Date)
    content_group = Column('Content Group', String, nullable=False)
    booked_impressions = Column('Booked Impressions', Integer)
    delivered_impressions = Column('Impressions', Integer)
    daily_impressions = Column('Daily Impressions', Integer)

    def __repr__(self):
        return f'<Bookings(Campaign External ID={self.campaign_external_id}, Campaign Name={self.campaign_name}, Start Date={self.start_date}, End Date={self.end_date}, Content Group={self.content_group}, Booked Impressions={self.booked_impressions}, Delivered Impressions={self.delivered_impressions}, Daily Impressions={self.daily_impressions})>'

    
class Entertainment_Forecast(Base):
    __tablename__ = 'Entertainment_Forecast'

    id = Column(Integer, primary_key=True)
    date = Column('Date', Date)
    inventory_available = Column('Inventory Available', Integer)
    inventory_used = Column('Inventory Used', Integer)

    @hybrid_property
    def inventory_remaining(self):
        return self.inventory_available - self.inventory_used

    def __repr__(self):
        return f'<Entertainment_Forecast(Date={self.date}, Inventory Available={self.inventory_available}, Inventory Used={self.inventory_used}, Inventory Remaining={self.inventory_remaining})>'


class Kids_Forecast(Base):
    __tablename__ = 'Kids_Forecast'

    id = Column(Integer, primary_key=True)
    date = Column('Date', Date)
    inventory_available = Column('Inventory Available', Integer)
    inventory_used = Column('Inventory Used', Integer)

    @hybrid_property
    def inventory_remaining(self):
        return self.inventory_available - self.inventory_used

    def __repr__(self):
        return f'<Kids_Forecast(Date={self.date}, Inventory Available={self.inventory_available}, Inventory Used={self.inventory_used}, Inventory Remaining={self.inventory_remaining})>'