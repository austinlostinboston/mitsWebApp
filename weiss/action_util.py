import logging
from weiss.action import *

logger = logging.getLogge(__name__)


actions = [nextRandomEntity,
           nextRandomCmt,
           nextRandomPositiveCmt,
           nextRandomNegativeCmt,
           nextRandomOppositeCmt,
           ]

def dispatch(request):
    actonId = request.POST['aid']
    action = action[aid]
    logger.DEBUG("Dispatch action: %s, %s" % (aid, action))
    action(session, request.POST)


