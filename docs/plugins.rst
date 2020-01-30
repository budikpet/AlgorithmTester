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

Algorithms
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

The :meth:`algorithm_tester_common.tester_dataclasses.Algorithm.get_name` function
is the identification of the algorithm. More information about using 
these identifiers in :ref:`howToUse` section.