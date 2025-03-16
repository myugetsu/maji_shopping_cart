import requests
from requests.auth import HTTPBasicAuth
from flask import current_app
import base64
from datetime import datetime

def generate_access_token():
    consumer_key = current_app.config['MPESA_CONSUMER_KEY']
    consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']

def initiate_stk_push(phone_number, amount):
    access_token = generate_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{current_app.config['MPESA_SHORTCODE']}{current_app.config['MPESA_PASSKEY']}{timestamp}".encode()).decode('utf-8')

    payload = {
        'BusinessShortCode': current_app.config['MPESA_SHORTCODE'],
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': current_app.config['MPESA_SHORTCODE'],
        'PhoneNumber': phone_number,
        'CallBackURL': current_app.config['MPESA_CALLBACK_URL'],
        'AccountReference': 'ShoppingCart',
        'TransactionDesc': 'Payment for goods'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
