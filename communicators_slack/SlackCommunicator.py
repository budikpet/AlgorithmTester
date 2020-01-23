from slack import WebClient
from algorithm_tester_common.tester_dataclasses import Communicator

#slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

class SlackCommunicator(Communicator):

    def get_name(self):
        return "Slack"