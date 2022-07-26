"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in the "LICENSE" file, packaged with the add-on.
"""
from __future__ import annotations

import webbrowser
from pathlib import Path

import aqt
from aqt.qt import QDialog, QColorDialog, QColor, QLabel, QDialogButtonBox, QRect, QIcon, QMenu
from aqt.qt import QListWidgetItem, QWidget, QHBoxLayout

from .config import TimeStatsConfigManager
from .consts import *
from ..res.ui.options_dialog import Ui_OptionsDialog


def set_label_background(label: QLabel, hex_arg: str, use_circle=True):
    if use_circle:
        label.setStyleSheet(f'QWidget {{background-color: {hex_arg}; border-radius: 10px;}}')
    else:
        label.setStyleSheet(f'QWidget {{background-color: {hex_arg}}}')


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        """
Addon options QDialog class for accessing and changing the addon's config values.
        :param conf_manager: TimeStatsConfigManager used to reading and writing user input.
        """
        super().__init__(flags=conf_manager.mw.windowFlags())
        self.manager = conf_manager
        self.config = conf_manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.setWindowIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{ICON_PATH}'))

        self._primary_color = self.config[Config.PRIMARY_COLOR]
        self._secondary_color = self.config[Config.SECONDARY_COLOR]

        # Deck list items
        self.ui.deck_enable_button.released.connect(lambda: self.set_selected_enabled(True))
        self.ui.deck_disable_button.released.connect(lambda: self.set_selected_enabled(False))
        self.ui.excluded_decks_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.ui.excluded_decks_list.setSortingEnabled(True)

        # About page buttons
        self.ui.context_menu = QMenu(self)

        kofi_button = self.ui.kofi_button
        kofi_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{KOFI_ICON_PATH}'))
        kofi_button.released.connect(lambda: webbrowser.open(KOFI_URL))
        kofi_button.customContextMenuRequested.connect(
            lambda point: self.on_line_context_menu(point, kofi_button)
        )

        patreon_button = self.ui.patreon_button
        patreon_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{PATREON_ICON_PATH}'))
        patreon_button.released.connect(lambda: webbrowser.open(PATREON_URL))
        patreon_button.customContextMenuRequested.connect(
            lambda point: self.on_line_context_menu(point, patreon_button)
        )

        ankiweb_button = self.ui.like_button
        ankiweb_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{ANKI_LIKE_ICON_PATH}'))
        ankiweb_button.released.connect(lambda: webbrowser.open(ANKI_URL))
        ankiweb_button.customContextMenuRequested.connect(
            lambda point: self.on_line_context_menu(point, ankiweb_button)
        )

        # Restore Defaults Button
        self.ui.confirm_button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.on_restore_defaults)

        # Color Select Button
        self.ui.primary_color_button.clicked.connect(lambda: self.open_color_dialog(self.ui.primary_color_preview))
        self.ui.seconday_color_button.clicked.connect(lambda: self.open_color_dialog(self.ui.secondary_color_preview))

        # Range Button
        self.ui.range_select_dropdown.activated[int].connect(self.on_range_type_change)
        self.ui.use_calendar_checkbox.clicked.connect(self.update_calendar_range_extras)

        # Update the position of the custom spinbox to the same position as the calendar checkbox
        self.ui.range_select_layout.layout().replaceWidget(self.ui.use_calendar_checkbox, self.ui.custom_range_spinbox)

        # Update custom range's max value
        self.ui.custom_range_spinbox.setMaximum(self.manager.max_range)

        # Update about header text with the current version number
        updated_about_header = self.ui.about_label_header.text().format(version=CURRENT_VERSION)
        self.ui.about_label_header.setText(updated_about_header)

        # Setting current index again to overwrite QTDesigner's auto-setting, just in case
        self.ui.tabs_widget.setCurrentIndex(0)
        self._load()

    def _load(self):
        """
