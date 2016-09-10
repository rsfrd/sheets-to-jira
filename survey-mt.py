""" Utility to copy data from Google Sheets to JIRA """

import os
import re
import gspread
from jira import JIRA
from itertools import izip
from oauth2client.service_account import ServiceAccountCredentials


def get_jira_client():
    """ Return a connected JIRA API client, configured by environment """
    options = {
        'server': os.environ.get('SERVER')
    }
    key_cert_data = os.environ.get('JIRA_KEY')
    # key_cert_data = open('mt-jira.pem', 'r')

    oauth_dict = {
        'access_token': os.environ.get('ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('ACCESS_TOKEN_SECRET'),
        'consumer_key': os.environ.get('CONSUMER_KEY'),
        'key_cert': key_cert_data
    }
    return JIRA(options, oauth=oauth_dict)


def get_worksheet():
    """ Get google the google worksheet, configured by environment """

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'google_creds_mt.json',
        scope)

    # auth, open sheet
    googlecred = gspread.authorize(credentials)
    sheet = googlecred.open_by_key(os.environ.get('GOOGLE_SHEET_SURVEY'))
    return sheet.sheet1


def sheet_to_jira():
    """ Using configuration from the environment, create jiras for data from
        a Google Spreadsheet """

    jira = get_jira_client()
    worksheet = get_worksheet()

    # If the goal is to find the highest numbered row with content
    # this might do it ; pull all the values out of the column and count them.
    # new_closing = len(worksheet.col_values(1)) - 1

    def row_start(r):
        while worksheet.cell(r, 1).value != "":
            r += 1
        else:
            return r - 1
    new_survey = row_start(1)

    # gather questions and answers in lists
    survey_questions = worksheet.row_values(1)
    survey_answers = worksheet.row_values(new_survey)
    
    client_re = re.compile(r'Company Name')
    client = worksheet.find(client_re)

    summary = worksheet.cell(new_survey, client.col).value + " Proposal"
    description = ""

    # combine questions and answers, build string
    # description = zip(survey_questions, survey_answers)
    # [v for i, v in enumerate(description) if v[0] == "Company Name"]
    # print v 
 
    for question, answer in izip(survey_questions, survey_answers):
      if question == "" and answer == "":
          continue

      description += question + '\n'
      if answer == "":
          description += '- No answer given' + '\n\n'
      else:
          description += '- ' + answer + '\n\n'

    # send to jira
    issue_dict = {
        'project': {'key': 'CM'},
        'summary': summary,
        'description': description,
        'components': [{'name': 'Proposal'},],
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    print "New Jira Created: {}".format(new_issue.key)

if __name__ == '__main__':
    sheet_to_jira()
