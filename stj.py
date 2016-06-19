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

sh = gc.open('sheets to jira test document')

worksheet = sh.sheet1

survey_questions = worksheet.row_values(1)
survey_answers = worksheet.row_values(4)

print survey_questions
print survey_answers

q_and_a = zip(survey_questions, survey_answers)

print q_and_a

print "%s" % q_and_a[0][0]
print "- %s" % q_and_a[0][1]
print ""
print "%s" % q_and_a[1][0]
print "- %s" % q_and_a[1][1]
