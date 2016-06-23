# complete: 
# - auth with google
# - read questions in headers, find most recent closing
# - match closing answers to headers, format for jira, export to file
# to do: 
# - auth with jira, export to jira

import os
from itertools import izip 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jira import JIRA

options = {
    'server': os.environ.get('SERVER')
}
jira = JIRA(options)

key_cert_data = None
with open('jira.pem', 'r') as key_cert_file:
    key_cert_data = key_cert_file.read()

oauth_dict = {
    'access_token': os.environ.get('ACCESS_TOKEN'),
    'access_token_secret': os.environ.get('ACCESS_TOKEN_SECRET'),
    'consumer_key': os.environ.get('CONSUMER_KEY'),
    'key_cert': key_cert_data
}
authed_jira = JIRA(options, oauth=oauth_dict)

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-credentials-mr.json', scope)

# auth, open sheet
gc = gspread.authorize(credentials)
sh = gc.open('sheets to jira test document')
worksheet = sh.sheet1

# find most recently added row
def row_start(r):
    while worksheet.cell(r, 1).value != "":
        r += 1            
    else:
        return r - 1 

new_closing = row_start(1)

# gather questions and answers in lists
survey_questions = filter(None, worksheet.row_values(1))
survey_answers = filter(None, worksheet.row_values(new_closing)) 

descr = ""

# combine questions and answers, write to file
for i in izip(survey_questions, survey_answers):
    descr += i[0] + '\n'
    descr += '- ' + i[1] + '\n\n'

issue_dict = {
    'project': {'key': 'PYT'},
    'summary': 'Confirmation of Closed',
    'description': descr,
    'issuetype': {'name': 'Task'},
}
new_issue = authed_jira.create_issue(fields=issue_dict)

