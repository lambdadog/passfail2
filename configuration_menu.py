from aqt import mw
from aqt.qt import *

from . import config

from . import passfail2
from . import build_info

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.preview_config = config.copy()
        self.error_label = None
        self.mainWindow()

    def mainWindow(self):
        self.setWindowTitle("Pass/Fail 2 v{}".format(build_info.version))
        self.setMinimumWidth(500)

        scroll_area = QScrollArea(self)
        # Ensures that the widget inside the scroll area resizes correctly
        scroll_area.setWidgetResizable(True) 

        # Create a widget to hold the layout
        widget = QWidget()
        scroll_area.setWidget(widget)

        layout = QVBoxLayout(widget)

        # text
        # Add subtitle
        subtitle_label = QLabel("Credits: Ashlynn Anderson, Dmitry Mikheev, and Rohan Modi", self)
        subtitle_label.setStyleSheet("font-size: 12px; font-style: italic;")
        layout.addWidget(subtitle_label)

        # Add paragraph
        paragraph_label = QLabel("This add-on replaces the original answer options with just two, which correspond to again, and good. This helps avoid issues such as ease hell, and helps eliminate the stress from grading. If you'd like, you can use the following options to enable custom coloring and naming of the two buttons. On some versions of Anki, the background color customization may not work, so you are free to toggle it, if it breaks things. There are two preview buttons, which reflect what the colorscheme of your buttons would look like, if you had both tickboxes checked. \n\n Remember to save your changes, and restart anki to see your changes take effect.", self)
        paragraph_label.setWordWrap(True)
        layout.addWidget(paragraph_label)

        # Add renaming + custom text colors toggle switch
        self.toggle_names_textcolors = QCheckBox("Enable renaming and custom text colors", self)
        self.toggle_names_textcolors.stateChanged.connect(self.toggleInputs1)
        layout.addWidget(self.toggle_names_textcolors)

        # Text input boxes with labels
        again_button_name = QHBoxLayout()
        again_button_name.addWidget(QLabel("'Again' Name", self))
        self.again_button_name = QLineEdit(self)
        self.again_button_name.setPlaceholderText("Default: Fail")
        again_button_name.addWidget(self.again_button_name)
        layout.addLayout(again_button_name)

        good_button_name = QHBoxLayout()
        good_button_name.addWidget(QLabel("'Good' Name", self))
        self.good_button_name = QLineEdit(self)
        self.good_button_name.setPlaceholderText("Default: Pass")
        good_button_name.addWidget(self.good_button_name)
        layout.addLayout(good_button_name)

        again_button_textcolor = QHBoxLayout()
        again_button_textcolor.addWidget(QLabel("'Again' TextColor", self))
        self.again_button_textcolor = QLineEdit(self)
        self.again_button_textcolor.setPlaceholderText("Default: #000000")
        again_button_textcolor.addWidget(self.again_button_textcolor)

        # Add 'Again' color picker
        self.again_textcolor_picker = QPushButton("Color Picker", self)
        self.again_textcolor_picker.setEnabled(False)  # Initially disabled
        self.again_textcolor_picker.clicked.connect(lambda: self.colorPick(1))
        again_button_textcolor.addWidget(self.again_textcolor_picker)
        layout.addLayout(again_button_textcolor)

        good_button_textcolor = QHBoxLayout()
        good_button_textcolor.addWidget(QLabel("'Good' Textcolor", self))
        self.good_button_textcolor = QLineEdit(self)
        self.good_button_textcolor.setPlaceholderText("Default: #000000")
        good_button_textcolor.addWidget(self.good_button_textcolor)

        # Add 'Good' color picker
        self.good_textcolor_picker = QPushButton("Color Picker", self)
        self.good_textcolor_picker.setEnabled(False)  # Initially disabled
        self.good_textcolor_picker.clicked.connect(lambda: self.colorPick(2))
        good_button_textcolor.addWidget(self.good_textcolor_picker)
        layout.addLayout(good_button_textcolor)

        # Add preview buttons
        preview_buttons_layout = QHBoxLayout()

        self.again_preview = QPushButton(self.preview_config['again_button_name'], self)
        self.again_preview.setStyleSheet(
            "color: " + self.preview_config['again_button_textcolor']
        )
        preview_buttons_layout.addWidget(self.again_preview)

        self.good_preview = QPushButton(self.preview_config['good_button_name'], self)
        self.good_preview.setStyleSheet(
            "color: " + self.preview_config['good_button_textcolor']
        )
        preview_buttons_layout.addWidget(self.good_preview)

        layout.addLayout(preview_buttons_layout)

        label_buttons_layout = QHBoxLayout()
        paragraph_label = QLabel("Press Preview to Refresh the Above Preview Buttons, and Save to Save.")
        label_buttons_layout.addWidget(paragraph_label)
        layout.addLayout(label_buttons_layout)

        # Add Cancel/Refresh/Save buttons
        bottom_buttons_layout = QHBoxLayout()

        self.cancel_changes = QPushButton("Cancel Changes", self)
        self.cancel_changes.clicked.connect(lambda: self.close_config_window())
        bottom_buttons_layout.addWidget(self.cancel_changes)

        self.preview_refresh = QPushButton("Refresh the Previews", self)
        self.preview_refresh.clicked.connect(lambda: self.update_preview_config())
        bottom_buttons_layout.addWidget(self.preview_refresh)

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.clicked.connect(lambda: self.write_config())
        bottom_buttons_layout.addWidget(self.save_button)

        layout.addLayout(bottom_buttons_layout)

        # Add error message
        error_message_layout = QHBoxLayout()
        self.error_label = QLabel(
            "There is an error with one of the fields you inputted. All names must be 0-15 Characters, and all colors must be in valid hex format, beginning with a #. They should be 7 characters long including the #.")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        error_message_layout.addWidget(self.error_label)
        layout.addLayout(error_message_layout)

        # Finish plugging in layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Set default states
        self.prepopulate_fields()
        self.error_label.hide()
        self.toggleInputs1(self.toggle_names_textcolors.checkState())

    def toggleInputs1(self, state):
        enabled = False
        if state == 2 or str(state) == "CheckState.Checked":
            enabled = True

        self.again_button_name.setEnabled(enabled)
        self.good_button_name.setEnabled(enabled)
        self.again_button_textcolor.setEnabled(enabled)
        self.good_button_textcolor.setEnabled(enabled)
        self.again_textcolor_picker.setEnabled(enabled)
        self.good_textcolor_picker.setEnabled(enabled)

    def colorPick(self, button_number):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if button_number == 1:
                self.again_button_textcolor.setText(hex_color)
            elif button_number == 2:
                self.good_button_textcolor.setText(hex_color)

    def prepopulate_fields(self):
        self.toggle_names_textcolors.setChecked(bool(int(self.preview_config['toggle_names_textcolors'])))
        self.again_button_name.setText(self.preview_config['again_button_name'])
        self.good_button_name.setText(self.preview_config['good_button_name'])
        self.again_button_textcolor.setText(self.preview_config['again_button_textcolor'])
        self.good_button_textcolor.setText(self.preview_config['good_button_textcolor'])

    def update_preview_config(self):
        if self.current_config_is_valid():
            self.preview_config = {
                'toggle_names_textcolors': "1" if self.toggle_names_textcolors.isChecked() else "0",
                'again_button_name': self.again_button_name.text(),
                'good_button_name': self.good_button_name.text(),
                'again_button_textcolor': self.again_button_textcolor.text(),
                'good_button_textcolor': self.good_button_textcolor.text()
            }
            self.error_label.hide()
            self.update_preview_buttons()
        else:
            self.error_label.show()

    def update_preview_buttons(self):
        self.again_preview.setText(self.preview_config['again_button_name'])
        self.again_preview.setStyleSheet(
            "color: " + self.preview_config['again_button_textcolor']
        )
        self.good_preview.setText(self.preview_config['good_button_name'])
        self.good_preview.setStyleSheet(
            "color: " + self.preview_config['good_button_textcolor']
        )

    def write_config(self):
        if self.current_config_is_valid():
            self.update_preview_config()
            config.update(self.preview_config)
            self.close_config_window()
        else:
            self.error_label.show()

    def close_config_window(self):
        self.close()

    def current_config_is_valid(self):
        is_valid = (
            is_valid_name(self.again_button_name.text())
            and is_valid_name(self.good_button_name.text())
            and is_valid_hex_color(self.again_button_textcolor.text())
            and is_valid_hex_color(self.good_button_textcolor.text())
        )
        return is_valid


def openWindow():
    settingsDialog = SettingsDialog()
    settingsDialog.exec()

def is_valid_hex_color(hexstring_to_validate):
    # Check if the string starts with a hash and is 7 characters long
    if len(hexstring_to_validate) != 7 or hexstring_to_validate[0] != '#':
        return False

    # Define the valid characters
    valid_chars = set("0123456789abcdefABCDEF")

    # Check if all characters in the string (except the first) are valid
    for char in hexstring_to_validate[1:]:
        if char not in valid_chars:
            return False

    return True

# TODO: Is this limited to 15 characters for a reason?
def is_valid_name(name_to_validate):
    if len(name_to_validate) < 15:
        return True
    else:
        return False

def read_config():
    current_config_in_memory = mw.addonManager.getConfig(__name__)
    return current_config_in_memory

def configuration_menu_init():
    try:
        mw.addonManager.setConfigAction(__name__, openWindow)
    except Exception as err:
        log.warn("Failed to initialize configuration menu: %s", err)
