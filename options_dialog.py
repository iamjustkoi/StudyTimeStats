# import aqt.qt.qt5
from aqt.qt import QDialog
# from aqt.qt.qt5 import QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, QFormLayout, QLabel, QComboBox, QGroupBox, \
#     QCheckBox, QDialogButtonBox
# from PyQt5.QtCore import Qt
from .config import RTConfigManager
# from .consts import Days


class RTOptionsDialog(QDialog):
    def __init__(self, config: RTConfigManager):
        super(RTOptionsDialog, self).__init__()

        self.setWindowTitle("Review Time Overview Options")

    #     self.options_vert_layout = QVBoxLayout(self)
    #     self.options_vert_layout.setObjectName(u"options_vert_layout")
    #     self.tabs_widget = QTabWidget(self)
    #     self.tabs_widget.setObjectName(u"tabs_widget")
    #     self.appearance_tab = QWidget()
    #     self.appearance_tab.setObjectName(u"appearance_tab")
    #     self.appearance_tab.setEnabled(True)
    #     self.appearance_tab_layout = QVBoxLayout(self.appearance_tab)
    #     self.appearance_tab_layout.setObjectName(u"appearance_tab_layout")
    #     self.appearance_vert_layout = QVBoxLayout()
    #     self.appearance_vert_layout.setObjectName(u"appearance_vert_layout")
    #     self.appearance_vert_layout.setContentsMargins(12, 12, 12, 12)
    #     self.week_start_form = QFormLayout()
    #     self.week_start_form.setObjectName(u"week_start_form")
    #     self.week_start_form.setFormAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
    #     self.week_start_label = QLabel(self.appearance_tab)
    #     self.week_start_label.setObjectName(u"week_start_label")
    #
    #     self.week_start_form.setWidget(0, QFormLayout.LabelRole, self.week_start_label)
    #
    #     self.week_start_dropdown = QComboBox(self.appearance_tab)
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.addItem("")
    #     self.week_start_dropdown.setObjectName(u"week_start_dropdown")
    #     self.week_start_dropdown.setSizeAdjustPolicy(QComboBox.AdjustToContents)
    #
    #     self.week_start_form.setWidget(0, QFormLayout.FieldRole, self.week_start_dropdown)
    #
    #     self.appearance_vert_layout.addLayout(self.week_start_form)
    #
    #     self.pages_group_box = QGroupBox(self.appearance_tab)
    #     self.pages_group_box.setObjectName(u"pages_group_box")
    #     self.pages_vertical_layout = QHBoxLayout(self.pages_group_box)
    #     self.pages_vertical_layout.setObjectName(u"pages_vertical_layout")
    #     self.browser_checkbox = QCheckBox(self.pages_group_box)
    #     self.browser_checkbox.setObjectName(u"browser_checkbox")
    #     self.browser_checkbox.setChecked(True)
    #
    #     self.pages_vertical_layout.addWidget(self.browser_checkbox)
    #
    #     self.overview_checkbox = QCheckBox(self.pages_group_box)
    #     self.overview_checkbox.setObjectName(u"overview_checkbox")
    #     self.overview_checkbox.setChecked(True)
    #
    #     self.pages_vertical_layout.addWidget(self.overview_checkbox)
    #
    #     self.congrats_checkbox = QCheckBox(self.pages_group_box)
    #     self.congrats_checkbox.setObjectName(u"congrats_checkbox")
    #     self.congrats_checkbox.setChecked(True)
    #
    #     self.pages_vertical_layout.addWidget(self.congrats_checkbox)
    #
    #     self.appearance_vert_layout.addWidget(self.pages_group_box)
    #
    #     self.appearance_tab_layout.addLayout(self.appearance_vert_layout)
    #
    #     self.tabs_widget.addTab(self.appearance_tab, "")
    #
    #     self.options_vert_layout.addWidget(self.tabs_widget)
    #
    #     self.confirm_button_box = QDialogButtonBox(self)
    #     self.confirm_button_box.setObjectName(u"confirm_button_box")
    #     self.confirm_button_box.setOrientation(Qt.Horizontal)
    #     self.confirm_button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)
    #
    #     self.options_vert_layout.addWidget(self.confirm_button_box)
    #
    #     self.retranslate_ui()
    #     self.confirm_button_box.accepted.connect(self.accept)
    #     self.confirm_button_box.rejected.connect(self.reject)
    #
    #     self.tabs_widget.setCurrentIndex(0)
    #
    # def retranslate_ui(self):
    #     self.week_start_label.setText(aqt.AnkiApp.translate("self", u"Week Start Day", None))
    #     self.week_start_dropdown.setItemText(0, aqt.AnkiApp.translate("self", u"Sunday", None))
    #     self.week_start_dropdown.setItemText(1, aqt.AnkiApp.translate("self", u"Monday", None))
    #     self.week_start_dropdown.setItemText(2, aqt.AnkiApp.translate("self", u"Tuesday", None))
    #     self.week_start_dropdown.setItemText(3, aqt.AnkiApp.translate("self", u"Wednesday", None))
    #     self.week_start_dropdown.setItemText(4, aqt.AnkiApp.translate("self", u"Thursday", None))
    #     self.week_start_dropdown.setItemText(5, aqt.AnkiApp.translate("self", u"Friday", None))
    #     self.week_start_dropdown.setItemText(6, aqt.AnkiApp.translate("self", u"Saturday", None))
    #
    #     self.pages_group_box.setTitle(aqt.AnkiApp.translate("self", u"Pages", None))
    #     self.browser_checkbox.setText(aqt.AnkiApp.translate("self", u"Deck Browser", None))
    #     self.overview_checkbox.setText(aqt.AnkiApp.translate("self", u"Overview", None))
    #     self.congrats_checkbox.setText(aqt.AnkiApp.translate("self", u"Congrats Screen", None))
    #
    #     appearance_index = self.tabs_widget.indexOf(self.appearance_tab)
    #     self.tabs_widget.setTabText(appearance_index, aqt.AnkiApp.translate("self", u"Appearance", None))
    #
    # def accept(self) -> None:
    #     super(RTOptionsDialog, self).accept()
    #
    # def reject(self) -> None:
    #     super(RTOptionsDialog, self).reject()
