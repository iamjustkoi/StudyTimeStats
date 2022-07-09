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
        OptionsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        OptionsDialog.resize(508, 485)
        OptionsDialog.setMinimumSize(QtCore.QSize(484, 0))
        OptionsDialog.setModal(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(OptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs_widget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabs_widget.setObjectName("tabs_widget")
        self.appearance_tab = QtWidgets.QWidget()
        self.appearance_tab.setEnabled(True)
        self.appearance_tab.setObjectName("appearance_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.appearance_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.general_layout = QtWidgets.QVBoxLayout()
        self.general_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.general_layout.setContentsMargins(12, 12, 12, 12)
        self.general_layout.setObjectName("general_layout")
        self.general_form = QtWidgets.QFormLayout()
        self.general_form.setContentsMargins(-1, -1, -1, 20)
        self.general_form.setObjectName("general_form")
        self.range_select_label = QtWidgets.QLabel(self.appearance_tab)
        self.range_select_label.setObjectName("range_select_label")
        self.general_form.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.range_select_label)
        self.range_select_layout = QtWidgets.QHBoxLayout()
        self.range_select_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.range_select_layout.setObjectName("range_select_layout")
        self.range_select_dropdown = QtWidgets.QComboBox(self.appearance_tab)
        self.range_select_dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.range_select_dropdown.setObjectName("range_select_dropdown")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_dropdown.addItem("")
        self.range_select_layout.addWidget(self.range_select_dropdown)
        self.use_calendar_checkbox = QtWidgets.QCheckBox(self.appearance_tab)
        self.use_calendar_checkbox.setChecked(True)
        self.use_calendar_checkbox.setObjectName("use_calendar_checkbox")
        self.range_select_layout.addWidget(self.use_calendar_checkbox)
        self.range_select_layout.setStretch(0, 1)
        self.general_form.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.range_select_layout)
        self.week_start_label = QtWidgets.QLabel(self.appearance_tab)
        self.week_start_label.setObjectName("week_start_label")
        self.general_form.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.week_start_label)
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
        self.general_form.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.week_start_dropdown)
        self.custom_range_spinbox = QtWidgets.QSpinBox(self.appearance_tab)
        self.custom_range_spinbox.setMaximum(5690)
        self.custom_range_spinbox.setProperty("value", 14)
        self.custom_range_spinbox.setObjectName("custom_range_spinbox")
        self.general_form.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.custom_range_spinbox)
        self.total_label = QtWidgets.QLabel(self.appearance_tab)
        self.total_label.setObjectName("total_label")
        self.general_form.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.total_label)
        self.total_line = QtWidgets.QLineEdit(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_line.sizePolicy().hasHeightForWidth())
        self.total_line.setSizePolicy(sizePolicy)
        self.total_line.setObjectName("total_line")
        self.general_form.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.total_line)
        self.ranged_label = QtWidgets.QLabel(self.appearance_tab)
        self.ranged_label.setObjectName("ranged_label")
        self.general_form.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.ranged_label)
        self.ranged_line = QtWidgets.QLineEdit(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ranged_line.sizePolicy().hasHeightForWidth())
        self.ranged_line.setSizePolicy(sizePolicy)
        self.ranged_line.setObjectName("ranged_line")
        self.general_form.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.ranged_line)
        self.hrs_label = QtWidgets.QLabel(self.appearance_tab)
        self.hrs_label.setObjectName("hrs_label")
        self.general_form.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.hrs_label)
        self.hrs_line = QtWidgets.QLineEdit(self.appearance_tab)
        self.hrs_line.setObjectName("hrs_line")
        self.general_form.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.hrs_line)
        self.min_label = QtWidgets.QLabel(self.appearance_tab)
        self.min_label.setObjectName("min_label")
        self.general_form.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.min_label)
        self.min_line = QtWidgets.QLineEdit(self.appearance_tab)
        self.min_line.setObjectName("min_line")
        self.general_form.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.min_line)
        self.primary_color_label = QtWidgets.QLabel(self.appearance_tab)
        self.primary_color_label.setObjectName("primary_color_label")
        self.general_form.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.primary_color_label)
        self.primary_color_layout = QtWidgets.QHBoxLayout()
        self.primary_color_layout.setObjectName("primary_color_layout")
        self.primary_color_button = QtWidgets.QPushButton(self.appearance_tab)
        self.primary_color_button.setObjectName("primary_color_button")
        self.primary_color_layout.addWidget(self.primary_color_button)
        self.primary_color_preview = QtWidgets.QLabel(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.primary_color_preview.sizePolicy().hasHeightForWidth())
        self.primary_color_preview.setSizePolicy(sizePolicy)
        self.primary_color_preview.setMinimumSize(QtCore.QSize(20, 20))
        self.primary_color_preview.setObjectName("primary_color_preview")
        self.primary_color_layout.addWidget(self.primary_color_preview)
        self.general_form.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.primary_color_layout)
        self.secondary_color_label = QtWidgets.QLabel(self.appearance_tab)
        self.secondary_color_label.setObjectName("secondary_color_label")
        self.general_form.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.secondary_color_label)
        self.secondary_color_layut = QtWidgets.QHBoxLayout()
        self.secondary_color_layut.setObjectName("secondary_color_layut")
        self.seconday_color_button = QtWidgets.QPushButton(self.appearance_tab)
        self.seconday_color_button.setObjectName("seconday_color_button")
        self.secondary_color_layut.addWidget(self.seconday_color_button)
        self.secondary_color_preview = QtWidgets.QLabel(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.secondary_color_preview.sizePolicy().hasHeightForWidth())
        self.secondary_color_preview.setSizePolicy(sizePolicy)
        self.secondary_color_preview.setMinimumSize(QtCore.QSize(20, 20))
        self.secondary_color_preview.setObjectName("secondary_color_preview")
        self.secondary_color_layut.addWidget(self.secondary_color_preview)
        self.general_form.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.secondary_color_layut)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.show_total_checkbox = QtWidgets.QCheckBox(self.appearance_tab)
        self.show_total_checkbox.setChecked(True)
        self.show_total_checkbox.setObjectName("show_total_checkbox")
        self.horizontalLayout_2.addWidget(self.show_total_checkbox)
        self.show_ranged_checkbox = QtWidgets.QCheckBox(self.appearance_tab)
        self.show_ranged_checkbox.setChecked(True)
        self.show_ranged_checkbox.setObjectName("show_ranged_checkbox")
        self.horizontalLayout_2.addWidget(self.show_ranged_checkbox)
        self.general_form.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.general_form.setItem(11, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.general_layout.addLayout(self.general_form)
        self.pages_group = QtWidgets.QGroupBox(self.appearance_tab)
        self.pages_group.setObjectName("pages_group")
        self.pages_vertical_layout = QtWidgets.QHBoxLayout(self.pages_group)
        self.pages_vertical_layout.setObjectName("pages_vertical_layout")
        self.browser_checkbox = QtWidgets.QCheckBox(self.pages_group)
        self.browser_checkbox.setChecked(True)
        self.browser_checkbox.setObjectName("browser_checkbox")
        self.pages_vertical_layout.addWidget(self.browser_checkbox)
        self.overview_checkbox = QtWidgets.QCheckBox(self.pages_group)
        self.overview_checkbox.setChecked(True)
        self.overview_checkbox.setObjectName("overview_checkbox")
        self.pages_vertical_layout.addWidget(self.overview_checkbox)
        self.congrats_checkbox = QtWidgets.QCheckBox(self.pages_group)
        self.congrats_checkbox.setChecked(True)
        self.congrats_checkbox.setObjectName("congrats_checkbox")
        self.pages_vertical_layout.addWidget(self.congrats_checkbox)
        self.general_layout.addWidget(self.pages_group)
        self.verticalLayout_3.addLayout(self.general_layout)
        self.tabs_widget.addTab(self.appearance_tab, "")
        self.decks_tab = QtWidgets.QWidget()
        self.decks_tab.setObjectName("decks_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.decks_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolbar_checkbox = QtWidgets.QCheckBox(self.decks_tab)
        self.toolbar_checkbox.setChecked(True)
        self.toolbar_checkbox.setObjectName("toolbar_checkbox")
        self.verticalLayout.addWidget(self.toolbar_checkbox)
        self.include_deleted_checkbox = QtWidgets.QCheckBox(self.decks_tab)
        self.include_deleted_checkbox.setChecked(True)
        self.include_deleted_checkbox.setObjectName("include_deleted_checkbox")
        self.verticalLayout.addWidget(self.include_deleted_checkbox)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, -1, -1, 20)
        self.formLayout.setObjectName("formLayout")
        self.total_hrs_line = QtWidgets.QLineEdit(self.decks_tab)
        self.total_hrs_line.setObjectName("total_hrs_line")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.total_hrs_line)
        self.total_hrs_label = QtWidgets.QLabel(self.decks_tab)
        self.total_hrs_label.setObjectName("total_hrs_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.total_hrs_label)
        self.range_hrs_label = QtWidgets.QLabel(self.decks_tab)
        self.range_hrs_label.setObjectName("range_hrs_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.range_hrs_label)
        self.range_hrs_line = QtWidgets.QLineEdit(self.decks_tab)
        self.range_hrs_line.setObjectName("range_hrs_line")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.range_hrs_line)
        self.verticalLayout.addLayout(self.formLayout)
        self.enabled_decks_group = QtWidgets.QGroupBox(self.decks_tab)
        self.enabled_decks_group.setMinimumSize(QtCore.QSize(0, 100))
        self.enabled_decks_group.setObjectName("enabled_decks_group")
        self.enabled_decks_layout = QtWidgets.QVBoxLayout(self.enabled_decks_group)
        self.enabled_decks_layout.setObjectName("enabled_decks_layout")
        self.exclude_layout = QtWidgets.QHBoxLayout()
        self.exclude_layout.setObjectName("exclude_layout")
        self.deck_enable_button = QtWidgets.QPushButton(self.enabled_decks_group)
        self.deck_enable_button.setFocusPolicy(QtCore.Qt.TabFocus)
        self.deck_enable_button.setObjectName("deck_enable_button")
        self.exclude_layout.addWidget(self.deck_enable_button)
        self.deck_disable_button = QtWidgets.QPushButton(self.enabled_decks_group)
        self.deck_disable_button.setFocusPolicy(QtCore.Qt.TabFocus)
        self.deck_disable_button.setObjectName("deck_disable_button")
        self.exclude_layout.addWidget(self.deck_disable_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.exclude_layout.addItem(spacerItem1)
        self.enabled_decks_layout.addLayout(self.exclude_layout)
        self.excluded_decks_list = QtWidgets.QListWidget(self.enabled_decks_group)
        self.excluded_decks_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.excluded_decks_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.excluded_decks_list.setObjectName("excluded_decks_list")
        self.enabled_decks_layout.addWidget(self.excluded_decks_list)
        self.verticalLayout.addWidget(self.enabled_decks_group)
        self.tabs_widget.addTab(self.decks_tab, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.about_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll_area = QtWidgets.QScrollArea(self.about_tab)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.about_scroll = QtWidgets.QWidget()
        self.about_scroll.setGeometry(QtCore.QRect(0, 0, 449, 766))
        self.about_scroll.setObjectName("about_scroll")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.about_scroll)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setObjectName("scroll_layout")
        self.about_label_header = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_header.sizePolicy().hasHeightForWidth())
        self.about_label_header.setSizePolicy(sizePolicy)
        self.about_label_header.setTextFormat(QtCore.Qt.MarkdownText)
        self.about_label_header.setWordWrap(True)
        self.about_label_header.setObjectName("about_label_header")
        self.scroll_layout.addWidget(self.about_label_header)
        self.support_buttons = QtWidgets.QHBoxLayout()
        self.support_buttons.setContentsMargins(6, 6, 6, 6)
        self.support_buttons.setObjectName("support_buttons")
        self.like_button = QtWidgets.QPushButton(self.about_scroll)
        self.like_button.setMinimumSize(QtCore.QSize(0, 42))
        self.like_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.like_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.like_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.like_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("raw/anki_like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.like_button.setIcon(icon)
        self.like_button.setIconSize(QtCore.QSize(32, 32))
        self.like_button.setObjectName("like_button")
        self.support_buttons.addWidget(self.like_button)
        self.kofi_button = QtWidgets.QPushButton(self.about_scroll)
        self.kofi_button.setMinimumSize(QtCore.QSize(0, 42))
        self.kofi_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kofi_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.kofi_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.kofi_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("raw/kofilogo_blue.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kofi_button.setIcon(icon1)
        self.kofi_button.setIconSize(QtCore.QSize(32, 32))
        self.kofi_button.setObjectName("kofi_button")
        self.support_buttons.addWidget(self.kofi_button)
        self.patreon_button = QtWidgets.QPushButton(self.about_scroll)
        self.patreon_button.setMinimumSize(QtCore.QSize(0, 42))
        self.patreon_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.patreon_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.patreon_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.patreon_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("raw/patreon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patreon_button.setIcon(icon2)
        self.patreon_button.setIconSize(QtCore.QSize(32, 32))
        self.patreon_button.setObjectName("patreon_button")
        self.support_buttons.addWidget(self.patreon_button)
        self.scroll_layout.addLayout(self.support_buttons)
        self.about_label_body = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_body.sizePolicy().hasHeightForWidth())
        self.about_label_body.setSizePolicy(sizePolicy)
        self.about_label_body.setTextFormat(QtCore.Qt.MarkdownText)
        self.about_label_body.setWordWrap(True)
        self.about_label_body.setObjectName("about_label_body")
        self.scroll_layout.addWidget(self.about_label_body)
        self.scroll_layout.setStretch(2, 1)
        self.scroll_area.setWidget(self.about_scroll)
        self.verticalLayout_2.addWidget(self.scroll_area)
        self.tabs_widget.addTab(self.about_tab, "")
        self.verticalLayout_4.addWidget(self.tabs_widget)
        self.confirm_button_box = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.confirm_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.confirm_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.confirm_button_box.setObjectName("confirm_button_box")
        self.verticalLayout_4.addWidget(self.confirm_button_box)

        self.retranslateUi(OptionsDialog)
        self.tabs_widget.setCurrentIndex(2)
        self.confirm_button_box.accepted.connect(OptionsDialog.accept)
        self.confirm_button_box.rejected.connect(OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Study Time Stats Options"))
        self.range_select_label.setText(_translate("OptionsDialog", "Selected Range"))
        self.range_select_dropdown.setToolTip(_translate("OptionsDialog", "Time range to filter through for the ranged total stat."))
        self.range_select_dropdown.setItemText(0, _translate("OptionsDialog", "Past Week"))
        self.range_select_dropdown.setItemText(1, _translate("OptionsDialog", "Past 2 Weeks"))
        self.range_select_dropdown.setItemText(2, _translate("OptionsDialog", "Past Month"))
        self.range_select_dropdown.setItemText(3, _translate("OptionsDialog", "Past Year"))
        self.range_select_dropdown.setItemText(4, _translate("OptionsDialog", "Custom"))
        self.use_calendar_checkbox.setToolTip(_translate("OptionsDialog", "Use the start of the selected range instead of using its timespan."))
        self.use_calendar_checkbox.setText(_translate("OptionsDialog", "Use Calendar Week"))
        self.week_start_label.setText(_translate("OptionsDialog", "Week-Start Day"))
        self.week_start_dropdown.setToolTip(_translate("OptionsDialog", "The day a new week should start on."))
        self.week_start_dropdown.setItemText(0, _translate("OptionsDialog", "Monday"))
        self.week_start_dropdown.setItemText(1, _translate("OptionsDialog", "Tuesday"))
        self.week_start_dropdown.setItemText(2, _translate("OptionsDialog", "Wednesday"))
        self.week_start_dropdown.setItemText(3, _translate("OptionsDialog", "Thursday"))
        self.week_start_dropdown.setItemText(4, _translate("OptionsDialog", "Friday"))
        self.week_start_dropdown.setItemText(5, _translate("OptionsDialog", "Saturday"))
        self.week_start_dropdown.setItemText(6, _translate("OptionsDialog", "Sunday"))
        self.custom_range_spinbox.setToolTip(_translate("OptionsDialog", "Amount of days to filter the custom range."))
        self.custom_range_spinbox.setSuffix(_translate("OptionsDialog", " days"))
        self.total_label.setText(_translate("OptionsDialog", "Total Title"))
        self.total_line.setToolTip(_translate("OptionsDialog", "Text that displays above the total statistic."))
        self.ranged_label.setText(_translate("OptionsDialog", "Range Title"))
        self.ranged_line.setToolTip(_translate("OptionsDialog", "Text that displays above the ranged statistic."))
        self.hrs_label.setText(_translate("OptionsDialog", "Hours Label"))
        self.hrs_line.setToolTip(_translate("OptionsDialog", "Unit text appended to hours."))
        self.min_label.setText(_translate("OptionsDialog", "Minutes Label"))
        self.min_line.setToolTip(_translate("OptionsDialog", "Unit text appended to minutes."))
        self.primary_color_label.setText(_translate("OptionsDialog", "Primary Color"))
        self.primary_color_button.setText(_translate("OptionsDialog", "Select"))
        self.secondary_color_label.setText(_translate("OptionsDialog", "Secondary Color"))
        self.seconday_color_button.setText(_translate("OptionsDialog", "Select"))
        self.show_total_checkbox.setToolTip(_translate("OptionsDialog", "Enables the total stat."))
        self.show_total_checkbox.setText(_translate("OptionsDialog", "Show Total Stat"))
        self.show_ranged_checkbox.setToolTip(_translate("OptionsDialog", "Enables the ranged stat."))
        self.show_ranged_checkbox.setText(_translate("OptionsDialog", "Show Range Stat"))
        self.pages_group.setTitle(_translate("OptionsDialog", "Enabled Pages"))
        self.browser_checkbox.setToolTip(_translate("OptionsDialog", "The main Anki screen for browsing decks."))
        self.browser_checkbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.overview_checkbox.setToolTip(_translate("OptionsDialog", "The screen that shows when viewing a deck."))
        self.overview_checkbox.setText(_translate("OptionsDialog", "Overview"))
        self.congrats_checkbox.setToolTip(_translate("OptionsDialog", "The screen that shows up on the Deck Overview when all reviews are finished for the day."))
        self.congrats_checkbox.setText(_translate("OptionsDialog", "Congrats Screen"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.appearance_tab), _translate("OptionsDialog", "General"))
        self.toolbar_checkbox.setToolTip(_translate("OptionsDialog", "Enables the Tools Menu shortcut for showing these options. \n"
"This window can also be opened in the Add-ons menu using the Config button."))
        self.toolbar_checkbox.setText(_translate("OptionsDialog", "Show options shortcut in the Tools Menu"))
        self.include_deleted_checkbox.setToolTip(_translate("OptionsDialog", "Include review times from cards that were deleted."))
        self.include_deleted_checkbox.setText(_translate("OptionsDialog", "Include reviews from deleted cards"))
        self.total_hrs_line.setToolTip(_translate("OptionsDialog", "Custom output filter to use for the total statistics value.\n"
"See: About -> Text Macros"))
        self.total_hrs_label.setText(_translate("OptionsDialog", "Total Text Output"))
        self.range_hrs_label.setText(_translate("OptionsDialog", "Range Text Output"))
        self.range_hrs_line.setToolTip(_translate("OptionsDialog", "Custom output filter to use for the ranged statistics value.\n"
"See: About -> Text Macros"))
        self.enabled_decks_group.setTitle(_translate("OptionsDialog", "Enabled Decks"))
        self.deck_enable_button.setToolTip(_translate("OptionsDialog", "Enable stats for the selected deck(s)."))
        self.deck_enable_button.setText(_translate("OptionsDialog", "Enable"))
        self.deck_disable_button.setToolTip(_translate("OptionsDialog", "Disable stats for the selected deck(s)."))
        self.deck_disable_button.setText(_translate("OptionsDialog", "Disable"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.decks_tab), _translate("OptionsDialog", "Advanced"))
        self.about_label_header.setText(_translate("OptionsDialog", "## Study Time Stats\n"
"Add some customizable total and ranged study time statistics to Anki\'s main window!  \n"
"\n"
"Version: {version}  \n"
"Have any issues or feedback? Feel free to post on the project\'s issue section on [GitHub](https://github.com/iamjustkoi/StudyTimeStats/issues)!  \n"
"\n"
"[Releases/Changelog](https://github.com/iamjustkoi/StudyTimeStats/releases)  \n"
"[Source Code](https://github.com/iamjustkoi/StudyTimeStats)\n"
"<br></br>  \n"
"If you like the add-on and want to consider supporting my stuff:  \n"
""))
        self.like_button.setText(_translate("OptionsDialog", "Review on AnkiWeb "))
        self.kofi_button.setText(_translate("OptionsDialog", "  Buy me a coffee "))
        self.patreon_button.setText(_translate("OptionsDialog", "  Become a patron "))
        self.about_label_body.setText(_translate("OptionsDialog", "### Text Macros\n"
"The add-on can also filter text in the custom labels input to show information based on what\'s set in the config (e.g. \"Past %range\" to \"Past Week\"). These can be used multiple times and will update whenever Anki\'s main window reloads.\n"
"\n"
"### Available Macros:\n"
"\n"
"##### General\n"
"+ `%range` - the currently selected range format (Week, 2 Weeks, Month, Year)\n"
"+ `%from_date` - range filter\'s start date using the system\'s locale (2022-06-30)\n"
"+ `%from_day` - range filter\'s starting day using a compact format (Sun)\n"
"+ `%from_full_day` - range filter\'s full start day (Sunday)\n"
"+ `%from_month` - range filter\'s month name using a compact format (Sep)\n"
"+ `%from_full_month` - range filter\'s full month name (September)\n"
"+ `%days` - total days the range filter checks against (17)\n"
"<br></br>\n"
"##### Advanced\n"
"These macros will each index the received review logs and output its individual value-unit combination (e.g. \"%total_hrs\" -> \"3.14 hrs\").\n"
"+ `%total_hrs` - total study time\n"
"+ `%range_hrs` - ranged study time\n"
"+ `%last_cal_hrs` - total study time of the last calendar range\n"
"+ `%last_day_hrs` - total study time of the previous day\n"
"<br></br>\n"
"##### Misc\n"
"+ `%%` - returns a single % symbol and doesn\'t apply the text macro (%, %range, etc)\n"
"\n"
"<br></br>\n"
"Thanks for downloading and hope you enjoy!  \n"
"-koi  \n"
"<br></br>  \n"
"MIT Liecense  \n"
"©2022 JustKoi (iamjustkoi)  "))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.about_tab), _translate("OptionsDialog", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
