'''
Provide singleton for DialogueManager

Author: Ming Fang
'''

from weiss.dialogue.dialogueManager import DialogueManager

_instance = None


def getDialogueManager():
    global _instance
    if _instance is None:
        _instance = DialogueManager()

    return _instance
