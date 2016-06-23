# complete: 
# - auth with google
# - read questions in headers, find most recent closing
# - match closing answers to headers, format for jira, export to file
# - auth with jira, export to jira
# - all of the things! now to clean up...

import os
import re
import gspread
from jira import JIRA
from itertools import izip 
from oauth2client.service_account import ServiceAccountCredentials

options = {
    'server': os.environ.get('SERVER')
}

key_cert_data = os.environ.get('JIRA_KEY') 

oauth_dict = {
    'access_token': os.environ.get('ACCESS_TOKEN'),
    'access_token_secret': os.environ.get('ACCESS_TOKEN_SECRET'),
    'consumer_key': os.environ.get('CONSUMER_KEY'),
    'key_cert': key_cert_data
}
jira = JIRA(options, oauth=oauth_dict)

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)

# auth, open sheet
gc = gspread.authorize(credentials)
sh = gc.open(os.environ.get('GOOGLE_SHEET'))
worksheet = sh.sheet1

# find most recently added row
def row_start(r):
    while worksheet.cell(r, 1).value != "":
        r += 1            
    else:
        return r - 1 

new_closing = row_start(1)

# gather questions and answers in lists
survey_questions = worksheet.row_values(1)
survey_answers = worksheet.row_values(new_closing)

# def client_name():
#     worksheet.find(re.compile(r'Client'))
#     return 
# 
# client = client_name()

client_re = re.compile(r'Client')
client = worksheet.find(client_re)

t = worksheet.cell(new_closing, client.col).value + " Deploy"
d = ""

# combine questions and answers, build string 
for i in izip(survey_questions, survey_answers):
    if i[0] == "" and i[1] == "":
        del i
    elif i[1] == "":
        d += i[0] + '\n'
        d += '- No answer given' + '\n\n'
    else:
        d += i[0] + '\n'
        d += '- ' + i[1] + '\n\n'

# send to jira
issue_dict = {
    'project': {'key': 'PYT'},
    'summary': t,
    'description': d,
    'issuetype': {'name': 'Task'},
}
new_issue = jira.create_issue(fields=issue_dict)

