.. AlgorithmTester documentation master file, created by
   sphinx-quickstart on Sat Feb  8 21:04:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AlgorithmTester's documentation!
===========================================
.. image:: https://travis-ci.com/budikpet/AlgorithmTester.svg?branch=master
    :target: https://travis-ci.com/budikpet/AlgorithmTester

Introduction
-------------
AlgorithmTester is a framework which is used to test performance and behaviour of provided algorithms. 
The framework itself is a Click_ CLI application. 
It receives input files with instances, hands them to provided algorithms and stores results in output files.

AlgorithmTester uses plugin architecture to make it possible to add any algorithm for any type of problem and use any
format of input and output files.

AlgorithmTester provides other useful features such as asynchronous computation or 
ability to monitor a state of computation using communicators.

.. _Click: https://click.palletsprojects.com/en/7.x/

Contents of AlgorithmTester's documentation:
----------------------------------------------

.. toctree::
    :maxdepth: 2
    
    getting_started
    plugins
    slack

.. toctree::
	:maxdepth: 1

	modules/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
