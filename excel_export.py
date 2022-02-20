from models import *

import xlsxwriter

def create_workbook():
    """
    An Excel document is created and downloaded from Entertainment and Kids DB.
    """
    entertainment_data = session.query(Entertainment_Forecast).all()
    kids_data = session.query(Kids_Forecast).all()


    workbook = xlsxwriter.Workbook('excel/Forecast.xlsx')
    # worksheet1 = workbook.add_worksheet('Entertainment Forecast')
    worksheet2 = workbook.add_worksheet('Entertainment Forecast')

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
    
    #Kids Forecast Table
    worksheet2.merge_range('G2:J2', 'Kids Inventory Forecast', merge_format)
    worksheet2.write('H3', 'Date', title_format)
    worksheet2.write('H3', 'Inventory Available', title_format)
    worksheet2.write('I3', 'Inventory Used', title_format)
    worksheet2.write('J3', 'Inventory Remaining', title_format)

    for data in kids_data:
        worksheet2.write('G' + str(rowIndex), data.date, date_format)
        worksheet2.write('H' + str(rowIndex), data.inventory_available)
        worksheet2.write('I' + str(rowIndex), data.inventory_used)
        worksheet2.write('J' + str(rowIndex), data.inventory_remaining)

        rowIndex += 1



    workbook.close()