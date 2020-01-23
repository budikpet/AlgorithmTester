from communicators_slack.SlackCommunicator import SlackCommunicator

__plugins__  = [SlackCommunicator]
__all__ = [plugin.__name__ for plugin in __plugins__]