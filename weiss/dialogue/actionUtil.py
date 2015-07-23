'''
Utility methods for actions
Note that, in practice, it is no need to import any from actions.py.
Just import needed method from actionUtil.py


Author: Ming Fang
'''

from django.contrib.auth.models import User

from weiss.models import History

def confirmAciton(UserName, ActionID):
    print 'confirmAciton called'
    # Find user
    user = User.objects.get(username=UserName)
    # Get last history record of that user
    his = History.objects.filter(userid=user.id).order_by('-hid')[0]
    # Modify ddid
    print str(his.hid) + "," + str(his.userid) + "," + str(his.desired_aid)
    his.desired_aid = ActionID
    # Update database
    his.save()
    return
