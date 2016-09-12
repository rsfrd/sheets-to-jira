""" Utility to copy data from Google Sheets to JIRA """

import re
import gspread
import credentials_jira
import credentials_google
from jira import JIRA
from itertools import izip
from slugify import slugify


def sheet_to_jira():
    """ Using configuration from the environment, create jiras for data from
        a Google Spreadsheet """

    jira = credentials_jira.get_jira_client()
    worksheet = credentials_google.get_worksheet('GOOGLE_SHEET_CLOSING')

    # If the goal is to find the highest numbered row with content
    # this might do it ; pull all the values out of the column and count them.
    # new_closing = len(worksheet.col_values(1)) - 1

    def row_start(r):
        while worksheet.cell(r, 1).value != "":
            r += 1
        else:
            return r - 1
    new_closing = row_start(1)

    # gather questions and answers in lists
    survey_questions = worksheet.row_values(1)
    survey_answers = worksheet.row_values(new_closing)

    client_re = re.compile(r'Client')
    client = worksheet.find(client_re)
    client_slug = slugify(worksheet.cell(new_closing, client.col).value)

    summary = worksheet.cell(new_closing, client.col).value + " Deploy"
    description = ""

    # combine questions and answers, build string
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
        'components': [{'name': 'Deploy'},],
        'issuetype': {'name': 'Task'},
        'labels': [client_slug],
    }
    new_issue = jira.create_issue(fields=issue_dict)
    print "New Jira Created: {}".format(new_issue.key)

if __name__ == '__main__':
    sheet_to_jira()
