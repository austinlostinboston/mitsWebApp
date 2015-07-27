"""
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
    range = set()
    for entity in entities:
        this_type = Type(entity.tid.tid)
        if this_type not in range:
            range.add(this_type)
    return range
