import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.shortcuts import render
from .models import TallyTransaction
from openpyxl import Workbook
import requests

def process_xml(xml_content):
    root = ET.fromstring(xml_content)
    transactions = []

    for entry in root.findall('.//VOUCHER'):
        voucher_type = entry.find('VOUCHERTYPENAME').text
        if voucher_type == 'Receipt':
            date = entry.find('.//DATE').text
            party = entry.find('.//PARTYLEDGERNAME').text
            amount = entry.find('.//AMOUNT').text
            transactions.append({'date': date, 'party': party, 'amount': amount, 'voucher_type': voucher_type})

    return transactions

def generate_excel(transactions):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Date', 'Party', 'Amount', 'Voucher Type'])

    for transaction in transactions:
        sheet.append([transaction['date'], transaction['party'], transaction['amount'], transaction['voucher_type']])

    return workbook

def process_tally_xml(request):
    # Fetch XML content from the provided URL
    xml_url = 'https://drive.google.com/file/d/1fbwTF0bWoseNJGgpCjl6fJdpaIb260nQ/view?usp=sharing'
    response = requests.get(xml_url)
    transactions = process_xml(response.content)

    # Save transactions to the database (optional)
    TallyTransaction.objects.all().delete()  # Clear existing data
    for transaction in transactions:
        TallyTransaction.objects.create(**transaction)

    # Generate Excel file
    workbook = generate_excel(transactions)
    excel_filename = 'response_spreadsheet.xlsx'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={excel_filename}'
    workbook.save(response)

    return response
