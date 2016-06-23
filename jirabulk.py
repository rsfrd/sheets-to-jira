from jira import JIRA

options = {
    'server': 'http://52.41.64.139:8080'
}
jira = JIRA(options)

key_cert_data = None  
with open('jira.pem', 'r') as key_cert_file:
    key_cert_data = key_cert_file.read()

oauth_dict = {
    'access_token': 'rawNkWV9JHOIA8xo3sx12uzrwPJDlUeV',
    'access_token_secret': 'AD7YCtxqxKDGriozdUJMHfOdZoGXP5Q5',
    'consumer_key': 'stj',
    'key_cert': key_cert_data 
}
authed_jira = JIRA(options, oauth=oauth_dict)

issue_dict = {
    'project': {'key': 'PYT'},
    'summary': 'New issue from jira-python',
    'description': 'Look into this one',
    'issuetype': {'name': 'Task'},
}
new_issue = authed_jira.create_issue(fields=issue_dict)
