"""
This file defines the concrete control flow logic

Author: Ming Fang
"""
from weiss.flows.abstractState import State

"""
Definitions of the system states
"""
SystemInitiative = State("System Initiative")
TypeSelected = State("Type Selected")
EntitySelected = State("Entity Selected")
CommentSelected = State("Comment Selected")



"""
Definition of the control flow
1. Next Random Comment
2. Next Opposite Comment
3. Next Positive Comment
4. Next Negative Comment
5. Next Random Entity (within current type)
6. Sentiment Stats
7. Entity Selection (base on key and within current type)
8. Type Selection
9. Type and Entity Selection
"""

"""
Systen initialization state
the beginning point of the dialog
"""
SystemInitiative[7] = EntitySelected
SystemInitiative[8] = TypeSelected


"""
Type selected state
The followings should be determined:
    curr_tid
"""
TypeSelected[7] = EntitySelected
TypeSelected[8] = TypeSelected

"""
Entity selceted state
The followings should be determined:
    curr_tid
    curr_eid
"""
EntitySelected[1] = CommentSelected
EntitySelected[3] = CommentSelected
EntitySelected[4] = CommentSelected

EntitySelected[5] = EntitySelected
EntitySelected[6] = EntitySelected
EntitySelected[7] = EntitySelected
EntitySelected[9] = EntitySelected

EntitySelected[8] = TypeSelected


"""
Comment selecetd state
The followings should be determined:
    curr_tid
    curr_eid
    curr_cid
"""
CommentSelected[1] = CommentSelected
CommentSelected[2] = CommentSelected
CommentSelected[3] = CommentSelected
CommentSelected[4] = CommentSelected
CommentSelected[6] = CommentSelected

CommentSelected[5] = EntitySelected
CommentSelected[7] = EntitySelected
CommentSelected[9] = EntitySelected

CommentSelected[8] = TypeSelected





