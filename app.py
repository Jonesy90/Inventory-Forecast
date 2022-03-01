#Internal Imports
from tracemalloc import start
from models import *
from excel_export import *
from functools import reduce
# from models import Bookings

#External Imports
import argparse
import pathlib
import csv
import datetime


parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')
args = parser.parse_args()

booking_uploaded_csv = args.source_file

def daily_average(start_date, end_date, booked_impressions, delivered_impressions):
    """
    Calculates the daily average for each booking within the Bookings DB.

    """       
    today = datetime.date.today()
    # print(start_date)
    # print(end_date)
    # print(booked_impressions)
    # print(delivered_impressions)

    if today >= end_date:
        return 0
    elif today <= start_date:
        days_running = end_date - start_date
        average_impressions = int(booked_impressions) / (int(days_running.days) + 1)
        # print(f'{campaign_name} average Impr: {int(average_impressions)}')
    elif today >= start_date:
        days_remaining = end_date - today
        remaining_impressons = int(booked_impressions) - int(delivered_impressions)
        average_impressions = int(remaining_impressons) / (int(days_remaining.days) + 1)
        # print(f'{campaign_name} average Impr: {int(average_impressions)}')
    return int(average_impressions)


def add_campaign_bookings():
    """
    Reads the CSV file and adds to the Bookings DB.

    """
    
    with open(booking_uploaded_csv) as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            # print(row)
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


def current_status():
    """
    Calculates the current status of Inventory Available, Inventory Used and Inventory Remaining through the current month.
    FIX/UPDATES:
    1. Figure out a way to dynamically update the start and end date.

    """

    # fixed_start_date = datetime.date(2022, 3, 1)
    start_date = datetime.date(2022, 3, 1)
    end_date = datetime.date(2022, 3, 31)
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