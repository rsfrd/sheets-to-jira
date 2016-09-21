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
    closing_headings = worksheet.row_values(1)
    closing_answers = worksheet.row_values(new_closing)

    client_re = re.compile(r'Client')
    client = worksheet.find(client_re)
    client_name = worksheet.cell(new_closing, client.col).value
    client_slug = slugify(client_name)

    summary = client_name + " Deploy"
    description = ""
    closing_pieces = []

    # combine questions and answers, build string
    # for question, answer in izip(survey_questions, survey_answers):
    #     if question == "" and answer == "":
    #         continue

    #     description += question + '\n'
    #     if answer == "":
    #         description += '- No answer given' + '\n\n'
    #     else:
    #         description += '- ' + answer + '\n\n'

    # create closing string
    closing_combined = zip(closing_headings, closing_answers)
      
    def zip_to_string(survey_snippet):
        snippet = ""
        for question, answer in survey_snippet:
            if question == "" and answer == "":
                continue
            
            snippet += question + '\n'
            if answer == "":
                snippet += '- No answer given' + '\n\n'
            else:
                snippet += '- ' + answer + '\n\n'
        return snippet
    
    closing_time = closing_combined[0:1]

    closing_string = closing_combined[1:7] + closing_combined[27:30] + closing_combined[7:27]
    closing_string = zip_to_string(closing_string)
 
    for x, y in closing_time:
        closing_pieces.append('h6.' + x + ': ' + y + ' PT \n\n')
    closing_pieces.append(closing_string)
  
    description = ''.join(closing_pieces)
  
    # determine salesperson
    salesperson_re = re.compile(r'Username')
    sales = worksheet.find(salesperson_re)
    salesperson = worksheet.cell(new_closing, sales.col).value

    if salesperson == 'sclaydon@mediatemple.net':
        salesperson = 'Simon'
    if salesperson == 'jmay@mediatemple.net':
        salesperson = 'Justin'
    if salesperson == 'erein@mediatemple.net':
        salesperson = 'Eric'
    if salesperson == 'cdowling@mediatemple.net':
        salesperson = 'Colin'

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
    slack_message.append('\n' + 'Everybody buy ' + salesperson + ' a :beer: !')
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