Loads all config values to the options dialog.
        """
        self.ui.toolbar_checkbox.setChecked(self.config[Config.TOOLBAR_ENABLED])

        self.ui.week_start_dropdown.setCurrentIndex(self.config[Config.WEEK_START])

        self.ui.range_select_dropdown.setCurrentIndex(self.config[Config.RANGE_TYPE])
        self.on_range_type_change(self.ui.range_select_dropdown.currentIndex())

        self.ui.use_calendar_checkbox.setChecked(self.config[Config.USE_CALENDAR_RANGE])
        self.update_calendar_range_extras()

        self.ui.show_total_checkbox.setChecked(self.config[Config.SHOW_TOTAL])
        self.ui.show_ranged_checkbox.setChecked(self.config[Config.SHOW_RANGED])

        self.ui.custom_range_spinbox.setValue(self.config[Config.CUSTOM_DAYS])
        self.ui.total_line.setText(self.config[Config.CUSTOM_TOTAL_TEXT])
        self.ui.ranged_line.setText(self.config[Config.CUSTOM_RANGE_TEXT])
        self.ui.hrs_line.setText(self.config[Config.CUSTOM_HRS_TEXT])
        self.ui.min_line.setText(self.config[Config.CUSTOM_MIN_TEXT])
        self.ui.total_hrs_line.setText(self.config[Config.CUSTOM_TOTAL_HRS])
        self.ui.range_hrs_line.setText(self.config[Config.CUSTOM_RANGE_HRS])

        # Color Pickers
        set_label_background(self.ui.primary_color_preview, self.config[Config.PRIMARY_COLOR])
        self._primary_color = self.config[Config.PRIMARY_COLOR]
        set_label_background(self.ui.secondary_color_preview, self.config[Config.SECONDARY_COLOR])
        self._secondary_color = self.config[Config.SECONDARY_COLOR]

        self.ui.browser_checkbox.setChecked(self.config[Config.BROWSER_ENABLED])
        self.ui.overview_checkbox.setChecked(self.config[Config.OVERVIEW_ENABLED])
        self.ui.congrats_checkbox.setChecked(self.config[Config.CONGRATS_ENABLED])

        self.ui.include_deleted_checkbox.setChecked(self.config[Config.INCLUDE_DELETED])

        # Excluded Decks
        self._load_excluded_decks()

    def _save(self):
        """
Retrieves values from options dialog window, updates/writes the values to the current config, then resets the main
window to update all the ui.
        """
        # Store options
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolbar_checkbox.isChecked()
        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config[Config.RANGE_TYPE] = self.ui.range_select_dropdown.currentIndex()
        self.config[Config.USE_CALENDAR_RANGE] = self.ui.use_calendar_checkbox.isChecked()
        self.config[Config.SHOW_TOTAL] = self.ui.show_total_checkbox.isChecked()
        self.config[Config.SHOW_RANGED] = self.ui.show_ranged_checkbox.isChecked()
        self.config[Config.CUSTOM_DAYS] = self.ui.custom_range_spinbox.value()
        self.config[Config.CUSTOM_TOTAL_TEXT] = self.ui.total_line.text()
        self.config[Config.CUSTOM_RANGE_TEXT] = self.ui.ranged_line.text()
        self.config[Config.CUSTOM_TOTAL_HRS] = self.ui.total_hrs_line.text()
        self.config[Config.CUSTOM_RANGE_HRS] = self.ui.range_hrs_line.text()
        self.config[Config.CUSTOM_HRS_TEXT] = self.ui.hrs_line.text()
        self.config[Config.CUSTOM_MIN_TEXT] = self.ui.min_line.text()

        # Store colors with saved hex info
        self.config[Config.PRIMARY_COLOR] = self._primary_color
        self.config[Config.SECONDARY_COLOR] = self._secondary_color

        self.config[Config.BROWSER_ENABLED] = self.ui.browser_checkbox.isChecked()
        self.config[Config.OVERVIEW_ENABLED] = self.ui.overview_checkbox.isChecked()
        self.config[Config.CONGRATS_ENABLED] = self.ui.congrats_checkbox.isChecked()

        self.config[Config.INCLUDE_DELETED] = self.ui.include_deleted_checkbox.isChecked()

        self.config[Config.EXCLUDED_DIDS] = self._get_excluded_dids()

        self.manager.write_config()
        self.manager.mw.reset()

    def _load_excluded_decks(self):
        """
Loads deck names to list and sets label to enabled if not in current config's excluded decks.
        """
        self.excluded_deck_names = [self.manager.decks.name(i) for i in self.config.get(Config.EXCLUDED_DIDS)]
        decks_list = self.ui.excluded_decks_list
        decks_list.clear()

        for deck in self.manager.mw.col.decks.all_names_and_ids():
            deck_item = DeckItem(deck.name, self)
            deck_item.set_included(deck_item.label.text() not in self.excluded_deck_names)

            list_item = DeckListItem(decks_list)
            # list_item.__lt__ = lambda
            list_item.setSizeHint(deck_item.sizeHint())

            decks_list.addItem(list_item)
            decks_list.setItemWidget(list_item, deck_item)

        decks_list.sortItems()

    def _get_excluded_dids(self):
        """
