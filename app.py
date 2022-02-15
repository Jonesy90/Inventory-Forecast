#Internal Imports
from models import *

#External Imports
import argparse
import pathlib
import csv
import datetime

from models import Bookings

parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')
args = parser.parse_args()

booking_uploaded_csv = args.source_file

def menu():
    """
    After the CSV has been uploaded, a menu will appear for the user to make a collection.
    
    """
    while True:
        print('''
            \n*****MAIN MENU*****:
            \rf : FORECAST
            \rd : EXPORT
            \re : EXIT
            ''')
        users_choice = input('Please select an option: ').lower()
        if users_choice in ['f', 'e']:
            return users_choice
        else:
            users_choice = input('''
            \n**********MENU ERROR***********
            \rInvalid Option
            \rPress Enter to try again.
            \r*****************************''')


def daily_average(campaign_external_id):
    """
    Calculate the daily average for each booking within the Bookings DB.

    """
    # print(campaign_external_id)
    campaign = session.query(Bookings).filter(Bookings.campaign_external_id==campaign_external_id)
    today = datetime.date.today()
    
    for camp in campaign:
        days_running = (camp.end_date - camp.start_date)
        print(f'Days Running: {int(days_running.days) + 1}')


def add_campaign_bookings():
    """
    Read a CSV file to and add to the Bookings DB.

    """
    
    with open(booking_uploaded_csv, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            campaign_external_id = row['\ufeffCampaign External ID']
            campaign_name = row['Campaign Name']
            start_date = datetime.datetime.strptime(row['Start Date'], '%d/%m/%Y').date()
            end_date = datetime.datetime.strptime(row['End Date'], '%d/%m/%Y').date()
            booked_impressions = row['Booked Impressions']
            delivered_impressions = row['Delivered Impressions']
            daily_impressions = daily_average(campaign_external_id)

            new_booking = Bookings(campaign_external_id=campaign_external_id, campaign_name=campaign_name, start_date=start_date, end_date=end_date, booked_impressions=booked_impressions, delivered_impressions=delivered_impressions, daily_impressions=daily_impressions)
            booking_in_db = session.query(Bookings).filter(Bookings.campaign_external_id==new_booking.campaign_external_id).one_or_none()

            if booking_in_db != None:
                pass
            else:
                session.add(new_booking)
                session.commit()


def app():
    add_campaign_bookings()
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'f':
            print('FORECAST')
        elif choice == 'd':
            print('EXPORT')
        elif choice == 'e':
            print('EXIT')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()