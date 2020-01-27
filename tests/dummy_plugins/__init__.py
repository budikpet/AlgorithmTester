import os
from tests.dummy_plugins.dummy_plugins import DummyAlgorithm, DummyParser, DummyFailingAlgorithm

_slack_config: str = "tests/dummy_plugins/fixtures/slack_communicator.cfg"
if os.path.isfile(_slack_config):
    os.environ["slack_config"] = _slack_config

__plugins__  = [DummyAlgorithm, DummyParser, DummyFailingAlgorithm]
__all__ = [plugin.__name__ for plugin in __plugins__]