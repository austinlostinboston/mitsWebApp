"""

Copyright 2015 Austin Ankney, Ming Fang, Wenjun Wang and Yao Zhou

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This file defines the concrete control flow logic
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
