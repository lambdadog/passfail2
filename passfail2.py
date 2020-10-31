# -*- mode:Python -*-
# Pass/Fail 2
#
# Only offers 2 buttons to press: Pass, and Fail. Fail is equivalent
# to "Again", whereas Pass is equivalent to "Good". This helps remove
# decision paralysis while reviewing and also avoids the fallacy of
# the "Hard" button, which lengthens the amount of time between
# reviewing Hard cards, making them more difficult to acquire.
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2020 Ashlynn Anderson
#
# Regards to Dmitry Mikheev for writing the original add-on this was
# derived from, and the Anki team.

from aqt.reviewer import Reviewer
from anki.hooks import wrap

## CHANGE ANSWER BUTTONS TO PASS/FAIL ##

# Hardcoding the shortcut keys is a lazy solution,
# but one I'm reasonably okay with
def pfAnswerButtonList(self):
    l = ((1, _("Fail"), _("Shortcut key: 1")),)
    cnt = self.mw.col.sched.answerButtons(self.card)
    if cnt == 2 or cnt == 3:
        return l + ((2, _("Pass"), _("Shortcut keys: 2, 3, 4")),)
    else:
        return l + ((3, _("Pass"), _("Shortcut keys: 2, 3, 4")),)

# For some reason it's necessary to copy over this function instead of
# just wrapping _answerButtonList, I couldn't say why.
def pfAnswerButtons(self, _old):
    default = self._defaultEase()
    def but(i, label, shortcutDialog):
        cnt = self.mw.col.sched.answerButtons(self.card)
        if i == default:
            extra = "id=defease"
        else:
            extra = ""
        due = self._buttonTime(i)
        return '''
<td align=center>%s<button %s title="%s" data-ease="%s" onclick='pycmd("ease%d");'>\
%s</button></td>''' % (due, extra, shortcutDialog, i, i, label)
    buf = "<center><table cellpading=0 cellspacing=0><tr>"
    for ease, label, shortcutDialog in pfAnswerButtonList(self):
        buf += but(ease, label, shortcutDialog)
    buf += "</tr></table>"
    script = """
<script>$(function () { $("#defease").focus(); });</script>"""
    return buf + script

## MAP KEYBINDS TO REFLECT CHANGE ##

# For 2/3 buttons, 1=FAIL/1, 2/3/4=PASS(2)
# For 4 buttons, 1=FAIL/1, 2/3/4=PASS(3)
remap = {
    2:  [None, 1, 2, 2, 2],
    3:  [None, 1, 2, 2, 2],
    4:  [None, 1, 3, 3, 3]
} 

def pfAnswerCard(self, ease, _old):
    cnt = self.mw.col.sched.answerButtons(self.card)
    try:
        ease = remap[cnt][ease]
    except (KeyError, IndexError):
        pass
    _old(self, ease)

def init():
    Reviewer._answerButtons =\
        wrap(Reviewer._answerButtons, pfAnswerButtons, 'around')
    Reviewer._answerCard =\
        wrap(Reviewer._answerCard, pfAnswerCard, 'around')
