# complete: 
# - auth with google
# - read questions in headers, find most recent closing
# - match closing answers to headers, format for jira, export to file
# to do: 
# - auth with jira, export to jira

from itertools import izip 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# write to a file for now; eventually send directly into jira
jira = open('closing-jira.txt', 'w+')

# combine questions and answers, write to file
for i in izip(survey_questions, survey_answers):
    jira.write(i[0] + '\n')
    jira.write('- ' + i[1] + '\n\n')

