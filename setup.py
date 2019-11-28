from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='algorithm_tester',
    version='0.3',
    description='Algorithms tester for MI-PAA.',
    long_description=long_description,
    keywords="algorithms,tester,budikpet, cli",
    setup_requires=['pytest-runner'],
    install_requires=['click>=6', 'numpy', 'notebook', 'pandas'],
    tests_require=['pytest==5.0.1', 'flexmock'],
    extras_require={
        'dev':  ["sphinx"]
    },
    python_requires='>=3.7',
    author='Petr Budík',
    author_email='budikpet@fit.cvut.cz',
    license='Public Domain',
    url='https://github.com/budikpet/AlgorithmTester',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'solver = algorithm_tester:solver',
        ],
    },
    # package_data={
    #     'ghia': ['templates/*.html', 'static/*.css']
    #     },
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