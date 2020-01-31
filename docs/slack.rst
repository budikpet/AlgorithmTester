.. _slack:

Slack communicator
=====================
AlgorithmTester has a built-in communicator which uses slackclient_ library
to monitor progress of running computation using a remote Slack channel. 

On top of monitoring computation progress it also ZIPs and sends results 
directory to the Slack channel. 

Configuration
----------------
Additional configuration is required to use the Slack communicator.
A user must create a Slack channel, prepare a Slack bot for that channel
and provide necessery information in a configuration file.
Each step will now be described here.

Our guide for preparing Slack channel and bot is going to 
follow the official tutorial_ of python slackclient_.

Prepare Slack channel and bot
_______________________________
1. Sign-in_ to an existing Slack workspace or create a `new Slack workspace`_.
2. To create a new Slack bot, go to `api.slack.com`_.
    i. Type in the Slack bot's name and select the workspace you created.
    
    .. image:: _static/create_slack_bot.png

3. Grant permissions to the Slack bot
    i. Navigate to **OAuth & Permissions -> Bot Token Scopes**.
    ii. Enable these scopes:

        - chat:write
        - files:read
        - files:write
4. Install the Slack bot to the workspace

    

5. Create a new Slack channel for AlgorithmTester
6. If bot is not automatically added to the new channel, add it.

    .. image:: _static/add_bot_to_channel.png 

The Slack channel and bot is now prepared to be used.

Prepare configuration file
_______________________________
AlgorithmTester needs a Slack configuration file to connect to the created Slack channel.
Provide file path to this configuration file to AlgorithmTester using *slack_config*
environmental variable.

The configuration file looks like this:

.. literalinclude:: _static/cfgs/slack_communicator_SAMPLE.cfg
	:language: ini

The **access_token** is received here:

    .. image:: _static/bot_access_token.png

The **channel_id** has a similar form to *CTEAX860M*. 
It is received here:

    .. image:: _static/get_channel_id.png

.. _`api.slack.com`: https://api.slack.com/apps?new_granular_bot_app=1
.. _`new Slack workspace`: https://slack.com/get-started#/create
.. _Sign-in: https://slack.com/intl/en-cz/help/articles/212681477#browser-1
.. _tutorial: https://github.com/slackapi/python-slackclient/tree/master/tutorial
.. _slackclient: https://github.com/slackapi/python-slackclient
