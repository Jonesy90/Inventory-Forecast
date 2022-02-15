#External Imports
import argparse
import pathlib
import csv

parser = argparse.ArgumentParser(description='Uploads the CSV, process it.')
parser.add_argument('source_file', metavar='source_file', type=pathlib.Path, help='Upload the CSV file.')
args = parser.parse_args()

booking_uploaded_csv = args.source_file

def menu():
    while True:
        print('''
            \n*****MAIN MENU*****:
            \rb : ADD BOOKINGS
            \rf : FORECAST
            ''')
        users_choice = input('Please select an option: ').lower()
        if users_choice in ['b, f']:
            return users_choice


def add_campaign_bookings():
    """
    Read a CSV file to and add to the Bookings DB.    

    """
    
    with open(booking_uploaded_csv, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            campaign_external_id = row['Campaign External ID']
            campaign_name = row['Campaign Name']
            start_date = row['Start Date']
            end_date = row['End Date']
            booked_impressions = row['Booked Impressions']
            delivered_impressions = row['Delivered Impressions']



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'b':
            add_campaign_bookings()


















if __name__ == '__main__':
    app()