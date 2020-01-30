.. _usingPlugins:

Using the Plugin architecture
===============================
AlgorithmTester is useful mainly because it's possible to add an algorithm to a problem it without many constraints.
Users aren't constrained by format of input or output files either as they can create a custom Parser for them.

Let's see how it's possible to add plugins for AlgorithmTester to use.

Project configuration
------------------------
Use setup.py entrypoints to specify packages where AlgorithmTester 
should look for specific plugins. Different types of plugins
can be located in a same package.

.. code-block:: python

    setup(
        ...,

        entry_points={
            'algorithm_tester.plugins': [
                'algorithms = package_algorithms',
                'parsers = package_others',
                'communicators = package_others'
            ]
        },

        ...,
    )

AlgorithmTester then checks these packages for package-wide *__init__.py* file.
More specifically it's trying to find a variable called **__plugins__** which contains
plugin classes the package provides.

An example of *__init__.py* file of package_others package:

.. code-block:: python

    import os
    from package_others.parsers import Parser1, Parser2
    from package_others.communicators import Comm1, Comm2

    __plugins__  = [Parser1, Parser2, Comm1, Comm2]
    __all__ = [plugin.__name__ for plugin in __plugins__]

Note that *__all__* variable isn't neccessary 
but it's possible to add it like this quite easily.

.. _algorithmsLabel:

Add Algorithms
----------------
New algorithms need to conform 
:class:`algorithm_tester_common.tester_dataclasses.Algorithm` class.

An example of how to add a new algorithm:

.. code-block:: python

    from algorithm_tester_common.tester_dataclasses import Algorithm

    class NewAlg(Algorithm):
        """
        DocString used in help.
        
        """

        def get_columns(self) -> List[str]:
            ...

        def get_name(self) -> str:
            return "AlgName"
        
        def perform_algorithm(self, context: AlgTesterContext, parsed_data: Dict[str, object]) -> Dict[str, object]:
            ...

These are neccessary methods for the new algorithm to work properly.

The :meth:`algorithm_tester_common.tester_dataclasses.Algorithm.get_name` method
is the identification of the algorithm. More information about using 
these identifiers in :ref:`howToUse` section.

The :meth:`algorithm_tester_common.tester_dataclasses.Algorithm.perform_algorithm` method
runs the actual algorithm using the provided instance data that is received
from a :class:`algorithm_tester_common.tester_dataclasses.Parser` plugin in a form of a python dictionary.
The method also returns results in a form of a python dictionary.

The :meth:`algorithm_tester_common.tester_dataclasses.Algorithm.get_columns` method
is used to select keys from the results of the algorithm. Data under these keys
will be added to the output file.

Add Parsers
-------------
New parsers need to conform 
:class:`algorithm_tester_common.tester_dataclasses.Parser` class.

An example of how to add a new parser:

.. code-block:: python

    from algorithm_tester_common.tester_dataclasses import Parser

    class NewParser(Parser):
        """
        DocString used in help.
        
        """

        def get_name(self) -> str:
            ...

        def get_output_file_name(self, context: AlgTesterContext, input_file: IO, click_args: Dict[str, object]) -> str:
            ...

        def get_instance_identifier(self, instance_data: Dict[str, object]) -> str:
            ...

        def get_num_of_instances(self, context: AlgTesterContext, input_file: IO) -> int:
            ...

        def get_next_instance(self, input_file: IO) -> Dict[str, object]:
            ...

        def write_result_to_file(self, output_file: IO, data: Dict[str, object]):
            ...

Parser plugins make it possible to use any format of input and output files.
It's responsible for parsing instance data from input files and writing results into output files.

Add Communicators
--------------------
New communicators need to conform 
:class:`algorithm_tester_common.tester_dataclasses.Communicators` class.

An example of how to add a new communicator:

.. code-block:: python

    from algorithm_tester_common.tester_dataclasses import Communicator

    class NewComm(Communicator):
        def get_name(self) -> str:
            ...
            
        def notify_instance_computed(self, context: AlgTesterContext, last_solution: Dict[str, object], num_of_instances_done: int, num_of_instances_failed: int):
            ...

They make it possible to remotely monitor progress of computation. 
Communicators are notified in desired intervals.

AlgorithmTester has a built-in Slack communicator. More about it in :ref:`slack` section.