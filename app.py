#Internal Imports
from tracemalloc import start
from models import *

#External Imports
import argparse
import pathlib
import csv
import datetime
import xlsxwriter

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


def daily_average(start_date, end_date, booked_impressions, delivered_impressions, campaign_name):
    """
    Calculate the daily average for each booking within the Bookings DB.

    """       
    today = datetime.date.today()

    if today >= end_date or today <= start_date:
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
    Read a CSV file to and add to the Bookings DB.

    """
    
    with open(booking_uploaded_csv, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            campaign_external_id = row['Campaign External ID']
            campaign_name = row['Campaign']
            start_date = datetime.datetime.strptime(row['Campaign Start Date'], '%d/%m/%Y').date()
            end_date = datetime.datetime.strptime(row['Campaign End Date'], '%d/%m/%Y').date()
            content_group = row['Content Group']
            booked_impressions = row['Campaign Booked Impressions'].replace(',', '')
            delivered_impressions = row['Impressions'].replace(',', '')
            daily_impressions = daily_average(start_date, end_date, booked_impressions, delivered_impressions, campaign_name)

            new_booking = Bookings(campaign_external_id=campaign_external_id, campaign_name=campaign_name, start_date=start_date, end_date=end_date, content_group=content_group, booked_impressions=booked_impressions, delivered_impressions=delivered_impressions, daily_impressions=daily_impressions)
            booking_in_db = session.query(Bookings).filter(Bookings.campaign_external_id==new_booking.campaign_external_id).one_or_none()

            if booking_in_db != None:
                pass
            else:
                session.add(new_booking)
                session.commit()


def forecast():
    """
    Populate the Forecast DB.
    DATE: It would have every date within the current month.
    INVENTORY AVAILABLE: The average amount of Inventory available.
    INVENTORY USED: The amount of inventory used per day.
    INVENTORY REMAINING: The amount of inventory remaining per day.

    FIX:
    1. Figure out a way to dynamically update the start and end date.
    2. Loop over the Bookings DB.
        a. If the campaign is live on the day, add the daily average impressions.
    3. The USED INVENTORY and INVENTORY AVAILABLE is not totalling up to the inventory available.

    """
    fixed_start_date = datetime.date(2022, 2, 1)
    start_date = datetime.date(2022, 2, 1)
    end_date = datetime.date(2022, 2, 28)
    delta = datetime.timedelta(days=1)


    while start_date <= end_date:
        entertainment_forecast_data = Entertainment_Forecast(date=start_date, inventory_available=140000, inventory_used=entertainment_inventory_used(start_date, fixed_start_date))
        kids_forecast_data = Kids_Forecast(date=start_date, inventory_available=50000, inventory_used=kids_inventory_used(start_date, fixed_start_date))

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

    create_workbook()


def entertainment_inventory_used(start_date, fixed_start_date):
    """

    """
    bookings = session.query(Bookings).all()
    total = 0

    for booking in bookings:
        if booking.content_group == '3|Ex Kids Content' and booking.start_date <= start_date and booking.start_date >= fixed_start_date:
            total += booking.daily_impressions
            print(f'{booking.campaign_name} {booking.content_group}')
    return total           


def kids_inventory_used(start_date, fixed_start_date):
    """

    """
    bookings = session.query(Bookings).all()
    total = 0

    for booking in bookings:
        if booking.content_group == '3|Kids Content' and booking.start_date <= start_date and booking.start_date >= fixed_start_date:
            total += booking.daily_impressions
            print(f'{booking.campaign_name} {booking.content_group}')
    return total  


def create_workbook():
    """
    
    """
    entertainment_data = session.query(Entertainment_Forecast).all()
    kids_data = session.query(Kids_Forecast).all()


    workbook = xlsxwriter.Workbook('excel/Forecast.xlsx')
    # worksheet1 = workbook.add_worksheet('Entertainment Forecast')
    worksheet2 = workbook.add_worksheet('Entertainment Forecast')
    worksheet3 = workbook.add_worksheet('Kids Forecast')

    #Shared Formattting
    date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
    merge_format = workbook.add_format({
        'bold': True,
        'align': "center",
        'valign': "center"
    })
    title_format = workbook.add_format({
        'bold': True,
        'align': "center",
        'valign': "center"
    })

    #Entertainment Forecast Sheet - Worksheet 2 - Formatting

    #Entertainment Forecast Sheet - Worksheet 2
    worksheet2.merge_range('B2:E2', 'Entertainment Inventory Forecast', merge_format)
    worksheet2.write('B3', 'Date', title_format)
    worksheet2.write('C3', 'Inventory Available', title_format)
    worksheet2.write('D3', 'Inventory Used', title_format)
    worksheet2.write('E3', 'Inventory Remaining', title_format)

    rowIndex = 4

    for data in entertainment_data:
        worksheet2.write('B' + str(rowIndex), data.date, date_format)
        worksheet2.write('C' + str(rowIndex), data.inventory_available)
        worksheet2.write('D' + str(rowIndex), data.inventory_used)
        worksheet2.write('E' + str(rowIndex), data.inventory_remaining)

        rowIndex += 1
    
    rowIndex = 4
    
    #Entertainment Forecast Sheet - Worksheet 3 - Formatting

    #Kids Forecast Sheet - Worksheet 3
    worksheet3.merge_range('B2:E2', 'Entertainment Inventory Forecast', merge_format)
    worksheet3.write('B3', 'Date', title_format)
    worksheet3.write('C3', 'Inventory Available', title_format)
    worksheet3.write('D3', 'Inventory Used', title_format)
    worksheet3.write('E3', 'Inventory Remaining', title_format)

    for data in kids_data:
        worksheet3.write('B' + str(rowIndex), data.date, date_format)
        worksheet3.write('C' + str(rowIndex), data.inventory_available)
        worksheet3.write('D' + str(rowIndex), data.inventory_used)
        worksheet3.write('E' + str(rowIndex), data.inventory_remaining)

        rowIndex += 1

    workbook.close()



def app():
    add_campaign_bookings()
    forecast()
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'f':
            print('FORECAST')
            forecast()
        elif choice == 'd':
            print('EXPORT')
        elif choice == 'e':
            print('EXIT')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()