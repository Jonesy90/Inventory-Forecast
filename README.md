# Inventory-Forecast

## Description
Takes in a CSV file, containing all the bookings for the current month. Calculates the daily average of impressions needed per day to ensure the booking delivers in full.
Breaks off into two tables (Entertainment Forecast and Kids Forecast). The tables contain -
1. Inventory Available
2. Inventory Used
3. Inventory Remaining

Once, the tables are populated, it would then export them to a CSV and formatted Excel file.

## Development Setup & Running Application
1. Setup a virtual enviroment with `python3 -m venv env`
2. Activate the virtual enviroment with `source ./env/bin/activate`
3. Install all the libraries within requirements.txt `pip install -r requirements.txt`
4. Run the application - `python3 app.py {PATH TO FILE}`
