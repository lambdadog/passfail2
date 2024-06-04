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

from .logger import log

try:
    from typing import Literal, Callable
except ImportError as err:
    log.debug("Typing import failure: %s", err)

from aqt import mw

try:
    from anki.utils import point_version
except ImportError:
    try:
        from anki.utils import pointVersion as point_version
    except:
        from anki import version # pyright: ignore
        def point_version():
            return int(version.split(".")[-1])

from . import config
from . import configuration_menu

from anki.hooks import wrap

from aqt.reviewer import Reviewer
from anki.cards import Card

if point_version() >= 20:
    import aqt.gui_hooks as gui_hooks

if point_version() >= 45:
    from aqt.utils import tr
elif point_version() >= 41:
    from aqt.utils import tr
    from anki.lang import TR
else:
    from anki.lang import _

# Hooks
def pf2_hook_replace_buttons(
        buttons_tuple, # type: tuple[tuple[int, str], ...]
        reviewer,      # type: Reviewer
        card           # type: Card
): # type: (...) -> tuple[tuple[int,str], ...]
    again_text = "Fail"
    good_text = "Pass"

    if config.as_bool('toggle_names_textcolors'):
        again_text = "<font color='{}'>{}</font>".format(
            config.as_str('again_button_textcolor'),
            config.as_str('again_button_name')
        )
        good_text = "<font color='{}'>{}</font>".format(
            config.as_str('good_button_textcolor'),
            config.as_str('good_button_name')
        )

    return (
        (1, again_text),
        (reviewer._defaultEase(), good_text)
    )

def pf2_hook_remap_answer_ease(
        ease_tuple, # type: tuple[bool, Literal[1, 2, 3, 4]]
        reviewer,   # type: Reviewer
        card        # type: Card
): # type: (...) -> tuple[bool, Literal[1, 2, 3, 4]]
    (cont, ease) = ease_tuple
    if ease == 1:
        return ease_tuple
    else:
        return (cont, reviewer._defaultEase())

# Shims for old versions of anki
def pf2_shim_answerButtonList(
        self, # type: Reviewer
        _old  # type: Callable[[Reviewer], tuple[tuple[int, str], ...]]
): # type: (...) -> tuple[tuple[int, str], ...]
    result = _old(self)
    if self.card:
        return pf2_hook_replace_buttons(result, self, self.card)
    else:
        return result

def pf2_shim_answerCard(
        self, # type: Reviewer
        ease, # type: Literal[1, 2, 3, 4]
        _old  # type: Callable[[Reviewer, Literal[1, 2, 3, 4]], None]
): # type: (...) -> None
    if self.card: # Should always be true
        (_, new_ease) = pf2_hook_remap_answer_ease((True, ease), self, self.card)
        return _old(self, new_ease)
    else:
        return _old(self, ease)

# Run after drawing ease buttons
def pf2_fix_pass_title(
        self # type: Reviewer
): # type: (...) -> None
    title = None
    if point_version() >= 45:
        title = tr.actions_shortcut_key(val=2)
    elif point_version() >= 41:
        title = tr(TR.ACTIONS_SHORTCUT_KEY, val=2)
    else:
        title = _("Shortcut key: %s") % 2

    self.bottom.web.eval(
        f'document.getElementById("defease").title = "{title}";'
    )

# Init
def init():
    version = point_version()

    config.load()
    configuration_menu.configuration_menu_init()

    # Answer button list
    if version >= 31:
        gui_hooks.reviewer_will_init_answer_buttons.append(pf2_hook_replace_buttons)
    else:
        Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, pf2_shim_answerButtonList, 'around')

    # Remap ease for keybinds
    if version >= 20:
        gui_hooks.reviewer_will_answer_card.append(pf2_hook_remap_answer_ease)
    else:
        Reviewer._answerCard = wrap(Reviewer._answerCard, pf2_shim_answerCard, 'around')

    # Show "Shortcut key: 2" rather than "Shortcut key: 3" for "Pass" button
    Reviewer._showEaseButtons = wrap(Reviewer._showEaseButtons, pf2_fix_pass_title, 'after')
