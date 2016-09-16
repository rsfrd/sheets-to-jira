""" Utility to copy data from Google Sheets to JIRA """

import re
import os
import gspread
import credentials_jira
import credentials_google
import credentials_slack
from jira import JIRA
from itertools import izip
from slugify import slugify
import requests

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
    client_name = worksheet.cell(new_closing, client.col).value

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

    # send to slack
    # slack_webhook = credentials_slack.get_slack_webhook()  
    slack_webhook = os.environ.get('SLACK_WEBHOOK')

    slack_message = []
    slack_message.append('New closing in JIRA at ' + '<https://tools.mtsvc.net/jira/browse/')
    slack_message.append(new_issue.key + '|' + new_issue.key + '> from ' + client_name)
    slack_message.append('\n' + 'CREAM!')
    slack_message = ''.join(slack_message)

    payload = {"channel": "#mt-cloud-services",
        "username": "Sales Closing",
        "text": slack_message,
        "icon_emoji": ":dollar:"}
    
    requests.post(slack_webhook, json=payload)

    # show result on command line
    print "New Jira Created: {}".format(new_issue.key)

if __name__ == '__main__':
    sheet_to_jira()
