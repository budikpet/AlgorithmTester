import os
from slack import WebClient
from typing import Dict
from datetime import datetime
from algorithm_tester_common.tester_dataclasses import Communicator
from algorithm_tester_common.tester_dataclasses import AlgTesterContext
from algorithm_tester.helpers import zip_dir

class SlackCommunicator(Communicator):
    """
    A communicator that enables communication using Slack channel.
    
    """
    
    def __init__(self):
        self.slack_web_client = WebClient(token=os.environ['slack_access_token'])
        self.main_msg_ts: str = None
        self.file_id: str = None

    def get_name(self):
        return "Slack"

    def _create_zip_file(self, output_dir: str) -> str:
        """
        Creates a ZIP file of the output directory.
        
        Arguments:
            output_dir {str} -- Directory to create ZIP file of.
        
        Returns:
            str -- Path to the created ZIP file.
        """
        zip_name: str = output_dir.split("/")[-1]
        zip_dir_path: str = zip_dir(zip_name, output_dir)

        # Move to output_dir parent
        new_path: str = f'{os.path.dirname(output_dir)}/{zip_name}.zip'
        os.replace(zip_dir_path, new_path)
        return new_path

    def notify_instance_computed(self, context: AlgTesterContext, last_solution: Dict[str, object], num_of_instances_done: int, num_of_instances_failed: int):
        """
        The Slack communicator is notified when an instance is computed.
        
        Arguments:
            context {AlgTesterContext} -- Used context.
            last_solution {Dict[str, object]} -- Last computed instance data.
            num_of_instances_done {int} -- Number of instances that were computed to this time.
        """
        output_filename: str = last_solution.get("output_filename")
        print(f'Output file: {context.output_dir}/{output_filename}')
        print(f'Instances [done/failed]: [{num_of_instances_done}/{num_of_instances_failed}]/{context.num_of_instances}')

        # Create a zip file of the results directory in the same parent directory
        zip_dir_path: str = self._create_zip_file(context.output_dir)

        # Prepare messages
        start_time = datetime.fromtimestamp(context.start_time)
        timestr: str = f'Computation started: {start_time.strftime("%d.%m.%Y %H:%M:%S")}'
        main_message = {
            "username": os.environ['slack_bot_username'],
            "channel": os.environ['slack_channel_id'],
            "text": f'{timestr}\nProgress: [{num_of_instances_done}/{num_of_instances_failed}]/{context.num_of_instances} instances [done/failed].'
        }

        file_message = {
            "channels": os.environ['slack_channel_id'], 
            "file": zip_dir_path,
            "filename": zip_dir_path.split("/")[-1],
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
                "as_user": os.environ['slack_bot_username'],
                "ts": self.main_msg_ts,
            })
            response = self.slack_web_client.chat_update(**main_message)

            # Reupload zip file with results
            response = self.slack_web_client.files_upload(**file_message)
            self.file_id = response["file"]["id"]
        
        print