import os

def get_slack_webhook():
    slack_webhook = os.environ.get('SLACK_WEBHOOK')

if __name__ == '__main__':
    get_slack_webhook()
