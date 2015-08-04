"""

copyright 2015 austin ankney, ming fang, wenjun wang and yao zhou

licensed under the apache license, version 2.0 (the "license");
you may not use this file except in compliance with the license.
you may obtain a copy of the license at

   http://www.apache.org/licenses/license-2.0

unless required by applicable law or agreed to in writing, software
distributed under the license is distributed on an "as is" basis,
without warranties or conditions of any kind, either express or implied.
see the license for the specific language governing permissions and
limitations under the license.


    Author: Ming Fang
"""
from weiss.flows.states import *
from weiss.utils.switch import switch

def StateFactory(sid):
    assert (isinstance(sid, State))
    """
    Factory for state class
    """
    for case in switch(sid):
        if case(State.SystemInitiative):
            return SystemInitiative()

        if case(State.TypeSelected):
            return TypeSelected()

        if case(State.EntitySelected):
            return EntitySelected()

        if case(State.CommentSelected):
            return CommentSelected()

        if case(State.RangeSelected):
            return RangeSelected()

        if case():
            raise KeyError("No such state %s" % sid)
