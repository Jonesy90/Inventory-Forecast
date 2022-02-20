# Inventory-Forecast

## Description
Takes in a CSV file, containing all the bookings for the current month. Calculates the daily average of impressions needed per day and how much is remaining per day. This allows us to see which days within the month are overbooked and inventory available.

Breaks off into two tables (Entertainment Forecast and Kids Forecast). The tables contain -
1. Inventory Available
2. Inventory Used
3. Inventory Remaining

Once, the tables are populated, it would then export them to a CSV and formatted Excel file.

# Tables
1. Bookings Table: 
   - Table Description. Report taken from the ad-serving platform. Shows all the bookings currently live, pending, cancelled or completed.
   - Campaign External ID
   - Campaign Name
   - Start Date
   - End Date
   - Content Group
   - Booked Impressions
   - Delivered Impressions
   - Daily Impressions

2. Entertainment Forecast Table:
   - Table Description: Take the 'Daily Impressions' for all bookings that have a 'Content Group' == 'Ex Kids'. This will populate the 'Inventory Used'. 'Inventory Remaining' will show the remaining inventory available for that day.
   - Date
   - Inventory Available
   - Inventory Used
   - Inventory Remaining


3. Kids Forecast Table:
   - Table Description: Take the 'Daily Impressions' for all bookings that have a 'Content Group' == 'Kids'. This will populate the 'Inventory Used'. 'Inventory Remaining' will show the remaining inventory available for that day.
   - Date
   - Inventory Available
   - Inventory Used
   - Inventory Remaining

## Development Setup & Running Application
1. Setup a virtual enviroment with `python3 -m venv env`
2. Activate the virtual enviroment with `source ./env/bin/activate`
3. Install all the libraries within requirements.txt `pip install -r requirements.txt`
4. Run the application - `python3 app.py {PATH TO FILE}`
