"""
A misc utilities for testing
"""
from termcolor import colored



"""
The following is for print colorful stuff to terminal
If your Python is complaining about missing package, do this:
    sudo pip install termcolor
"""
PASSED = colored('PASSED', 'green')
FAILED = colored('FAILED', 'red')
