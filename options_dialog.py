# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.resize(402, 380)
        self.options_vert_layout = QtWidgets.QVBoxLayout(OptionsDialog)
        self.options_vert_layout.setObjectName("options_vert_layout")
        self.tabs_widget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabs_widget.setObjectName("tabs_widget")
        self.appearance_tab = QtWidgets.QWidget()
        self.appearance_tab.setEnabled(True)
        self.appearance_tab.setObjectName("appearance_tab")
        self.appearance_tab_layout = QtWidgets.QVBoxLayout(self.appearance_tab)
        self.appearance_tab_layout.setObjectName("appearance_tab_layout")
        self.appearance_vert_layout = QtWidgets.QVBoxLayout()
        self.appearance_vert_layout.setContentsMargins(12, 12, 12, 12)
        self.appearance_vert_layout.setObjectName("appearance_vert_layout")
        self.appearance_grid_layout = QtWidgets.QGridLayout()
        self.appearance_grid_layout.setObjectName("appearance_grid_layout")
        self.primary_color_label = QtWidgets.QLabel(self.appearance_tab)
        self.primary_color_label.setObjectName("primary_color_label")
        self.appearance_grid_layout.addWidget(self.primary_color_label, 6, 0, 1, 1)
        self.seconday_color_button = QtWidgets.QPushButton(self.appearance_tab)
        self.seconday_color_button.setObjectName("seconday_color_button")
        self.appearance_grid_layout.addWidget(self.seconday_color_button, 7, 1, 1, 1)
        self.total_label = QtWidgets.QLabel(self.appearance_tab)
        self.total_label.setObjectName("total_label")
        self.appearance_grid_layout.addWidget(self.total_label, 4, 0, 1, 1)
        self.week_start_dropdown = QtWidgets.QComboBox(self.appearance_tab)
        self.week_start_dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.week_start_dropdown.setObjectName("week_start_dropdown")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.week_start_dropdown.addItem("")
        self.appearance_grid_layout.addWidget(self.week_start_dropdown, 0, 1, 1, 2)
        self.primary_color_button = QtWidgets.QPushButton(self.appearance_tab)
        self.primary_color_button.setObjectName("primary_color_button")
        self.appearance_grid_layout.addWidget(self.primary_color_button, 6, 1, 1, 1)
        self.secondary_color_label = QtWidgets.QLabel(self.appearance_tab)
        self.secondary_color_label.setObjectName("secondary_color_label")
        self.appearance_grid_layout.addWidget(self.secondary_color_label, 7, 0, 1, 1)
        self.ranged_line = QtWidgets.QLineEdit(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ranged_line.sizePolicy().hasHeightForWidth())
        self.ranged_line.setSizePolicy(sizePolicy)
        self.ranged_line.setObjectName("ranged_line")
        self.appearance_grid_layout.addWidget(self.ranged_line, 5, 1, 1, 2)
        self.total_line = QtWidgets.QLineEdit(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_line.sizePolicy().hasHeightForWidth())
        self.total_line.setSizePolicy(sizePolicy)
        self.total_line.setObjectName("total_line")
        self.appearance_grid_layout.addWidget(self.total_line, 4, 1, 1, 2)
        self.primary_color_preview = QtWidgets.QLabel(self.appearance_tab)
        self.primary_color_preview.setStyleSheet("background-color: #BDC;")
        self.primary_color_preview.setObjectName("primary_color_preview")
        self.appearance_grid_layout.addWidget(self.primary_color_preview, 6, 2, 1, 1)
        self.ranged_label = QtWidgets.QLabel(self.appearance_tab)
        self.ranged_label.setObjectName("ranged_label")
        self.appearance_grid_layout.addWidget(self.ranged_label, 5, 0, 1, 1)
        self.secondary_color_preview = QtWidgets.QLabel(self.appearance_tab)
        self.secondary_color_preview.setStyleSheet("background-color: #ADC;")
        self.secondary_color_preview.setObjectName("secondary_color_preview")
        self.appearance_grid_layout.addWidget(self.secondary_color_preview, 7, 2, 1, 1)
        self.week_start_label = QtWidgets.QLabel(self.appearance_tab)
        self.week_start_label.setObjectName("week_start_label")
        self.appearance_grid_layout.addWidget(self.week_start_label, 0, 0, 1, 1)
        self.range_select_label = QtWidgets.QLabel(self.appearance_tab)
        self.range_select_label.setObjectName("range_select_label")
        self.appearance_grid_layout.addWidget(self.range_select_label, 1, 0, 1, 1)
        self.custom_range_spinbox = QtWidgets.QSpinBox(self.appearance_tab)
        self.custom_range_spinbox.setMaximum(5690)
        self.custom_range_spinbox.setProperty("value", 14)
        self.custom_range_spinbox.setObjectName("custom_range_spinbox")
        self.appearance_grid_layout.addWidget(self.custom_range_spinbox, 2, 1, 1, 1)
        self.range_select_dropdown = QtWidgets.QComboBox(self.appearance_tab)
        self.range_select_dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.range_select_dropdown.setObjectName("range_select_dropdown")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.appearance_grid_layout.addWidget(self.range_select_dropdown, 1, 1, 1, 1)
        self.use_start_checkbox = QtWidgets.QCheckBox(self.appearance_tab)
        self.use_start_checkbox.setChecked(True)
        self.use_start_checkbox.setObjectName("use_start_checkbox")
        self.appearance_grid_layout.addWidget(self.use_start_checkbox, 1, 2, 1, 1)
        self.appearance_vert_layout.addLayout(self.appearance_grid_layout)
        self.pages_group_box = QtWidgets.QGroupBox(self.appearance_tab)
        self.pages_group_box.setObjectName("pages_group_box")
        self.pages_vertical_layout = QtWidgets.QHBoxLayout(self.pages_group_box)
        self.pages_vertical_layout.setObjectName("pages_vertical_layout")
        self.browser_checkbox = QtWidgets.QCheckBox(self.pages_group_box)
        self.browser_checkbox.setChecked(True)
        self.browser_checkbox.setObjectName("browser_checkbox")
        self.pages_vertical_layout.addWidget(self.browser_checkbox)
        self.overview_checkbox = QtWidgets.QCheckBox(self.pages_group_box)
        self.overview_checkbox.setChecked(True)
        self.overview_checkbox.setObjectName("overview_checkbox")
        self.pages_vertical_layout.addWidget(self.overview_checkbox)
        self.congrats_checkbox = QtWidgets.QCheckBox(self.pages_group_box)
        self.congrats_checkbox.setChecked(True)
        self.congrats_checkbox.setObjectName("congrats_checkbox")
        self.pages_vertical_layout.addWidget(self.congrats_checkbox)
        self.appearance_vert_layout.addWidget(self.pages_group_box)
        self.appearance_tab_layout.addLayout(self.appearance_vert_layout)
        self.tabs_widget.addTab(self.appearance_tab, "")
        self.decks_tab = QtWidgets.QWidget()
        self.decks_tab.setObjectName("decks_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.decks_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.excluded_decks_label = QtWidgets.QLabel(self.decks_tab)
        self.excluded_decks_label.setTextFormat(QtCore.Qt.RichText)
        self.excluded_decks_label.setObjectName("excluded_decks_label")
        self.verticalLayout.addWidget(self.excluded_decks_label)
        self.add_remove_layout = QtWidgets.QHBoxLayout()
        self.add_remove_layout.setContentsMargins(-1, 10, -1, 10)
        self.add_remove_layout.setObjectName("add_remove_layout")
        self.add_button = QtWidgets.QPushButton(self.decks_tab)
        self.add_button.setObjectName("add_button")
        self.add_remove_layout.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.decks_tab)
        self.remove_button.setObjectName("remove_button")
        self.add_remove_layout.addWidget(self.remove_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.add_remove_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.add_remove_layout)
        self.excluded_decks_list = QtWidgets.QListWidget(self.decks_tab)
        self.excluded_decks_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.excluded_decks_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.excluded_decks_list.setObjectName("excluded_decks_list")
        self.verticalLayout.addWidget(self.excluded_decks_list)
        self.tabs_widget.addTab(self.decks_tab, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.about_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.about_text = QtWidgets.QTextBrowser(self.about_tab)
        self.about_text.setObjectName("about_text")
        self.verticalLayout_2.addWidget(self.about_text)
        self.tabs_widget.addTab(self.about_tab, "")
        self.options_vert_layout.addWidget(self.tabs_widget)
        self.confirm_button_box = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.confirm_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.confirm_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.confirm_button_box.setObjectName("confirm_button_box")
        self.options_vert_layout.addWidget(self.confirm_button_box)

        self.retranslateUi(OptionsDialog)
        self.tabs_widget.setCurrentIndex(1)
        self.confirm_button_box.accepted.connect(OptionsDialog.accept)
        self.confirm_button_box.rejected.connect(OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Study TIme Stats Options"))
        self.primary_color_label.setText(_translate("OptionsDialog", "Primary Color"))
        self.seconday_color_button.setText(_translate("OptionsDialog", "Select"))
        self.total_label.setText(_translate("OptionsDialog", "Custom Total Text"))
        self.week_start_dropdown.setItemText(0, _translate("OptionsDialog", "Monday"))
        self.week_start_dropdown.setItemText(1, _translate("OptionsDialog", "Tuesday"))
        self.week_start_dropdown.setItemText(2, _translate("OptionsDialog", "Wednesday"))
        self.week_start_dropdown.setItemText(3, _translate("OptionsDialog", "Thursday"))
        self.week_start_dropdown.setItemText(4, _translate("OptionsDialog", "Friday"))
        self.week_start_dropdown.setItemText(5, _translate("OptionsDialog", "Saturday"))
        self.week_start_dropdown.setItemText(6, _translate("OptionsDialog", "Sunday"))
        self.primary_color_button.setText(_translate("OptionsDialog", "Select"))
        self.secondary_color_label.setText(_translate("OptionsDialog", "Secondary Color"))
        self.ranged_label.setText(_translate("OptionsDialog", "Custom Ranged Text"))
        self.week_start_label.setText(_translate("OptionsDialog", "Week-Start Day"))
        self.range_select_label.setText(_translate("OptionsDialog", "Selected Range"))
        self.custom_range_spinbox.setSuffix(_translate("OptionsDialog", " days"))
        self.range_select_dropdown.setItemText(0, _translate("OptionsDialog", "Past Week"))
        self.range_select_dropdown.setItemText(1, _translate("OptionsDialog", "Past 2 Weeks"))
        self.range_select_dropdown.setItemText(2, _translate("OptionsDialog", "Past Month"))
        self.range_select_dropdown.setItemText(3, _translate("OptionsDialog", "Past Year"))
        self.range_select_dropdown.setItemText(4, _translate("OptionsDialog", "Custom"))
        self.use_start_checkbox.setText(_translate("OptionsDialog", "From Week-Start"))
        self.pages_group_box.setTitle(_translate("OptionsDialog", "Pages"))
        self.browser_checkbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.overview_checkbox.setText(_translate("OptionsDialog", "Overview"))
        self.congrats_checkbox.setText(_translate("OptionsDialog", "Congrats Screen"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.appearance_tab), _translate("OptionsDialog", "Appearance"))
        self.excluded_decks_label.setText(_translate("OptionsDialog", "Excluded Decks"))
        self.add_button.setText(_translate("OptionsDialog", "Add..."))
        self.remove_button.setText(_translate("OptionsDialog", "Remove"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.decks_tab), _translate("OptionsDialog", "Decks"))
        self.about_text.setHtml(_translate("OptionsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">About page text. Lorem ipsum-thing go here.</p></body></html>"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.about_tab), _translate("OptionsDialog", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
