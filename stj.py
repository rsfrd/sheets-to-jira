# auth with jira
# auth with google sheets
#
# in sheets
# read row one
# copy string in each cell
# read last row
# copy string in each cell
# match the corresponding columns
# pair them up
#
# format for jira
# export to jira

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-credentials-mr.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('sheets to jira test document').sheet1

