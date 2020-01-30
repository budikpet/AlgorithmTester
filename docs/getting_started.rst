Getting started
==================

Installation
--------------

.. code-block:: bash

    $ pip install -i https://test.pypi.org/simple/ algorithm-tester

All required dependencies are also installed. AlgorithmTester requires these packages to run:

- Click_
- slackclient_

.. _Click: https://click.palletsprojects.com/en/7.x/
.. _slackclient: https://github.com/slackapi/python-slackclient

How to use
------------

Check how to use the AlgorithmTester using:

.. code-block:: bash

    $ python -m run_tester --help

    ############ OR ################

    $ run_tester --help

That shows standard Click CLI help and also documentation of all 
available Algorithms, Parsers, Communicators and ConcurrencyRunners.

See :ref:`usingPlugins` to learn how to add new plugins.