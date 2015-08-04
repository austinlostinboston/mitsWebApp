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

This file contains responses for different API

Author: Ming Fang
"""

class InitResponse(object):
    """
    unregister user will be assign one flow id
    register user will use user id as flow id
    """
    def __init__(self, response):
        self.response = response


class QueryResponse(object):

    def __init__(self, response):
        self.response = response


class CloseResponse(object):

    def __init__(self, status):
        self.status = status


