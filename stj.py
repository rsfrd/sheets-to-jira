# auth with jira
# auth with google sheets - done!
#
# in sheets
# read row one - done!
# copy string in each cell - done!
# read last row - done! 
# copy string in each cell - done!
# match the corresponding columns - done!
# pair them up - done!
#
# format for jira - done!
# export to jira

from itertools import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-credentials-mr.json', scope)

# closed_row = raw_input("Most recent closing row number > ")

gc = gspread.authorize(credentials)

sh = gc.open('sheets to jira test document')

worksheet = sh.sheet1

def row_start(vrow):
    while worksheet.cell(vrow, 1).value != "":
        vrow += 1            
    else:
        return vrow - 1 

new_closing = row_start(1)

survey_questions = filter(None, worksheet.row_values(1))
survey_answers = filter(None, worksheet.row_values(new_closing))

for i in izip(survey_questions, survey_answers):
    print i[0]
    print '- ' + i[1] + '\n'


# q_and_a = zip(survey_questions, survey_answers)
# 
# print q_and_a
# 
# q_and_a_len = len(q_and_a)
# for i in range (0, q_and_a_len):
#     print q_and_a[i]
 

# print "%s" % q_and_a[0][0]
# print "- %s" % q_and_a[0][1]
# print ""
# print "%s" % q_and_a[1][0]
# print "- %s" % q_and_a[1][1]