Retrieves currently excluded deck id's.
        :return: a list containing all excluded deck id's as integers.
        """
        dids = []
        for i in range(self.ui.excluded_decks_list.count()):
            item = self.ui.excluded_decks_list.item(i)
            deck_item = DeckItem.from_list_widget(self, item)
            if not deck_item.is_included():
                dids.append(self.manager.decks.id(deck_item.label.text(), create=False))
        return dids

    def _redraw_calendar_checkbox(self):
        """
Redraws the calendar date checkbox using the updated label's width.
        """
        width = self.ui.use_calendar_checkbox.width()
        height = self.ui.use_calendar_checkbox.height()
        x = self.ui.use_calendar_checkbox.pos().x()
        y = self.ui.use_calendar_checkbox.pos().y()

        self.ui.use_calendar_checkbox.setGeometry(QRect(x, y, width, height))

    def accept(self) -> None:
        """
Saves all user config values and closes the window.
        """
        self._save()
        self.close()

    def set_selected_enabled(self, should_enable: bool):
        for item in self.ui.excluded_decks_list.selectedItems():
            deck_item = DeckItem.from_list_widget(self, item)
            deck_item.set_included(should_enable)
            # self.on_selection_change()

    def on_item_double_clicked(self, item: QListWidgetItem):
        self.set_selected_enabled(not DeckItem.from_list_widget(self, item).is_included())
        # self.set_selected_enabled()
        pass

    def on_line_context_menu(self, point, button):
        """
Handles context menu actions for the input button.
        :param point: input coordinate to display the menu
        :param button: button being clicked/triggered
        """
        self.ui.context_menu = QMenu(self)
        self.ui.context_menu.addAction(String.COPY_LINK_ACTION).triggered.connect(lambda: self.on_copy_link(button))
        self.ui.context_menu.exec(button.mapToGlobal(point))

    def on_copy_link(self, button):
        """
Copies a link to the clipboard based on the input button.
        :param button: button to use for determining which link to copy
        """
        cb = self.manager.mw.app.clipboard()
        cb.clear(mode=cb.Clipboard)

        if button.objectName() == self.ui.patreon_button.objectName():
            cb.setText(PATREON_URL, mode=cb.Clipboard)
        elif button.objectName() == self.ui.kofi_button.objectName():
            cb.setText(KOFI_URL, mode=cb.Clipboard)
        elif button.objectName() == self.ui.like_button.objectName():
            cb.setText(ANKI_URL, mode=cb.Clipboard)

    def open_color_dialog(self, preview: QLabel):
        """
Opens a color picker dialog and updates the selected config color.
        :param preview: QLabel to update when showing the selected color value
        """
        is_primary = preview.objectName() == self.ui.primary_color_preview.objectName()
        selected_color = self._primary_color if is_primary else self._secondary_color

        color = QColorDialog().getColor(initial=QColor(selected_color), options=QColorDialog.ShowAlphaChannel)

        if color.isValid():
            color_name = color.name(QColor.HexRgb)
            set_label_background(preview, color_name)
            if is_primary:
                self._primary_color = color_name
            else:
                self._secondary_color = color_name

    def on_range_type_change(self, idx: int):
        """
    Updates dialog ui based on the current range-type selection.
        :param idx: range-type index
        """
        if idx == Range.CUSTOM:
            self.ui.custom_range_spinbox.show()
            self.ui.use_calendar_checkbox.hide()
            # self.ui.appearance_grid_layout.replaceWidget(self.ui.use_calendar_checkbox, self.ui.custom_range_spinbox)
            self.ui.range_select_layout.layout().replaceWidget(self.ui.use_calendar_checkbox,
                                                               self.ui.custom_range_spinbox)
        else:
            self.ui.custom_range_spinbox.hide()
            self.ui.use_calendar_checkbox.show()
            self.ui.range_select_layout.layout().replaceWidget(self.ui.custom_range_spinbox,
                                                               self.ui.use_calendar_checkbox)

        self.update_calendar_range_extras()

    def on_restore_defaults(self):
        """
