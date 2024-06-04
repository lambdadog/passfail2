# This should maybe be a class, but there should never be multiple
# instances of it, really.

from .logger import log

from aqt import mw

_config = {
    'toggle_names_textcolors': "0",
    'again_button_name': "Fail",
    'good_button_name': "Pass",
    'again_button_textcolor': "#000000",
    'good_button_textcolor': "#000000"
}

# Required asserts to make config work properly
assert(not any(isinstance(val, dict) for val in _config.values()))
assert(all(isinstance(val, str) for val in _config.values()))

def as_str(key):
    return _config[key]
def as_bool(key):
    return bool(int(_config[key]))

def update(new_kv):
    for k in new_kv.keys():
        if k in _config:
            _config[k] = new_kv[k]
        else:
            raise KeyError("Key '%s' does not exist in config.".format(k))

    save()

def copy():
    return _config.copy()

def load():
    try:
        fs_config = mw.addonManager.getConfig(__name__)

        # We don't reuse update here because we want to silently
        # ignore removed keys in newer versions
        for k in _config.keys():
            try:
                _config[k] = fs_config[k]
            except:
                ()
    except:
        log.warn("Failed to load config. Writing.")

    log.info(_config)

    save()

def save():
    mw.addonManager.writeConfig(__name__, _config)
