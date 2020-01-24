from slack import WebClient
from algorithm_tester_common.tester_dataclasses import Communicator
from algorithm_tester_common.tester_dataclasses import AlgTesterContext

#slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

class SlackCommunicator(Communicator):

    def get_name(self):
        return "Slack"

    def notify_instance_computed(self, context: AlgTesterContext, output_file_name: str):
        """
        The Slack communicator is notified when an instance is computed.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            output_file_name {str} -- Last name of a output file that the instance belongs to.
        """
        print(f'Output file: {context.output_dir}/{output_file_name}')
        print(f'Instances remaining: {context.num_of_instances_done}/{context.num_of_instances}')