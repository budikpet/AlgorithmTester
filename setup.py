from setuptools import setup, find_packages
import os
from typing import List

def get_plugins() -> List[str]:
    """
    Uses dummy plugins only if we are testing the framework.
    
    Returns:
        List[str] -- Plugins entrypoints.
    """
    res: List[str] = ['communicators_internal = communicators_slack']
    if os.path.isfile("./tests/dummy_plugins/fixtures/slack_communicator.cfg"):
        res.extend([
            'algorithms = tests.dummy_plugins',
            'parsers = tests.dummy_plugins'
        ])
    
    return res

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='algorithm_tester',
    version='0.7.2',
    description='Algorithms tester for MI-PAA.',
    long_description=long_description,
    keywords="algorithms,tester,budikpet, cli",
    setup_requires=['pytest-runner'],
    install_requires=['Click', 'slackclient'],
    tests_require=['pytest==5.0.1', 'flexmock'],
    
    # All these 'dev' packages can then be installed by 'pip install .[dev]'
    extras_require={
        'dev':  ["sphinx"],
        'tests': ['pytest==5.0.1', 'flexmock']
    },
    python_requires='>=3.7',
    author='Petr Budik',
    author_email='budikpet@fit.cvut.cz',
    license='Public Domain',
    url='https://github.com/budikpet/AlgorithmTester',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run_tester = algorithm_tester:run_tester_cli_interface',
        ],
        'algorithm_tester.plugins': get_plugins()
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Environment :: Console',
        ],
)