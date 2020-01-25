import os
from slack import WebClient
from typing import Dict
from algorithm_tester_common.tester_dataclasses import Communicator
from algorithm_tester_common.tester_dataclasses import AlgTesterContext
from algorithm_tester.helpers import zip_dir

class SlackCommunicator(Communicator):
    
    def __init__(self):
        self.slack_web_client = WebClient(token=os.environ['slack_access_token'])
        self.main_msg_ts: str = None
        self.file_id: str = None

    def get_name(self):
        return "Slack"

    def notify_instance_computed(self, context: AlgTesterContext, last_solution: Dict[str, object], num_of_instances_done: int):
        """
        The Slack communicator is notified when an instance is computed.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            last_solution {Dict[str, object]} -- Last computed instance data.
            num_of_instances_done {int} -- Number of instances that were computed to this time.
        """
        output_filename: str = last_solution.get("output_file_name")
        print(f'Output file: {context.output_dir}/{output_filename}')
        print(f'Instances remaining: {num_of_instances_done}/{context.num_of_instances}')

        # Create a zip file of the results directory in the same parent directory
        archive_name: str = context.output_dir.split("/")[-1]
        original_dir = os.getcwd()
        os.chdir(os.path.dirname(context.output_dir))
        zip_dir_path: str = zip_dir(archive_name, context.output_dir)
        os.chdir(os.path.dirname(original_dir))

        # Prepare messages
        main_message = {
            "username": "AlgorithmTester_Bot",
            "channel": os.environ['slack_channel_id'],
            "text": f"Test message. Progress: {num_of_instances_done}/{context.num_of_instances} instances done."
        }

        file_message = {
            "channels": os.environ['slack_channel_id'], 
            "file": zip_dir_path,
            "filename": f"{archive_name}.zip",
            "filetype": "zip"
        }

        if self.main_msg_ts is None:
            # Create info message
            response = self.slack_web_client.chat_postMessage(**main_message)
            self.main_msg_ts = response["ts"]

            # Upload zip file with results
            response = self.slack_web_client.files_upload(**file_message)
            self.file_id = response["file"]["id"]
        else:
            # Update message and uploaded file
            response = self.slack_web_client.files_delete(file=self.file_id)
            
            main_message.update({
                "as_user": "AlgorithmTester_Bot",
                "ts": self.main_msg_ts,
            })
            response = self.slack_web_client.chat_update(**main_message)

            # Reupload zip file with results
            response = self.slack_web_client.files_upload(**file_message)
            self.file_id = response["file"]["id"]
        
        print