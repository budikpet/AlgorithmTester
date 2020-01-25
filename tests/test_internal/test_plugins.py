import os
from configparser import ConfigParser
from algorithm_tester.plugins import Plugins

# def test_check_internal_communicators_preconditions():
#     plugins: Plugins = Plugins()
#     assert len(plugins.get_communicators()) == 0

#     config_file_path: str = "tests/dummy_plugins/fixtures/slack_communicator_SAMPLE.cfg"
#     with open(config_file_path) as config_file:
#         config_parser: ConfigParser = ConfigParser()
#         config_parser.read_file(config_file)
#         access_token: str = config_parser["auth"]["access_token"]
#         channel_id: str = config_parser["channel"]["id"]

#     os.environ["slack_config"] = config_file_path
#     plugins = Plugins()
#     assert len(plugins.get_communicators()) == 1
#     assert os.environ.get("slack_access_token") is not None
#     assert os.environ.get("slack_channel_id") is not None 
#     assert os.environ["slack_access_token"] == access_token
#     assert os.environ["slack_channel_id"] == channel_id

#     print