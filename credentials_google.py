import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_worksheet(sheet_name):
    """ Get google the google worksheet, configured by environment """

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'google_creds_mt.json',
        scope)

    # auth, open sheet
    googlecred = gspread.authorize(credentials)
    sheet = googlecred.open_by_key(os.environ.get(sheet_name))
    return sheet.sheet1

if __name__ == '__main__':
    get_worksheet()
