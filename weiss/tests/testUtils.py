"""
A misc utilities for testing

Author: Ming Fang
"""
from termcolor import colored
from django.test.runner import DiscoverRunner



"""
The following is for print colorful stuff to terminal
If your Python is complaining about missing package, do this:
    sudo pip install termcolor
"""
PASSED = colored('PASSED', 'green')
FAILED = colored('FAILED', 'red')



class NoDbTestRunner(DiscoverRunner):
    """
    A test runner to test without database creation
    To run test wit this, add the following to the settings.py
    TEST_RUNNER = 'weiss.tests.testUtils.NoDbTestRunner'
    """

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass
