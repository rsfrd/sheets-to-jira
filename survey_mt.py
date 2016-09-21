""" Utility to copy data from Google Sheets to JIRA """

import re
import os
import gspread
import credentials_jira
import credentials_google
from jira import JIRA
# from itertools import izip
from slugify import slugify
import requests

def sheet_to_jira():
    """ Using configuration from the environment, create jiras for data from
        a Google Spreadsheet """

    jira = credentials_jira.get_jira_client()
    worksheet = credentials_google.get_worksheet('GOOGLE_SHEET_SURVEY')

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
    client_name = worksheet.cell(new_survey, client.col).value
    client_slug = slugify(client_name)

    summary = client_name + " Proposal"
    description = ""
    survey_pieces = []

    # create survey results string
    survey_combined = zip(survey_questions, survey_answers)

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

    survey_time = survey_combined[0:1]

    survey_client = survey_combined[30:31] + survey_combined [27:29]
    survey_client = zip_to_string(survey_client)

    survey_general = survey_combined[29:30] + survey_combined [1:7]
    survey_general = zip_to_string(survey_general)
    
    survey_technical = survey_combined[7:27]
    survey_technical = zip_to_string(survey_technical)

    for x, y in survey_time:
        survey_pieces.append('h6.' + x + ': ' + y + ' PT \n\n')
    survey_pieces.append('h3.Client' + '\n')
    survey_pieces.append(survey_client)
    survey_pieces.append('h3.Sales' + '\n' + '- ' + '\n\n')
    survey_pieces.append('h3.Survey' + '\n' + 'h4.GENERAL QUESTIONS' + '\n')
    survey_pieces.append(survey_general)
    survey_pieces.append('h4.TECHNICAL QUESTIONS' + '\n')
    survey_pieces.append(survey_technical)

    description = ''.join(survey_pieces)

    # send to jira
    issue_dict = {
        'project': {'key': 'CM'},
        'summary': summary,
        'description': description,
        'components': [{'name': 'Proposal'},],
        'issuetype': {'name': 'Task'},
        'labels': [client_slug],
    }
    
    new_issue = jira.create_issue(fields=issue_dict)

    # send to cloud slack
    slack_webhook = os.environ.get('SLACK_WEBHOOK')

    slack_message = []
    slack_message.append('New tech survey in JIRA at ' + '<https://tools.mtsvc.net/jira/browse/') 
    slack_message.append(new_issue.key + '|' + new_issue.key + '> from ' + client_name)
    slack_message = ''.join(slack_message)

    payload = {"channel": "#mt-cloud-services", 
        "username": "Sales Survey", 
        "text": slack_message, 
        "icon_emoji": ":postbox:"}

    requests.post(slack_webhook, json=payload)

    # send to sales slack
    slack_sales_message = []
    slack_sales_message.append('New tech survey in Cloud Services queue from ' + client_name)
    slack_sales_message.append('\n' + 'To whom should we send the proposal?')
    slack_sales_message = ''.join(slack_sales_message)

    sales_payload = {"channel": "#mt-sales-cloud",
        "username": "Sales Survey",
        "text": slack_sales_message,
        "icon_emoji": ":postbox:"}

    requests.post(slack_webhook, json=sales_payload)

    # show result on command line
    print "New Jira Created: {}".format(new_issue.key)

if __name__ == '__main__':
    sheet_to_jira()
