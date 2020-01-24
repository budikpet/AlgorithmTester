import os
from tests.dummy_plugins.dummy_plugins import DummyAlgorithm, DummyParser

os.environ["slack_config"] = "tests/dummy_plugins/fixtures/slack_communicator.cfg"

__plugins__  = [DummyAlgorithm, DummyParser]
__all__ = [plugin.__name__ for plugin in __plugins__]