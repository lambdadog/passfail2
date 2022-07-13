# Pass/Fail 2
#
# Only offers 2 buttons to press: Pass, and Fail. Fail is equivalent
# to "Again", whereas Pass is equivalent to "Good". This helps remove
# decision paralysis while reviewing and also avoids the fallacy of
# the "Hard" button, which lengthens the amount of time between
# reviewing Hard cards, making them more difficult to acquire.
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2022 Ashlynn Anderson
#
# Regards to Dmitry Mikheev for writing the original add-on this was
# derived from, and the Anki team.

from typing import Literal

from anki.collection import CardIdsLimit
import aqt.gui_hooks as gui_hooks
from aqt.reviewer import Reviewer
from anki.cards import Card

from anki.utils import point_version
from anki.hooks import wrap

# Hooks
def pf2_replace_buttons(
        buttons_tuple: tuple[tuple[int, str], ...],
        reviewer: Reviewer,
        card: Card
) -> tuple[tuple[int, str], ...]:
    return (
        (1, "Fail"),
        (2, "Pass")
    )

def pf2_remap_answer_ease(
        ease_tuple: tuple[bool, Literal[1, 2, 3, 4]],
        reviewer: Reviewer,
        card: Card
) -> tuple[bool, Literal[1, 2, 3, 4]]:
    (cont, ease) = ease_tuple
    if ease == 1:
        return ease_tuple
    else:
        return (cont, reviewer._defaultEase())

def pf2_force_defaultEase(_self) -> Literal[2, 3]:
    return 2

# Shims for old versions of anki
def pf2_shim_answerButtonList(self, _old) -> tuple[tuple[int, str], ...]:
    result = _old(self)
    return pf2_replace_buttons(result, self, self.card)

def pf2_shim_answerCard(self, ease: Literal[1, 2, 3, 4], _old) -> None:
    (_, new_ease) = pf2_remap_answer_ease((True, ease), self, self.card)
    return _old(self, new_ease)

# Init
def init():
    version = point_version()

    # Answer button list
    if version >= 31:
        gui_hooks.reviewer_will_init_answer_buttons.append(pf2_replace_buttons)
    else:
        Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, pf2_shim_answerButtonList, 'around')

    # Remap ease for keybinds
    if version >= 20:
        gui_hooks.reviewer_will_answer_card.append(pf2_remap_answer_ease)
    else:
        Reviewer._answerCard = wrap(Reviewer._answerCard, pf2_shim_answerCard, 'around')

    # Fixes some default behavior, including keybind popup
    Reviewer._defaultEase = pf2_force_defaultEase
