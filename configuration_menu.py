try:
    from aqt import mw
    from aqt.qt import *
    from . import passfail2
except Exception as e1:
    print("pf logger: 1-" + str(e1))


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.preview_config = read_config()
        self.error_label = None
        self.mainWindow()

    def mainWindow(self):
        self.setWindowTitle("Pass / Fail 2 v0.3.0")
        self.setMinimumWidth(500)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Ensures that the widget inside the scroll area resizes correctly

        # Create a widget to hold the layout
        widget = QWidget()
        scroll_area.setWidget(widget)

        layout = QVBoxLayout(widget)

        # text
        # Adding subtitle
        subtitle_label = QLabel("Credits: Ashlynn Anderson, Dmitry Mikheev, and Rohan Modi", self)
        subtitle_label.setStyleSheet("font-size: 12px; font-style: italic;")
        layout.addWidget(subtitle_label)

        # Adding paragraph
        paragraph_label = QLabel("This add-on replaces the original answer options with just two, which correspond to again, and good. This helps avoid issues such as ease hell, and helps eliminate the stress from grading. If you'd like, you can use the following options to enable custom coloring and naming of the two buttons. On some versions of Anki, the background color customization may not work, so you are free to toggle it, if it breaks things. There are two preview buttons, which reflect what the colorscheme of your buttons would look like, if you had both tickboxes checked. \n\n Remember to save your changes, and restart anki to see your changes take effect.", self)
        paragraph_label.setWordWrap(True)
        layout.addWidget(paragraph_label)

        # first toggle switch
        # Adding first toggle switch
        self.toggle_names_textcolors = QCheckBox("Toggle Renaming and Custom TextColors", self)
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

        # Adding button 1
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

        # Adding button 2
        self.good_textcolor_picker = QPushButton("Color Picker", self)
        self.good_textcolor_picker.setEnabled(False)  # Initially disabled
        self.good_textcolor_picker.clicked.connect(lambda: self.colorPick(2))
        good_button_textcolor.addWidget(self.good_textcolor_picker)

        layout.addLayout(good_button_textcolor)

        # second toggle switch

        self.toggle_bgcolor = QCheckBox("Toggle Background Color", self)
        self.toggle_bgcolor.stateChanged.connect(self.toggleInputs2)
        layout.addWidget(self.toggle_bgcolor)

        # Additional text input boxes with labels
        again_button_bgcolor = QHBoxLayout()
        again_button_bgcolor.addWidget(QLabel("'Again' BG Color", self))
        self.again_button_bgcolor = QLineEdit(self)
        self.again_button_bgcolor.setPlaceholderText("Default: #de0d0d")
        again_button_bgcolor.addWidget(self.again_button_bgcolor)

        # Adding button 4
        self.again_bgcolor_picker = QPushButton("Color Picker", self)
        self.again_bgcolor_picker.setEnabled(False)  # Initially disabled
        self.again_bgcolor_picker.clicked.connect(lambda: self.colorPick(3))
        again_button_bgcolor.addWidget(self.again_bgcolor_picker)

        layout.addLayout(again_button_bgcolor)

        good_button_bgcolor = QHBoxLayout()
        good_button_bgcolor.addWidget(QLabel("'Good' BG Color", self))
        self.good_button_bgcolor = QLineEdit(self)
        self.good_button_bgcolor.setPlaceholderText("Default: #26a269")
        good_button_bgcolor.addWidget(self.good_button_bgcolor)

        # Adding button 3
        self.good_bgcolor_picker = QPushButton("Color Picker", self)
        self.good_bgcolor_picker.setEnabled(False)  # Initially disabled
        self.good_bgcolor_picker.clicked.connect(lambda: self.colorPick(4))
        good_button_bgcolor.addWidget(self.good_bgcolor_picker)

        layout.addLayout(good_button_bgcolor)

        preview_buttons_layout = QHBoxLayout()

        # Again Preview Button
        self.again_preview = QPushButton(self.preview_config['again_button_name'], self)
        self.again_preview.setStyleSheet(
            "color: " + self.preview_config['again_button_textcolor'] + "; background-color: " + self.preview_config[
                'again_button_bgcolor'])
        preview_buttons_layout.addWidget(self.again_preview)

        # Good Preview Button
        self.good_preview = QPushButton(self.preview_config['good_button_name'], self)
        self.good_preview.setStyleSheet(
            "color: " + self.preview_config['good_button_textcolor'] + "; background-color: " + self.preview_config[
                'good_button_bgcolor'])
        preview_buttons_layout.addWidget(self.good_preview)

        layout.addLayout(preview_buttons_layout)

        label_buttons_layout = QHBoxLayout()
        paragraph_label = QLabel("Press Preview to Refresh the Above Preview Buttons, and Save to Save.")
        label_buttons_layout.addWidget(paragraph_label)
        layout.addLayout(label_buttons_layout)

        # Adding centered buttons next to each other
        bottom_buttons_layout = QHBoxLayout()

        # Again Preview Button

        self.cancel_changes = QPushButton("Cancel Changes", self)
        self.cancel_changes.clicked.connect(lambda: self.close_config_window())
        bottom_buttons_layout.addWidget(self.cancel_changes)

        self.preview_refresh = QPushButton("Refresh the Previews", self)
        self.preview_refresh.clicked.connect(lambda: self.update_preview_config())
        bottom_buttons_layout.addWidget(self.preview_refresh)

        # Good Preview Button
        self.save_button = QPushButton("Save Changes", self)
        self.save_button.clicked.connect(lambda: self.write_config())
        bottom_buttons_layout.addWidget(self.save_button)

        layout.addLayout(bottom_buttons_layout)

        error_message_layout = QHBoxLayout()
        self.error_label = QLabel(
            "There is an error with one of the fields you inputted. All names must be 0-15 Characters, and all colors must be in valid hex format, beginning with a #. They should be 7 characters long including the #.")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        error_message_layout.addWidget(self.error_label)
        layout.addLayout(error_message_layout)

        ################

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Set default states

        self.prepopulate_fields()
        self.error_label.hide()
        print(str(self.toggle_names_textcolors.checkState()))
        self.toggleInputs1(self.toggle_names_textcolors.checkState())
        self.toggleInputs2(self.toggle_bgcolor.checkState())

    def toggleInputs1(self, state):
        if state == 2 or str(state) == "CheckState.Checked":  # Checked state
            self.again_button_name.setEnabled(True)
            self.good_button_name.setEnabled(True)
            self.again_button_textcolor.setEnabled(True)
            self.good_button_textcolor.setEnabled(True)
            self.toggle_bgcolor.setEnabled(True)  # Enable second checkbox
            self.again_textcolor_picker.setEnabled(True)  # Enable button 1
            self.good_textcolor_picker.setEnabled(True)  # Enable button 2
        else:  # Unchecked state
            self.again_button_name.setEnabled(False)
            self.good_button_name.setEnabled(False)
            self.again_button_textcolor.setEnabled(False)
            self.good_button_textcolor.setEnabled(False)
            # self.toggle_bgcolor.setChecked(False)  # Uncheck second checkbox
            # self.toggle_bgcolor.setEnabled(False)  # Disable second checkbox
            self.again_textcolor_picker.setEnabled(False)  # Disable button 1
            self.good_textcolor_picker.setEnabled(False)  # Disable button 2

    def toggleInputs2(self, state):
        if state == 2 or str(state) == "CheckState.Checked":  # Checked state
            self.again_button_bgcolor.setEnabled(True)
            self.good_button_bgcolor.setEnabled(True)

            self.good_bgcolor_picker.setEnabled(True)  # Enable button 3
            self.again_bgcolor_picker.setEnabled(True)  # Enable button 4
        else:  # Unchecked state
            self.again_button_bgcolor.setEnabled(False)
            self.good_button_bgcolor.setEnabled(False)

            self.good_bgcolor_picker.setEnabled(False)  # Disable button 3
            self.again_bgcolor_picker.setEnabled(False)  # Disable button 4

    def colorPick(self, button_number):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if button_number == 1:
                # self.again_textcolor_picker.setStyleSheet(f"background-color: {hex_color};")
                self.again_button_textcolor.setText(hex_color)
            elif button_number == 2:
                # self.good_textcolor_picker.setStyleSheet(f"background-color: {hex_color};")
                self.good_button_textcolor.setText(hex_color)
            elif button_number == 3:
                # self.good_bgcolor_picker.setStyleSheet(f"background-color: {hex_color};")
                self.again_button_bgcolor.setText(hex_color)
            elif button_number == 4:
                # self.again_bgcolor_picker.setStyleSheet(f"background-color: {hex_color};")
                self.good_button_bgcolor.setText(hex_color)

    def prepopulate_fields(self):
        config_from_json = read_config()

        self.toggle_names_textcolors.setChecked(bool(int(config_from_json['toggle_names_textcolors'])))
        self.again_button_name.setText(config_from_json['again_button_name'])
        self.good_button_name.setText(config_from_json['good_button_name'])
        self.again_button_textcolor.setText(config_from_json['again_button_textcolor'])
        self.good_button_textcolor.setText(config_from_json['good_button_textcolor'])
        self.toggle_bgcolor.setChecked(bool(int(config_from_json['toggle_bgcolor'])))
        self.again_button_bgcolor.setText(config_from_json['again_button_bgcolor'])
        self.good_button_bgcolor.setText(config_from_json['good_button_bgcolor'])

        return config_from_json

    def update_preview_config(self):

        if self.current_config_is_valid():
            self.preview_config = {'toggle_names_textcolors': "1" if self.toggle_names_textcolors.isChecked() else "0",
                                   'again_button_name': self.again_button_name.text(),
                                   'good_button_name': self.good_button_name.text(),
                                   'again_button_textcolor': self.again_button_textcolor.text(),
                                   'good_button_textcolor': self.good_button_textcolor.text(),
                                   'toggle_bgcolor': "1" if self.toggle_bgcolor.isChecked() else "0",
                                   'again_button_bgcolor': self.again_button_bgcolor.text(),
                                   'good_button_bgcolor': self.good_button_bgcolor.text()}
            self.error_label.hide()
            self.update_preview_buttons()
        else:
            self.error_label.show()

    def update_preview_buttons(self):
        self.again_preview.setText(self.preview_config['again_button_name'])
        self.again_preview.setStyleSheet(
            "color: " + self.preview_config['again_button_textcolor'] + "; background-color: " + self.preview_config[
                'again_button_bgcolor'])
        self.good_preview.setText(self.preview_config['good_button_name'])
        self.good_preview.setStyleSheet(
            "color: " + self.preview_config['good_button_textcolor'] + "; background-color: " + self.preview_config[
                'good_button_bgcolor'])

    def write_config(self):
        if self.current_config_is_valid():
            self.update_preview_config()
            mw.addonManager.writeConfig(__name__, self.preview_config)
            self.close_config_window()

        else:
            self.error_label.show()

    def close_config_window(self):
        self.close()

    def current_config_is_valid(self):
        is_valid = (is_valid_name(self.again_button_name.text()) and is_valid_name(
            self.good_button_name.text()) and is_valid_hex_color(
            self.again_button_textcolor.text()) and is_valid_hex_color(
            self.good_button_textcolor.text()) and is_valid_hex_color(
            self.again_button_bgcolor.text()) and is_valid_hex_color(self.good_button_bgcolor.text()))
        return is_valid


def openWindow():
    settingsDialog = SettingsDialog()
    settingsDialog.exec()


def is_valid_hex_color(hexstring_to_validate):
    # Check if the string starts with a hashtag and is 7 characters long
    if len(hexstring_to_validate) != 7 or hexstring_to_validate[0] != '#':
        return False

    # Define the valid characters
    valid_chars = set("0123456789abcdefABCDEF")

    # Check if all characters in the string (except the first) are valid
    for char in hexstring_to_validate[1:]:
        if char not in valid_chars:
            return False

    return True


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
    except Exception as e:
        print("Issue with Pass / Fail: " + str(e))
