AlgorithmTester
==================

.. image:: https://travis-ci.com/budikpet/AlgorithmTester.svg?branch=master
    :target: https://travis-ci.com/budikpet/AlgorithmTester

AlgorithmTester is a framework which is used to test performance and behaviour of provided algorithms. 
The framework itself is a Click_ CLI application. 
It receives input files with instances, hands them to provided algorithms and stores results in output files.

AlgorithmTester uses plugin architecture to make it possible to add any algorithm for any type of problem and use any
format of input and output files.

AlgorithmTester provides other useful features such as asynchronous computation or 
ability to monitor a state of computation using communicators.

.. _Click: https://click.palletsprojects.com/en/7.x/

Main utilization
-------------------

- The script reads data from input files with instances of the problem and parses them
- These instances are passes to required algorithms
- These algorithms solve the instances and return results
- These results are then one by one saved to output files

It must be possible to add new algorithms and parsers easily via plugins.

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

The resulting output could look like this:

.. code-block:: bash

    Usage: run_tester [OPTIONS] [EXTRA_OPTIONS]...

    ALGORITHMS:

    AlgName1:
        Long info about AlgName1 algorithm.

    AlgName2:
        ...

    PARSERS:

    ParserName1:
        ...

    ParserName2:
        ...

    COMMUNICATORS:

    Slack:
        A communicator that enables communication using Slack channel.

    RUNNERS:

    base:
        Processes files and their instances sequentially. No concurrency is used.

    files:
        Processes multiple files concurrently.

        Technically reads first instances of all files and stores them for
        multiprocessing.      Then reads second instances of all files and
        stores them for multiprocessing.      This repeats until no new
        instances are left in any input file.

    instances:
        Processes multiple instances of 1 file concurrently.

    SHORT_INFO:

        Available algorithms:    AlgName1, AlgName2, ...

        Available parsers:    ParserName1, ParserName2, ...

        Available communicators:    Slack, Communicator1, ...

        Available runners:    base, files, instances

    Options:
    -s, --algorithms TEXT           CSV string of names of available algorithms.
                                    [default:
                                    DummyAlgorithm,DummyFailingAlgorithm;
                                    required]
    -r, --concurrency-runner TEXT   Concurrency mode the programme should use to
                                    compute results.  [default: BASE; required]
    --check-time BOOLEAN            Should the result also check elapsed time.
    --time-retries INTEGER          How many times should we retry if elapsed
                                    time is checked.
    -p, --parser TEXT               Name of the parser that is used to parse
                                    input files.  [required]
    -c, --communicators TEXT        CSV string of names of available
                                    communication interfaces.
    -n, --max-num INTEGER           If set then the run_tester uses only (0,
                                    max-num] of input files.
    -f, --is-forced                 If set then all previous output is removed
                                    before starting. If not set then the
                                    programme will start from the place it
                                    ended.
    -t, --min-communicator-delay FLOAT
                                    How many seconds there at least must be
                                    between two communicator messages.
    --input-dir TEXT                Path to directory with input files.
                                    [required]
    --output-dir TEXT               Path to directory where output files are to
                                    be stored.  [required]
    --help                          Show this message and exit.

*AlgName1*, *AlgName2*, *ParserName1*, ... are names provided by plugins. 
These names are used to identify unique Algorithms, Parsers etc.