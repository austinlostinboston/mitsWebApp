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

Utility methods for actions

Author: Ming Fang
"""

from django.contrib.auth.models import User

from weiss.models import History, Type


def confirmAciton(user_name, aid):
    print 'confirmAciton called'
    # Find user
    user = User.objects.get(username=user_name)
    # Get last history record of that user
    his = History.objects.filter(userid=user.id).order_by('-hid')[0]
    # Modify ddid
    print str(his.hid) + "," + str(his.userid) + "," + str(his.desired_aid)
    his.desired_aid = aid
    # Update database
    his.save()
    return

def get_type_range(entities):
    type_range = set()
    for entity in entities:
        this_type = Type(entity.tid.tid)
        if this_type not in type_range:
            type_range.add(this_type)
    return type_range



