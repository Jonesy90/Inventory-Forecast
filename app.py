#Internal Imports
# from tracemalloc import start
from queue import Empty
from sqlalchemy import null
from models import *
from excel_export import *
from functools import reduce

#External Imports
import argparse
import pathlib
import csv
import datetime
import calendar


parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')
args = parser.parse_args()

booking_uploaded_csv = args.source_file

def daily_average(start_date, end_date, booked_impressions, delivered_impressions):
    """
    Calculates the daily average for each booking within the Bookings DB.

    """       
    today = datetime.date.today()

    if today >= end_date:
        return 0
    elif today <= start_date:
        days_running = end_date - start_date
        average_impressions = int(booked_impressions) / (int(days_running.days) + 1)
    elif today >= start_date:
        days_remaining = end_date - today
        remaining_impressons = int(booked_impressions) - int(delivered_impressions)
        average_impressions = int(remaining_impressons) / (int(days_remaining.days) + 1)
    return int(average_impressions)


def add_campaign_bookings():
    """
    Reads the CSV file and adds to the Bookings DB.

    Error Handling:
    1. Campaign External ID: This can return a blank. Not required when calculating forecasting.
    2. Campaign Name; This is required. Should return error if not filled in. Required when updating the 'Entertainment'
        and 'Kids' DBs.
    3. Start & End Date: This is required to calculate the amount needed per day. Will return a 'ValueError' is incorrect.
    4. Booked Impressions: Required. To calculate the daily impressions needed.
    5. Daily Impressions: Required. Dependent on other metrics (Remaining Impressions and days running).

    """
    
    with open(booking_uploaded_csv) as csvfile:
        data = csv.DictReader(csvfile)
        try:
            for row in data:
                campaign_external_id = row['\ufeffCampaign External ID']
                campaign_name = row['Campaign']
                start_date = datetime.datetime.strptime(row['Campaign Start Date'], '%d/%m/%Y').date()
                end_date = datetime.datetime.strptime(row['Campaign End Date'], '%d/%m/%Y').date()
                content_group = row['Content Group']
                booked_impressions = row['Booked Impressions'].replace(',', '')
                delivered_impressions = row['Impressions'].replace(',', '')
                daily_impressions = daily_average(start_date, end_date, booked_impressions, delivered_impressions)

                new_booking = Bookings(campaign_external_id=campaign_external_id, campaign_name=campaign_name, start_date=start_date, end_date=end_date, content_group=content_group, booked_impressions=booked_impressions, delivered_impressions=delivered_impressions, daily_impressions=daily_impressions)
                booking_in_db = session.query(Bookings).filter(Bookings.campaign_external_id==new_booking.campaign_external_id).one_or_none()

                if booking_in_db != None:
                    pass
                else:
                    session.add(new_booking)
                    session.commit()
        except ValueError:
            print('ValueError: Start Date and/or End Date incorrect. Check CSV and resubmit.')


def current_status():
    """
    Calculates the current status of Inventory Available, Inventory Used and Inventory Remaining through the current month.

    """
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        entertainment_forecast_data = Entertainment_Forecast(
            date=start_date,
            inventory_available=150000,
            inventory_used=reduce(get_entertainment_inventory_used,[booking.daily_impressions for booking in session.query(Bookings).all() 
                if booking.content_group == '3|Ex Kids Content' and start_date <= booking.end_date])
        )
        kids_forecast_data = Kids_Forecast(date=start_date,
            inventory_available=50000,
            inventory_used=reduce(get_kids_inventory_used, [booking.daily_impressions for booking in session.query(Bookings).all() 
                if booking.content_group == '3|Kids Content' and start_date <= booking.end_date])
        )

        entertainment_in_db = session.query(Entertainment_Forecast).filter(Entertainment_Forecast.date==entertainment_forecast_data.date).one_or_none()
        kids_in_db = session.query(Kids_Forecast).filter(Kids_Forecast.date==entertainment_forecast_data.date).one_or_none()

        if entertainment_in_db != None:
            pass
        else:
            session.add(entertainment_forecast_data)
            session.commit()

        if kids_in_db != None:
            pass
        else:
            session.add(kids_forecast_data)
            session.commit()

        start_date += delta


def get_remaining_inventory(booking):
    print(booking.inventory_available)
    return booking.inventory_available - booking.inventory_used

def get_entertainment_inventory_used(booking1, booking2):
    return booking1 + booking2

def get_kids_inventory_used(booking1, booking2):
    return booking1 + booking2


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_campaign_bookings()
    current_status()
    create_workbook()