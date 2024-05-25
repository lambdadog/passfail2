try:
    from anki.scheduler.v3 import Scheduler as V3Scheduler
    import aqt
    from aqt.utils import tr
except Exception as e1:
    print("Issue with Pass / Fail: " + str(e1))

try:
    from aqt import mw
except Exception as e1:
    print("Issue with Pass / Fail: " + str(e1))



def answer_buttons_with_bgcolor(self) -> str:
    try:
        config = mw.addonManager.getConfig(__name__)
    except Exception as e:
        print("Issue with Pass / Fail: " + str(e))

    default = self._defaultEase()

    assert isinstance(self.mw.col.sched, V3Scheduler)
    labels = self.mw.col.sched.describe_next_states(self._v3.states)

    def but(i: int, label: str) -> str:
        if i == default:
            extra = """id="defease" """
        else:
            extra = ""

        ## inserted ##

        answer_button_background_color = '#ffffff'
        if font_tag_stripper(label) == config['again_button_name']:
            answer_button_background_color = config['again_button_bgcolor']
        elif font_tag_stripper(label) == config['good_button_name']:
            answer_button_background_color = config['good_button_bgcolor']

        ## inserted ##

        due = self._buttonTime(i, v3_labels=labels)
        key = (
            tr.actions_shortcut_key(val=aqt.mw.pm.get_answer_key(i))
            if aqt.mw.pm.get_answer_key(i)
            else ""
        )
        return f"""<td align=center> <button %s title="%s" data-ease="%s" onclick='pycmd("ease%d");'
        style="background-color: %s;">%s%s</button></td>""" % (  # inserted style
            extra,
            key,
            i,
            i,
            answer_button_background_color,  # inserted
            label,
            due,
        )

    buf = "<center><table cellpadding=0 cellspacing=0><tr>"
    for ease, label in self._answerButtonList():
        buf += but(ease, label)
    buf += "</tr></table>"
    print(label)
    print(config['again_button_name'])
    return buf

def answer_buttons_bgcolor_2_1_15(self):
    try:
        config = mw.addonManager.getConfig(__name__)
    except Exception as e:
        print("Issue with Pass / Fail: " + str(e))

    ## inserted ##

    answer_button_background_color = '#ffffff'


    ## inserted ##

    default = self._defaultEase()
    def but(i, label, bgcolor='#ffffff'):
        if i == default:
            extra = "id=defease"
        else:
            extra = ""
        due = self._buttonTime(i)
        return '''
<td align=center>%s<button %s style="background-color: %s" title="%s" data-ease="%s" onclick='pycmd("ease%d");'>\
%s</button></td>''' % (due, extra, answer_button_background_color, _("Shortcut key: %s") % i, i, i, label)
    buf = "<center><table cellpading=0 cellspacing=0><tr>"
    for ease, label in self._answerButtonList():

        if font_tag_stripper(label) == config['again_button_name']:
            answer_button_background_color = config['again_button_bgcolor']
        elif font_tag_stripper(label) == config['good_button_name']:
            answer_button_background_color = config['good_button_bgcolor']


        buf += but(ease, label,answer_button_background_color)
    buf += "</tr></table>"
    script = """
<script>$(function () { $("#defease").focus(); });</script>"""
    print(buf)
    return buf + script




def font_tag_stripper(input_string):
    pass
    if len(input_string) > 28:
        if input_string[-7:] == "</font>":
            return input_string[22:-7]
    else:
        return input_string