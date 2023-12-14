# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        OptionsDialog.resize(517, 620)
        OptionsDialog.setSizeGripEnabled(True)
        OptionsDialog.setModal(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(OptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs_widget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabs_widget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs_widget.sizePolicy().hasHeightForWidth())
        self.tabs_widget.setSizePolicy(sizePolicy)
        self.tabs_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabs_widget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabs_widget.setObjectName("tabs_widget")
        self.appearance_tab = QtWidgets.QWidget()
        self.appearance_tab.setEnabled(True)
        self.appearance_tab.setObjectName("appearance_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.appearance_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.appearance_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pages_group = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages_group.sizePolicy().hasHeightForWidth())
        self.pages_group.setSizePolicy(sizePolicy)
        self.pages_group.setObjectName("pages_group")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.pages_group)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browser_checkbox = QtWidgets.QCheckBox(self.pages_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browser_checkbox.sizePolicy().hasHeightForWidth())
        self.browser_checkbox.setSizePolicy(sizePolicy)
        self.browser_checkbox.setChecked(True)
        self.browser_checkbox.setObjectName("browser_checkbox")
        self.horizontalLayout.addWidget(self.browser_checkbox)
        self.overview_checkbox = QtWidgets.QCheckBox(self.pages_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overview_checkbox.sizePolicy().hasHeightForWidth())
        self.overview_checkbox.setSizePolicy(sizePolicy)
        self.overview_checkbox.setChecked(True)
        self.overview_checkbox.setObjectName("overview_checkbox")
        self.horizontalLayout.addWidget(self.overview_checkbox)
        self.congrats_checkbox = QtWidgets.QCheckBox(self.pages_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.congrats_checkbox.sizePolicy().hasHeightForWidth())
        self.congrats_checkbox.setSizePolicy(sizePolicy)
        self.congrats_checkbox.setChecked(True)
        self.congrats_checkbox.setObjectName("congrats_checkbox")
        self.horizontalLayout.addWidget(self.congrats_checkbox)
        self.verticalLayout_8.addWidget(self.pages_group)
        self.mainViewGroupbox = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainViewGroupbox.sizePolicy().hasHeightForWidth())
        self.mainViewGroupbox.setSizePolicy(sizePolicy)
        self.mainViewGroupbox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
            )
        self.mainViewGroupbox.setObjectName("mainViewGroupbox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.mainViewGroupbox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cellListWidget = QtWidgets.QListWidget(self.mainViewGroupbox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cellListWidget.sizePolicy().hasHeightForWidth())
        self.cellListWidget.setSizePolicy(sizePolicy)
        self.cellListWidget.setMinimumSize(QtCore.QSize(0, 64))
        self.cellListWidget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.cellListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cellListWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.cellListWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cellListWidget.setProperty("showDropIndicator", False)
        self.cellListWidget.setDragEnabled(True)
        self.cellListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.cellListWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.cellListWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cellListWidget.setObjectName("cellListWidget")
        self.verticalLayout_5.addWidget(self.cellListWidget)
        self.verticalLayout_8.addWidget(self.mainViewGroupbox)
        self.verticalLayout_3.addWidget(self.frame)
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
        self.useRolloverCheckbox = QtWidgets.QCheckBox(self.decks_tab)
        self.useRolloverCheckbox.setChecked(True)
        self.useRolloverCheckbox.setObjectName("useRolloverCheckbox")
        self.verticalLayout.addWidget(self.useRolloverCheckbox)
        self.useDecimalCheckbox = QtWidgets.QCheckBox(self.decks_tab)
        self.useDecimalCheckbox.setChecked(True)
        self.useDecimalCheckbox.setObjectName("useDecimalCheckbox")
        self.verticalLayout.addWidget(self.useDecimalCheckbox)
        self.enabled_decks_group = QtWidgets.QGroupBox(self.decks_tab)
        self.enabled_decks_group.setMinimumSize(QtCore.QSize(0, 100))
        self.enabled_decks_group.setObjectName("enabled_decks_group")
        self.enabled_decks_layout = QtWidgets.QVBoxLayout(self.enabled_decks_group)
        self.enabled_decks_layout.setObjectName("enabled_decks_layout")
        self.exclude_layout = QtWidgets.QHBoxLayout()
        self.exclude_layout.setObjectName("exclude_layout")
        self.deck_enable_button = QtWidgets.QPushButton(self.enabled_decks_group)
        self.deck_enable_button.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.deck_enable_button.setObjectName("deck_enable_button")
        self.exclude_layout.addWidget(self.deck_enable_button)
        self.deck_disable_button = QtWidgets.QPushButton(self.enabled_decks_group)
        self.deck_disable_button.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.deck_disable_button.setObjectName("deck_disable_button")
        self.exclude_layout.addWidget(self.deck_disable_button)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.exclude_layout.addItem(spacerItem)
        self.enabled_decks_layout.addLayout(self.exclude_layout)
        self.excluded_decks_list = QtWidgets.QListWidget(self.enabled_decks_group)
        self.excluded_decks_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.excluded_decks_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.excluded_decks_list.setObjectName("excluded_decks_list")
        self.enabled_decks_layout.addWidget(self.excluded_decks_list)
        self.verticalLayout.addWidget(self.enabled_decks_group)
        self.tabs_widget.addTab(self.decks_tab, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.about_tab)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll_area = QtWidgets.QScrollArea(self.about_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.about_scroll = QtWidgets.QWidget()
        self.about_scroll.setGeometry(QtCore.QRect(0, 0, 456, 555))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_scroll.sizePolicy().hasHeightForWidth())
        self.about_scroll.setSizePolicy(sizePolicy)
        self.about_scroll.setObjectName("about_scroll")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.about_scroll)
        self.scroll_layout.setObjectName("scroll_layout")
        self.about_label_header = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_header.sizePolicy().hasHeightForWidth())
        self.about_label_header.setSizePolicy(sizePolicy)
        self.about_label_header.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.about_label_header.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
            )
        self.about_label_header.setWordWrap(True)
        self.about_label_header.setOpenExternalLinks(True)
        self.about_label_header.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse | QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
            | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard |
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.about_label_header.setObjectName("about_label_header")
        self.scroll_layout.addWidget(self.about_label_header)
        self.supportButtonHolder = QtWidgets.QFrame(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.supportButtonHolder.sizePolicy().hasHeightForWidth())
        self.supportButtonHolder.setSizePolicy(sizePolicy)
        self.supportButtonHolder.setObjectName("supportButtonHolder")
        self.support_buttons = QtWidgets.QHBoxLayout(self.supportButtonHolder)
        self.support_buttons.setContentsMargins(6, 6, 6, 6)
        self.support_buttons.setObjectName("support_buttons")
        self.like_button = QtWidgets.QPushButton(self.supportButtonHolder)
        self.like_button.setMinimumSize(QtCore.QSize(0, 42))
        self.like_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.like_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.like_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.like_button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/img/anki_like.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.like_button.setIcon(icon)
        self.like_button.setIconSize(QtCore.QSize(32, 32))
        self.like_button.setObjectName("like_button")
        self.support_buttons.addWidget(self.like_button)
        self.patreon_button = QtWidgets.QPushButton(self.supportButtonHolder)
        self.patreon_button.setMinimumSize(QtCore.QSize(0, 42))
        self.patreon_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.patreon_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.patreon_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.patreon_button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/img/patreon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.patreon_button.setIcon(icon1)
        self.patreon_button.setIconSize(QtCore.QSize(32, 32))
        self.patreon_button.setObjectName("patreon_button")
        self.support_buttons.addWidget(self.patreon_button)
        self.kofi_button = QtWidgets.QPushButton(self.supportButtonHolder)
        self.kofi_button.setMinimumSize(QtCore.QSize(0, 42))
        self.kofi_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kofi_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.kofi_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.kofi_button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("res/img/kofilogo_blue.PNG"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.kofi_button.setIcon(icon2)
        self.kofi_button.setIconSize(QtCore.QSize(32, 32))
        self.kofi_button.setObjectName("kofi_button")
        self.support_buttons.addWidget(self.kofi_button)
        self.scroll_layout.addWidget(self.supportButtonHolder)
        self.about_label_body = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_body.sizePolicy().hasHeightForWidth())
        self.about_label_body.setSizePolicy(sizePolicy)
        self.about_label_body.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.about_label_body.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
            )
        self.about_label_body.setWordWrap(True)
        self.about_label_body.setOpenExternalLinks(True)
        self.about_label_body.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse | QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
            | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard | QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.about_label_body.setObjectName("about_label_body")
        self.scroll_layout.addWidget(self.about_label_body)
        self.scroll_area.setWidget(self.about_scroll)
        self.verticalLayout_2.addWidget(self.scroll_area)
        self.tabs_widget.addTab(self.about_tab, "")
        self.verticalLayout_4.addWidget(self.tabs_widget)
        self.frame_2 = QtWidgets.QFrame(OptionsDialog)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.confirm_button_box = QtWidgets.QDialogButtonBox(self.frame_2)
        self.confirm_button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.confirm_button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Apply | QtWidgets.QDialogButtonBox.StandardButton.Cancel |
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults
        )
        self.confirm_button_box.setObjectName("confirm_button_box")
        self.horizontalLayout_2.addWidget(self.confirm_button_box)
        self.supportButton = HoverButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.supportButton.sizePolicy().hasHeightForWidth())
        self.supportButton.setSizePolicy(sizePolicy)
        self.supportButton.setObjectName("supportButton")
        self.horizontalLayout_2.addWidget(self.supportButton)
        self.verticalLayout_4.addWidget(self.frame_2)

        self.retranslateUi(OptionsDialog)
        self.tabs_widget.setCurrentIndex(0)
        self.confirm_button_box.accepted.connect(OptionsDialog.accept)  # type: ignore
        self.confirm_button_box.rejected.connect(OptionsDialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Study Time Stats Options"))
        self.pages_group.setTitle(_translate("OptionsDialog", "Enabled Pages"))
        self.browser_checkbox.setToolTip(_translate("OptionsDialog", "The main page for browsing decks."))
        self.browser_checkbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.overview_checkbox.setToolTip(_translate("OptionsDialog", "The page that shows when viewing a deck."))
        self.overview_checkbox.setText(_translate("OptionsDialog", "Overview"))
        self.congrats_checkbox.setToolTip(
            _translate(
                "OptionsDialog",
                "The page that shows when viewing a deck that has its reviews done for the day."
            )
        )
        self.congrats_checkbox.setText(_translate("OptionsDialog", "Congrats"))
        self.mainViewGroupbox.setTitle(_translate("OptionsDialog", "Stats View"))
        self.cellListWidget.setSortingEnabled(True)
        self.tabs_widget.setTabText(
            self.tabs_widget.indexOf(self.appearance_tab),
            _translate("OptionsDialog", "General")
        )
        self.toolbar_checkbox.setToolTip(
            _translate(
                "OptionsDialog", "Enable the Tools Menu shortcut for these options. \n"
                                 "(Can also be accessed via Tools>Add-ons>Study Time Stats>Config)"
            )
        )
        self.toolbar_checkbox.setText(_translate("OptionsDialog", "Show options shortcut in the Tools Menu"))
        self.include_deleted_checkbox.setToolTip(
            _translate("OptionsDialog", "Include review/time stats for cards that\'ve been deleted.")
        )
        self.include_deleted_checkbox.setText(_translate("OptionsDialog", "Include reviews from deleted cards"))
        self.useRolloverCheckbox.setToolTip(
            _translate(
                "OptionsDialog",
                "Use Anki\'s rollover (next-day) hour when considering the time days are cut off."
            )
        )
        self.useRolloverCheckbox.setText(
            _translate("OptionsDialog", "Use the next-day hour when calculating ranged times")
        )
        self.useDecimalCheckbox.setToolTip(
            _translate(
                "OptionsDialog", "Shows an \"hour.min\" format for all time outputs. \n"
                                 "(Otherwise uses \"hh:mm\")"
            )
        )
        self.useDecimalCheckbox.setText(_translate("OptionsDialog", "Use decimal format time outputs"))
        self.enabled_decks_group.setTitle(_translate("OptionsDialog", "Enabled Decks"))
        self.deck_enable_button.setToolTip(_translate("OptionsDialog", "Enable stats for the selected deck(s)."))
        self.deck_enable_button.setText(_translate("OptionsDialog", "Enable"))
        self.deck_disable_button.setToolTip(_translate("OptionsDialog", "Disable stats for the selected deck(s)."))
        self.deck_disable_button.setText(_translate("OptionsDialog", "Disable"))
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.decks_tab), _translate("OptionsDialog", "Advanced"))
        self.about_label_header.setText(
            _translate(
                "OptionsDialog", "## <p align=\"center\">Study Time Stats<img src=\"{img_path}\"></p>\n"
                                 "Adds a total and ranged study time statistic to Anki\'s main window.  \n"
                                 "\n"
                                 "Version: {version}  \n"
                                 "Have any issues or feedback? Feel free to post on the project\'s issue section on ["
                                 "GitHub](https://github.com/iamjustkoi/StudyTimeStats/issues)!  \n"
                                 "\n"
                                 "[Releases/Changelog](https://github.com/iamjustkoi/StudyTimeStats/releases)  \n"
                                 "[Source Code](https://github.com/iamjustkoi/StudyTimeStats)  \n"
                                 "\n"
                                 "If you like the add-on and want to consider supporting me in anyway:"
            )
        )
        self.like_button.setToolTip(_translate("OptionsDialog", "Leave a review over at AnkiWeb!"))
        self.like_button.setText(_translate("OptionsDialog", "AnkiWeb "))
        self.patreon_button.setToolTip(_translate("OptionsDialog", "Follow/support me on Patreon!"))
        self.patreon_button.setText(_translate("OptionsDialog", " Patreon "))
        self.kofi_button.setToolTip(_translate("OptionsDialog", "Buy me a coffee with Ko-Fi!"))
        self.kofi_button.setText(_translate("OptionsDialog", "Ko-Fi"))
        self.about_label_body.setText(
            _translate(
                "OptionsDialog", "Every bit helps and is greatly appreciated! <3\n"
                                 "\n"
                                 "### Text Macros\n"
                                 "All output text can also be filtered to show some more customized information (e.g. "
                                 "\"Past %range\" to \"Past Week\"). These can be used multiple times and will update "
                                 "whenever Anki\'s main window reloads. \n"
                                 "\n"
                                 "`%%` - can be used to return a single % symbol and disable filtering for any macro "
                                 "text (e.g. `%%` -> %, `%%range` -> %range)\n"
                                 "\n"
                                 "*Small warning: as a general rule, the more stats used/the larger the range of the "
                                 "stat, the longer it might take to load them all (some caching is also done on the "
                                 "side, too though).\n"
                                 "\n"
                                 "<br></br>\n"
                                 "<br></br>\n"
                                 "Thanks for downloading and hope you enjoy!\n"
                                 "\n"
                                 "-koi \n"
                                 "\n"
                                 "\n"
                                 "<br></br>\n"
                                 "<br></br>\n"
                                 "MIT License \n"
                                 "\n"
                                 "©2022-2023 JustKoi (iamjustkoi)"
            )
        )
        self.tabs_widget.setTabText(self.tabs_widget.indexOf(self.about_tab), _translate("OptionsDialog", "About"))
        self.supportButton.setText(_translate("OptionsDialog", "<3"))


from res.ui.forms import HoverButton

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
