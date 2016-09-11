import os
import pem
from jira import JIRA

def get_jira_client():
    """ Return a connected JIRA API client, configured by environment """
    options = {
        'server': os.environ.get('SERVER')
    }

    key_cert_data = pem.parse_file("mt-jira.pem")
    key_cert_data = str(key_cert_data[0])
    
    # key_cert_data = os.environ.get('JIRA_KEY')
    # key_cert_data = open('mt-jira.pem', 'r')

    oauth_dict = {
        'access_token': os.environ.get('ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('ACCESS_TOKEN_SECRET'),
        'consumer_key': os.environ.get('CONSUMER_KEY'),
        'key_cert': key_cert_data
    }
    return JIRA(options, oauth=oauth_dict)

if __name__ == '__main__':
    get_jira_client()