Restores all config value to their default settings.
        """
        for field in Config.DEFAULT_CONFIG:
            # load temp defaults
            self.config[field] = Config.DEFAULT_CONFIG[field]
        self._load()

    def update_calendar_range_extras(self):
        """
Updates the calendar date checkbox label with the appropriate range-type string based on the currently selected
range-type index.
        """
        self._redraw_calendar_checkbox()
        dropdown_index = self.ui.range_select_dropdown.currentIndex()
        if dropdown_index != Range.CUSTOM:
            type_index = dropdown_index if dropdown_index != Range.TWO_WEEKS else Range.WEEK
            self.ui.use_calendar_checkbox.setText(f'{String.USE_CALENDAR} {Range.LABEL[type_index]}')

        using_calendar_range = self.ui.use_calendar_checkbox.isChecked()
        if (dropdown_index == Range.WEEK or dropdown_index == Range.TWO_WEEKS) and using_calendar_range:
            self.ui.week_start_dropdown.show()
            self.ui.week_start_label.show()
        else:
            self.ui.week_start_dropdown.hide()
            self.ui.week_start_label.hide()
            self.ui.week_start_label.hide()


class DeckItem(QWidget):

    def __init__(self, text: str, dialog: TimeStatsOptionsDialog):
        """
DeckItem used for DeckListItems to give more options to interaction between the list and the enabled decks.
        :param text: string value to use for the label of the list item
        :param dialog: reference to the base class to use for context menu actions
        """
        super().__init__()
        self.context_menu = QMenu(self)
        self.dialog = dialog

        self.label = QLabel(text)
        self.label.setFixedHeight(18)

        self.item_layout = QHBoxLayout()
        self.item_layout.setContentsMargins(4, 0, 0, 0)

        self.item_layout.addWidget(self.label)
        self.setLayout(self.item_layout)

        self.enabled = False

    def __lt__(self: DeckItem, other: DeckItem):
        """
Uses the DeckItems enabled/disabled values, otherwise label text, to sort the items in descending order.
        :param other: comparable DeckItem
        :return: True if the current DeckItem is less than the other DeckItem
        """
        if not isinstance(self, DeckItem):
            return True
        elif not isinstance(other, DeckItem):
            return False

        if self.is_included() != other.is_included():
            return self.is_included() and not other.is_included()
        else:
            return self.label.text() < other.label.text()

    def from_widget(self: QWidget):
        return self if isinstance(self, DeckItem) else QWidget(self)

    def from_list_widget(self: TimeStatsOptionsDialog, item: QListWidgetItem) -> DeckItem:
        return self.ui.excluded_decks_list.itemWidget(item)

    def is_included(self):
        """
Returns enabled state of the current DeckItem.
        :return: True if the DeckItem is enabled, otherwise false
        """
        return self.enabled

    def set_included(self, enable: bool):
        """
Sets the enabled state of the current DeckItem and updates its label to represent that.
        :param enable: value the DeckItem should be set to
        """
        self.label.setEnabled(enable)
        self.enabled = enable

    def mousePressEvent(self, mouse_event: aqt.QMouseEvent) -> None:
        super(DeckItem, self).mousePressEvent(mouse_event)
        if mouse_event.button() == aqt.qt.Qt.RightButton:
            self.on_context_menu(mouse_event.pos())

    def on_context_menu(self, point):
        """
Opens a context menu for modifying deck list info.
        :param point: input coordinate to display the menu
        """
        self.context_menu = QMenu(self)
        self.context_menu.addAction(String.ENABLE_ACTION).triggered.connect(
            lambda: self.dialog.set_selected_enabled(True)
        )
        self.context_menu.addAction(String.DISABLE_ACTION).triggered.connect(
            lambda: self.dialog.set_selected_enabled(False)
        )
        self.context_menu.exec(self.mapToGlobal(point))


class DeckListItem(QListWidgetItem):
    def __lt__(self: DeckListItem, other: DeckListItem):
        """
Uses the base DeckItem to sort its value less than the other DeckItem.
        :param other: comparable DeckListItem
        :return: True if this item is less than ther other DeckItem
        """
        this_item = DeckItem.from_widget(self.listWidget().itemWidget(self))
        other_item = DeckItem.from_widget(other.listWidget().itemWidget(other))
        return this_item < other_item
