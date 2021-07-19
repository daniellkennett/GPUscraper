import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
def send_email(msg, to = 'daniel.l.kennett@gmail.com'):

    emailMsg = msg
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = to
    mimeMessage['subject'] = 'Sup'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)
# from Google.quickstart import send_email
# from Google.Google  import Create_Service


import requests
import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import time

d = {'name': [],
     'price' : [],
     'button' : []}

info_class = 'sku-header'
price_class = 'priceView-hero-price priceView-customer-price'
button_class = 'btn btn-disabled btn-sm btn-block add-to-cart-button'

url = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507002&id=pcat17071&iht=n&ks=960&list=y&qp=chipsetmanufacture_facet%3DChipset%20Manufacturer~NVIDIA%5Evideomemorycapacitysv_facet%3DVideo%20Memory%20Capacity~10%20gigabytes%5Evideomemorycapacitysv_facet%3DVideo%20Memory%20Capacity~12%20gigabytes%5Evideomemorycapacitysv_facet%3DVideo%20Memory%20Capacity~24%20gigabytes%5Evideomemorycapacitysv_facet%3DVideo%20Memory%20Capacity~8%20gigabytes&sc=Global&st=categoryid%24abcat0507002&type=page&usc=All%20Categories'
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
def webscrap(url, headers):
    bb = requests.get(url, headers=headers)
    soup = BeautifulSoup(bb.content.decode(), 'html.parser')

    mydivs_name = soup.find_all("h4", {"class": info_class})
    mydivs_price = soup.find_all('div', {'class': price_class})
    mydivs_button = soup.find_all('button', {'class' : button_class})

    for i in range(len(mydivs_name)):
        name = mydivs_name[i].find('a').text
        price = mydivs_price[i].find('span').text
        button = mydivs_button[i].text
        d['name'].append(name)
        d['price'].append(price)
        d['button'].append(button)

    df = pd.DataFrame(d)
    # button = df.button
    # button[3] = 'Sold In'
    trigger = df.button.str.contains('Sold Out').all()
    if not trigger:
        send_email('CHECK BESTBUY NOW YOU MOTHERF****R')
        send_email('CHECK BESTBUY NOW YOU MOTHERF****R', 'dweikferris@gmail.com')

if __name__ == '__main__':
    while True:
        webscrap(url, headers)
