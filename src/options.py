#  MIT License: 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
#  Full license text available in the "LICENSE" file, packaged with the add-on.

from __future__ import annotations

import webbrowser
from datetime import date
from pathlib import Path

import aqt.theme
import markdown
from aqt.qt import (
    QAbstractAnimation,
    QAction,
    QColor,
    QColorDialog,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QIcon,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPoint,
    QPropertyAnimation,
    QResizeEvent,
    QSortFilterProxyModel,
    QStandardItem,
    QStandardItemModel,
    QToolButton,
    QWidget,
    Qt,
    pyqtSignal,
)

from .config import ANKI_VERSION, TimeStatsConfigManager
from .consts import *
from ..res.ui.cell_item import Ui_CellWidget
from ..res.ui.macro_dialog import Ui_MacroDialog
from ..res.ui.options_dialog import Ui_OptionsDialog
from ..src.overview import parsed_string

if ANKI_QT_VER == 6:
    WindowModal = Qt.WindowModality.WindowModal
    UserRole = Qt.ItemDataRole.UserRole
    MaskOutColor = Qt.MaskMode.MaskOutColor
    RightButton = Qt.MouseButton.RightButton
else:
    WindowModal = Qt.WindowModal
    UserRole = Qt.UserRole
    MaskOutColor = Qt.MaskOutColor
    RightButton = Qt.RightButton

FLAT_ICON_STYLE = \
    '''
    background: transparent;
    border: none;
    width: 20px;
    height: 20px;
    '''


def _refresh_cell_list(list_widget: QListWidget):
    """
    Updates the sorting indices of the cells in the given QListWidget.

    :param list_widget: The QListWidget containing the cells to be updated.
    """
    # update sorting indices
    for i in range(list_widget.count()):
        cell_widget = list_widget.item(i)
        if isinstance(cell_widget, CellItem.CellListItem):
            cell_widget.cell_item.index = i


def _add_cell_to_list(list_widget: QListWidget, cell_item: CellItem):
    """
    Adds a cell item to a QListWidget and refreshes the list.

    :param list_widget: The QListWidget to add the cell item to.
    :param cell_item: The cell item to add to the list.
    """
    list_widget.addItem(cell_item.list_item)
    list_widget.setItemWidget(cell_item.list_item, cell_item)
    list_widget.sortItems()
    list_widget.currentRowChanged.emit(list_widget.currentRow())

    _refresh_cell_list(list_widget)


def _remove_cell_from_list(list_widget: QListWidget, cell_item: CellItem):
    """
    Removes a cell item from the QListWidget.

    :param list_widget: The QListWidget to remove the cell item from.
    :param cell_item: The cell item to remove.
    """
    for i in range(list_widget.count()):
        item = list_widget.item(i)
        if item and isinstance(item, CellItem.CellListItem) and item.cell_item == cell_item:
            list_widget.takeItem(i)
            break

    _refresh_cell_list(list_widget)

    list_widget.sortItems()
    list_widget.currentRowChanged.emit(list_widget.currentRow())


class TimeStatsOptionsDialog(QDialog):
    anim: QPropertyAnimation

    def __init__(self, conf_manager: TimeStatsConfigManager):
        """
        Addon options QDialog class for accessing and changing the addon's config values.

        :param conf_manager: TimeStatsConfigManager used to reading and writing user input.
        """
        super().__init__(flags=aqt.mw.windowFlags())

        self.manager = conf_manager
        self.config = conf_manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.setWindowIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{ADDON_ICON_PATH}'))

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

        # Convert markdown to HTML and update
        self.ui.about_label_header.setText(markdown.markdown(self.ui.about_label_header.text()))
        self.ui.about_label_body.setText(markdown.markdown(self.ui.about_label_body.text()))

        # Restore Defaults Button
        self.ui.confirm_button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.on_restore_defaults)

        # Setup Cell List
        self.ui.cellListWidget.setStyleSheet('#cellListWidget { background: transparent; border: none; }')
        self.ui.cellListWidget.verticalScrollBar().setSingleStep(12)

        # Update about header text with the current version number and stats image
        updated_about_header = self.ui.about_label_header.text().format(
            version=CURRENT_VERSION,
            img_path=f'{Path(__file__).parent.resolve()}\\{ADDON_ICON_PATH}'
        )
        self.ui.about_label_header.setText(updated_about_header)

        # Apply button
        self.apply_button = self.ui.confirm_button_box.button(QDialogButtonBox.Apply)
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.apply)

        # Setting current index again to overwrite QTDesigner's auto-setting, just in case
        self.ui.tabs_widget.setCurrentIndex(0)
        self._load()

        # Attached post-load to prevent pre-change broadcasts
        change_signals = {
            self.ui.browser_checkbox.stateChanged,
            self.ui.overview_checkbox.stateChanged,
            self.ui.congrats_checkbox.stateChanged,
            self.ui.toolbar_checkbox.stateChanged,
            self.ui.include_deleted_checkbox.stateChanged,
            self.ui.excluded_decks_list.itemDoubleClicked,
            self.ui.excluded_decks_list.itemActivated,
            self.ui.deck_enable_button.clicked,
            self.ui.deck_disable_button.clicked,
            self.ui.confirm_button_box.clicked,
            self.ui.useRolloverCheckbox.stateChanged,
            self.ui.useDecimalCheckbox.stateChanged,
            self.ui.cellListWidget.currentRowChanged,
        }

        self._attach_change_signals(change_signals)

        # Build support button
        self.ui.supportButton.setRawIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{HEART_ICON_PATH}'))
        self.ui.supportButton.setTint(Color.BUTTON_ICON[theme_manager.get_night_mode()])
        self.ui.supportButton.setHoverTint(Color.HOVER[theme_manager.get_night_mode()])
        self.ui.supportButton.setStyleSheet('border: unset;')
        self.ui.supportButton.clicked.connect(self.on_support_button_clicked)

        # Short highlight animation
        self.anim = QPropertyAnimation(self.ui.supportButtonHolder, b"opacity")
        self.anim.setDirection(QAbstractAnimation.Direction.Forward)
        self.anim_delay = 30
        self.anim.setEndValue(0)
        highlight_color = ['rgba(0, 0, 0, {alpha})', 'rgba(255, 255, 255, {alpha})']
        support_holder_style_template = f'''
            QFrame {{{{
                background-color: {highlight_color[theme_manager.get_night_mode()]};
                border-radius: 6px;
            }}}};
        '''

        # FIXME: Random flashing at the end of the animation every now and then
        # Updates the support button holder alpha
        def set_support_alpha(alpha: int):
            if self.anim.direction() == QAbstractAnimation.Direction.Forward:
                should_update = self.anim.currentValue() != self.anim.endValue()
            else:
                should_update = self.anim.currentValue() != self.anim.startValue()

            if should_update:
                style = support_holder_style_template.format(alpha=max(alpha - self.anim_delay, self.anim.endValue()))
                # print(f'style({alpha - self.anim_delay})\n{style}')
                self.ui.supportButtonHolder.setStyleSheet(style)

        # Connect value changed listener
        self.anim.valueChanged.connect(set_support_alpha)

        # Set starting value
        set_support_alpha(0)

        win_size: list = self.config.get(Config.WIN_SIZE, None)
        self.resize(win_size[0], win_size[1]) if win_size else None

        self.updateGeometry()

    def resizeEvent(self, evt: QResizeEvent):
        super().resizeEvent(evt)
        # Update the window's size value in the config
        self.manager.write_config_val(Config.WIN_SIZE, [self.width(), self.height()])

    def apply(self):
        """
        Write options to add-on config, refresh the Anki window, and disable the apply button.
        """
        self._save()
        self.apply_button.setEnabled(False)

    def _attach_change_signals(self, signals: set[aqt.qt.pyqtBoundSignal]):
        for signal in signals:
            def enable_apply(*__args):
                """
                Intercept function for the created button. Refreshes the button's visibility after running the input
                write-callback.
                """
                self.apply_button.setEnabled(True)

            signal.connect(enable_apply)

    def _load(self):
        """
        Loads all config values to the options dialog.
        """
        self.ui.toolbar_checkbox.setChecked(self.config[Config.TOOLBAR_ENABLED])

        self.ui.browser_checkbox.setChecked(self.config[Config.BROWSER_ENABLED])
        self.ui.overview_checkbox.setChecked(self.config[Config.OVERVIEW_ENABLED])
        self.ui.congrats_checkbox.setChecked(self.config[Config.CONGRATS_ENABLED])

        self.ui.include_deleted_checkbox.setChecked(self.config[Config.INCLUDE_DELETED])

        self.ui.useRolloverCheckbox.setChecked(self.config[Config.USE_ROLLOVER])

        self.ui.useDecimalCheckbox.setChecked(self.config[Config.USE_DECIMAL])

        # Load Cell Data
        self.ui.cellListWidget.clear()

        # Add blank
        _add_cell_to_list(self.ui.cellListWidget, CellItem(self.ui.cellListWidget, is_empty=True))

        # Loop through data
        for data in self.config[Config.CELLS_DATA]:
            _add_cell_to_list(self.ui.cellListWidget, CellItem(self.ui.cellListWidget, data=data))

        # Excluded Decks
        self._load_excluded_decks()

    def _save(self):
        """
        Retrieves values from options dialog window, updates/writes the values to the current config,
        then resets the main window to update all the ui.
        """
        # Store options
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolbar_checkbox.isChecked()

        self.config[Config.BROWSER_ENABLED] = self.ui.browser_checkbox.isChecked()
        self.config[Config.OVERVIEW_ENABLED] = self.ui.overview_checkbox.isChecked()
        self.config[Config.CONGRATS_ENABLED] = self.ui.congrats_checkbox.isChecked()

        self.config[Config.INCLUDE_DELETED] = self.ui.include_deleted_checkbox.isChecked()

        self.config[Config.USE_ROLLOVER] = self.ui.useRolloverCheckbox.isChecked()

        self.config[Config.USE_DECIMAL] = self.ui.useDecimalCheckbox.isChecked()

        self.config[Config.EXCLUDED_DIDS] = self._get_excluded_dids()

        cell_data = []
        for i in range(self.ui.cellListWidget.count()):
            item = self.ui.cellListWidget.item(i)
            if isinstance(item, CellItem.CellListItem) and not item.cell_item.is_empty:
                cell_data.append(item.cell_item.get_data())
        self.config[Config.CELLS_DATA] = cell_data

        self.manager.write_config()
        self.manager.mw.reset()

    def _load_excluded_decks(self):
        """
        Loads deck names to list and sets label to enabled if not in current config's excluded decks.
        """
        self.excluded_deck_names = [self.manager.decks.name(i) for i in self.config.get(Config.EXCLUDED_DIDS)]
        decks_list = self.ui.excluded_decks_list
        decks_list.clear()

        if ANKI_VERSION > ANKI_LEGACY_VER:
            all_decks = self.manager.mw.col.decks.all_names_and_ids()
        else:
            all_decks = self.manager.mw.col.decks.allNames()

        for deck in all_decks:
            deck_name = deck.name if ANKI_VERSION > ANKI_LEGACY_VER else deck
            deck_item = DeckItem(deck_name, self)
            deck_item.set_included(deck_item.label.text() not in self.excluded_deck_names)

            list_item = DeckListItem(decks_list)
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

    def on_item_double_clicked(self, item: QListWidgetItem):
        self.set_selected_enabled(not DeckItem.from_list_widget(self, item).is_included())

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
        cb.clear()

        if button.objectName() == self.ui.patreon_button.objectName():
            cb.setText(PATREON_URL)
        elif button.objectName() == self.ui.kofi_button.objectName():
            cb.setText(KOFI_URL)
        elif button.objectName() == self.ui.like_button.objectName():
            cb.setText(ANKI_URL)

    def on_restore_defaults(self):
        """
        Restores all config value to their default settings.
        """
        for field in Config.DEFAULT_CONFIG:
            # load_data temp defaults
            self.config[field] = Config.DEFAULT_CONFIG[field]
        self._load()

    def on_support_button_clicked(self):
        start_value = 127

        # Switch to about tab
        self.ui.tabs_widget.setCurrentWidget(self.ui.about_tab)

        # Scroll to support button holder position
        scroll_pos = self.ui.supportButtonHolder.pos().y()
        self.ui.scroll_area.verticalScrollBar().setValue(scroll_pos)

        # Animate support button holder background color
        if not self.anim.startValue() or self.anim.currentValue() != self.anim.startValue():
            self.anim.setDirection(QAbstractAnimation.Direction.Backward)
            self.anim.setStartValue(start_value + self.anim_delay)
            self.anim.setDuration(100)
            self.anim.start()

        def playForward():
            if self.anim.currentValue() != self.anim.endValue():
                self.anim.setDirection(QAbstractAnimation.Direction.Forward)
                self.anim.setDuration(600)
                self.anim.setStartValue(start_value)
                self.anim.start()

        if self.anim.receivers(self.anim.finished) <= 0:
            self.anim.finished.connect(playForward)


class DeckItem(QWidget):

    def __init__(self, text: str, dialog: TimeStatsOptionsDialog):
        """
        DeckItem used for DeckListItems to give more options to interaction between the list and the enabled decks.

        :param text: string value to use for the label of the list item
        :param dialog: reference to the base class to use for context menu actions
        """
        super().__init__(flags=aqt.mw.windowFlags())
        self.context_menu = QMenu(self)
        self.dialog = dialog

        self.label = QLabel(text)
        self.label.setFixedHeight(18)

        self.item_layout = QHBoxLayout()
        self.item_layout.setContentsMargins(4, 0, 0, 0)

        self.item_layout.addWidget(self.label, alignment=self.label.alignment())
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
        return self if isinstance(self, DeckItem) else QWidget(self, flags=aqt.mw.windowFlags())

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

    def mouseReleaseEvent(self, mouse_event: aqt.QMouseEvent) -> None:
        super(DeckItem, self).mousePressEvent(mouse_event)
        if mouse_event.button() == RightButton:
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


class CellItem(QWidget):
    color_changed = pyqtSignal()

    button_colors: dict = {}
    data: dict = {}
    direction = 'vertical'
    index = 0
    mask_color = 'black'

    class CellListItem(QListWidgetItem):
        cell_item: CellItem

        def __init__(self, *args, cell_item: CellItem):
            """
            QListWidgetItem of a parent, CellItem widget. Used for easy access to widget/widget item properties.

            :param args: Default QT arguments.
            :param cell_item: The QListWidgetItem's referenced/parent cell item.
            """
            super().__init__(*args)
            # Store parent cell item
            self.cell_item = cell_item

        def __lt__(self, other: CellItem.CellListItem):
            other_cell = other.cell_item if (other and isinstance(other, CellItem.CellListItem)) else None

            # Returns whether this cell is less than the other cell's index, unless this cell is empty (always last)
            if not self.cell_item.is_empty:
                return self.cell_item.index < other.cell_item.index if other_cell else True

            return False

    def __init__(self, list_widget: QListWidget, is_empty: bool = False, data: dict = None):
        """
        QWidget used in the cells QListWidget.

        :param list_widget: A QListWidget holding cell items.
        :param is_empty: Whether the cell show use an add button/unfilled template.
        :param data: Data dict used to fill in information for the widget's input objects.
        """
        super().__init__()

        self.index = list_widget.count() - 1
        self.is_empty = is_empty
        self.widget = Ui_CellWidget()
        self.widget.setupUi(CellWidget=self)
        self.list_widget = list_widget

        self.list_item = CellItem.CellListItem(self.list_widget, cell_item=self)

        def add_cell():
            # External cell adder used so lambda doesn't use old/static variables (quick-fix)
            _add_cell_to_list(self.list_widget, CellItem(self.list_widget, False))

        if is_empty:
            # Hide rest of cell, initialize and show the add button

            self.widget.addButton.clicked.connect(lambda *_: add_cell())

            self.widget.addButton.setRawIcon(
                QIcon(f'{Path(__file__).parent.resolve()}\\{ADD_ICON_PATH}')
            )
            self.widget.addButton.setTint(Color.BUTTON_ICON[theme_manager.get_night_mode()])
            self.widget.addButton.setHoverTint(Color.HOVER[theme_manager.get_night_mode()])

            self.widget.addButton.setVisible(True)
            self.widget.mainFrame.setVisible(False)
            self.widget.expandFrame.setVisible(False)
            self.widget.addButton.setFixedHeight(self.widget.addButton.minimumHeight())

        else:
            # Hide the add button, initialize and load all cell inputs/data
            self.build_hover_buttons()
            self.build_color_pickers()
            self.build_direction_buttons()
            self.build_range_inputs()
            self.build_code_button()
            self.build_drag_handles()
            self.build_expando()
            self.build_line_edits()

            self.data = {k: v for k, v in Config.DEFAULT_CELL_DATA.items()} if not data else data
            self.load_data(self.data)

            self.widget.addButton.setVisible(False)
            self.widget.mainFrame.setVisible(True)
            self.widget.expandFrame.setVisible(True)

            self._redraw()
            self.build_signals()

        # Update size hint for the list
        self.list_item.setSizeHint(self.sizeHint())
        self.list_item.setFlags(Qt.ItemFlag.NoItemFlags)

    def load_data(self, data):
        self.widget.titleLineEdit.setText(data[Config.TITLE])
        self.widget.outputLineEdit.setText(data[Config.OUTPUT])
        self.widget.rangeDropdown.setCurrentIndex(data[Config.RANGE] + 1)
        self.widget.calendarCheckbox.setChecked(data[Config.USE_CALENDAR])
        self.widget.startDayDropdown.setCurrentIndex(data[Config.WEEK_START])
        self.widget.hourEdit.setText(data[Config.HRS_UNIT])
        self.widget.minEdit.setText(data[Config.MIN_UNIT])
        self.widget.customRangeSpinbox.setValue(data[Config.DAYS])
        self.widget.codeTextEdit.setPlainText(data[Config.HTML])

        self.set_button_color(self.widget.titleColorButton, data[Config.TITLE_COLOR])
        self.set_button_color(self.widget.outputColorButton, data[Config.OUTPUT_COLOR])
        self.toggle_direction_buttons(data[Config.DIRECTION])

    def get_data(self):
        self.data[Config.TITLE] = self.widget.titleLineEdit.text()
        self.data[Config.OUTPUT] = self.widget.outputLineEdit.text()
        self.data[Config.RANGE] = self.widget.rangeDropdown.currentIndex() - 1
        self.data[Config.USE_CALENDAR] = self.widget.calendarCheckbox.isChecked()
        self.data[Config.WEEK_START] = self.widget.startDayDropdown.currentIndex()
        self.data[Config.HRS_UNIT] = self.widget.hourEdit.text()
        self.data[Config.MIN_UNIT] = self.widget.minEdit.text()
        self.data[Config.DAYS] = self.widget.customRangeSpinbox.value()
        self.data[Config.HTML] = self.widget.codeTextEdit.toPlainText()

        self.data[Config.TITLE_COLOR] = self.button_colors[str(self.widget.titleColorButton)]
        self.data[Config.OUTPUT_COLOR] = self.button_colors[str(self.widget.outputColorButton)]

        self.data[Config.DIRECTION] = self.direction

        return self.data

    def _redraw(self):
        self.widget.expandFrame.adjustSize()
        self.widget.mainFrame.adjustSize()
        self.list_item.setSizeHint(self.sizeHint())

    def build_hover_buttons(self):
        self.widget.removeButton.clicked.connect(lambda *_: self.open_delete_confirm_button(self.list_widget))

        self.widget.removeButton.setRawIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))
        self.widget.removeButton.setTint(Color.BUTTON_ICON[theme_manager.get_night_mode()])
        self.widget.removeButton.setHoverTint(Color.HOVER[theme_manager.get_night_mode()])
        self.widget.removeButton.setStyleSheet(FLAT_ICON_STYLE)

        self.widget.codeButton.setRawIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{CODE_ICON_PATH}'))
        self.widget.codeButton.setTint(Color.BUTTON_ICON[theme_manager.get_night_mode()])
        self.widget.codeButton.setHoverTint(Color.HOVER[theme_manager.get_night_mode()])
        self.widget.codeButton.setStyleSheet(FLAT_ICON_STYLE)

        self.widget.expandoButton.setRawIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{CHEVRON_ICON_PATH}'))
        self.widget.expandoButton.setTint(Color.BUTTON_ICON[theme_manager.get_night_mode()])
        self.widget.expandoButton.setStyleSheet(FLAT_ICON_STYLE)

    def build_color_pickers(self):
        def _append_color_change_signal(button: QToolButton):
            default_set_stylesheet = button.setStyleSheet

            def set_stylesheet(style_sheet: str):
                default_set_stylesheet(style_sheet)
                self.color_changed.emit()

            button.setStyleSheet = set_stylesheet

        self.widget.titleColorButton.clicked.connect(
            lambda _: self.on_click_color_button(button=self.widget.titleColorButton)
        )
        self.widget.outputColorButton.clicked.connect(
            lambda _: self.on_click_color_button(button=self.widget.outputColorButton)
        )

        _append_color_change_signal(self.widget.titleColorButton)
        _append_color_change_signal(self.widget.outputColorButton)

    def build_direction_buttons(self):
        mask_color = '#000000'
        style = f'''
            QPushButton:disabled {{
                background: {Color.BUTTON_ACTIVE[theme_manager.get_night_mode()]};
        ''' + (
            '''            
                width: 24px;
                height: 24px;
                margin-right: 2px;
                margin-left: 2px;
                border-radius: 1px;
            ''' if aqt.QT_VERSION_STR[0] == '5' else '\n    }'
        )

        # Setup radio button-like functionality for the vertical button
        vert_lines = QIcon(f'{Path(__file__).parent.resolve()}\\{VERT_LINES_PATH}')
        vert_pixmap = vert_lines.pixmap(self.widget.directionVerticalButton.size(), QIcon.Normal, QIcon.On)
        mask = vert_pixmap.createMaskFromColor(QColor(mask_color), MaskOutColor)
        vert_pixmap.fill(QColor(Color.BUTTON_ICON[theme_manager.get_night_mode()]))
        vert_pixmap.setMask(mask)
        self.widget.directionVerticalButton.setIcon(QIcon(vert_pixmap))
        self.widget.directionVerticalButton.setStyleSheet(style)

        # Setup radio button-like functionality for the horizontal button
        horiz_lines = QIcon(f'{Path(__file__).parent.resolve()}\\{HORIZ_LINES_PATH}')
        horiz_pixmap = horiz_lines.pixmap(self.widget.directionHorizontalButton.size(), QIcon.Normal, QIcon.On)
        mask = horiz_pixmap.createMaskFromColor(QColor(mask_color), MaskOutColor)
        horiz_pixmap.fill(QColor(Color.BUTTON_ICON[theme_manager.get_night_mode()]))
        horiz_pixmap.setMask(mask)
        self.widget.directionHorizontalButton.setIcon(QIcon(horiz_pixmap))
        self.widget.directionHorizontalButton.setStyleSheet(style)

        # Connect signals
        self.widget.directionVerticalButton.clicked.connect(lambda _: self.toggle_direction_buttons())
        self.widget.directionHorizontalButton.clicked.connect(lambda _: self.toggle_direction_buttons())

    def build_line_edits(self, mask_color='black'):
        # Build macro-add action's icon and colors
        icon_path = f'{Path(__file__).parent.resolve()}\\{ADD_ICON_PATH}'
        tint_color = Color.BUTTON_ICON[theme_manager.get_night_mode()]

        pixmap = QIcon(icon_path).pixmap(self.size(), QIcon.Normal, QIcon.On)
        mask = pixmap.createMaskFromColor(QColor(mask_color), MaskOutColor)

        pixmap.fill(QColor(tint_color))
        pixmap.setMask(mask)

        icon = QIcon(pixmap)

        # Add the actions to the QLineEdits
        action = QAction(icon, 'Add Text Macro', self.widget.titleLineEdit)
        action.triggered.connect(lambda _: self.open_macro_dialog(self.widget.titleLineEdit))
        self.widget.titleLineEdit.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

        action = QAction(icon, 'Add Text Macro', self.widget.outputLineEdit)
        action.triggered.connect(lambda _: self.open_macro_dialog(self.widget.outputLineEdit))
        self.widget.outputLineEdit.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

    def build_range_inputs(self):
        self.widget.rangeDropdown.currentIndexChanged.connect(self.on_range_update)
        self.widget.calendarCheckbox.stateChanged.connect(self.on_use_calendar_update)
        self.on_range_update(0)  # Initial update

        self.widget.customRangeSpinbox.setMaximum((date.today() - date.fromisoformat(UNIQUE_DATE)).days)
        self.widget.customRangeSpinbox.setMinimum(1)

    def build_code_button(self):
        self.widget.codeButton.clicked.connect(lambda _: self.toggle_code_editor())
        self.toggle_code_editor(True)

    def build_expando(self):
        self.widget.expandoButton.clicked.connect(lambda _: self.toggle_expando())
        self.toggle_expando(True)

    def build_drag_handles(self):
        self.widget.dragHandle.icon_color = Color.BUTTON_ICON[theme_manager.get_night_mode()]
        self.widget.dragHandle.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{HANDLES_PATH}'))
        self.widget.dragHandle.setStyleSheet(FLAT_ICON_STYLE)
        self.widget.dragHandle.list_widget = self.list_widget
        self.widget.dragHandle.list_item = self.list_item

    def build_signals(self):
        def broadcast_change_signal(__data=None, *__):
            self.list_widget.currentRowChanged.emit(self.index)

        # lambda *__: broadcast_change_signal(cell=self)
        self.widget.titleLineEdit.textChanged.connect(broadcast_change_signal)
        self.widget.outputLineEdit.textChanged.connect(broadcast_change_signal)
        self.widget.hourEdit.textChanged.connect(broadcast_change_signal)
        self.widget.minEdit.textChanged.connect(broadcast_change_signal)
        self.widget.codeTextEdit.textChanged.connect(broadcast_change_signal)

        self.widget.rangeDropdown.currentIndexChanged.connect(broadcast_change_signal)
        self.widget.startDayDropdown.currentIndexChanged.connect(broadcast_change_signal)

        self.widget.calendarCheckbox.stateChanged.connect(broadcast_change_signal)
        self.widget.customRangeSpinbox.valueChanged.connect(broadcast_change_signal)

        self.widget.directionVerticalButton.clicked.connect(broadcast_change_signal)
        self.widget.directionHorizontalButton.clicked.connect(broadcast_change_signal)

        self.color_changed.connect(broadcast_change_signal)

    # noinspection PyUnresolvedReferences
    def toggle_code_editor(self, hide: bool = None):
        """
        Toggles the code editor widget.

        :param hide: A boolean value indicating whether to hide the code editor widget.
        """
        if hide is None:
            is_hidden = self.widget.codeTextEdit.isHidden()
            if is_hidden:
                self.widget.codeTextEdit.show()
                self.widget.codeButton.lockHoverTint(True)
            else:
                self.widget.codeTextEdit.hide()
                self.widget.codeButton.lockHoverTint(False)

        else:
            self.widget.codeTextEdit.show() if not hide else self.widget.codeTextEdit.hide()
            self.widget.codeButton.lockHoverTint(not hide)

        # self.widget.expandFrame.adjustSize()
        self._redraw()

    def toggle_expando(self, collapse: bool = None):
        """
        Toggles the expandable frame of the widget.

        :param collapse: A boolean value indicating whether to hide or show the expandable frame.
        """
        if collapse is None:
            if self.widget.expandFrame.isHidden():
                self.widget.expandFrame.show()
                self.widget.expandoButton.setRotation(0)
            else:
                self.widget.expandFrame.hide()
                self.widget.expandoButton.setRotation(90)
        else:
            self.widget.expandFrame.show() if not collapse else self.widget.expandFrame.hide()
            self.widget.expandoButton.setRotation(90) if not collapse else self.widget.expandoButton.setRotation(0)

        self._redraw()

    def toggle_direction_buttons(self, direction: str = None):
        """
        Toggles the direction buttons of a widget between horizontal and vertical.

        If no direction is specified, both buttons will be toggled. If a direction is specified,
        only the corresponding button will be toggled.

        :param direction: A string representing the direction to toggle the button to. Can be either
                          'horizontal' or 'vertical'. Defaults to None.
        """
        if direction is None:
            self.widget.directionHorizontalButton.setEnabled(not self.widget.directionHorizontalButton.isEnabled())
            self.widget.directionVerticalButton.setEnabled(not self.widget.directionVerticalButton.isEnabled())
        else:
            self.widget.directionHorizontalButton.setEnabled(not direction == Direction.HORIZONTAL)
            self.widget.directionVerticalButton.setEnabled(not direction == Direction.VERTICAL)

        self.widget.directionFrame.setFocus()  # so focus doesn't switch in a weird direction
        self.direction = Direction.VERTICAL if not self.widget.directionVerticalButton.isEnabled() \
            else Direction.HORIZONTAL

    def on_click_color_button(self, button: QToolButton):
        color = QColorDialog.getColor(QColor(self.button_colors[str(button)]))
        if color.isValid():
            self.set_button_color(button, color.name())

    def on_use_calendar_update(self, *__):
        if self.widget.rangeDropdown.currentIndex() - 1 in (Range.WEEK, Range.TWO_WEEKS) \
                and self.widget.calendarCheckbox.isChecked():
            self.widget.startDayLabel.show()
            self.widget.startDayDropdown.show()
        else:
            self.widget.startDayLabel.hide()
            self.widget.startDayDropdown.hide()

        self._redraw()

    def on_range_update(self, index: int):
        """
        Updates and toggles the visibility of all range-related elements based on the passed index value.

        :param index: An integer representing the range index.
        """
        range_idx = index - 1
        self.data[Config.RANGE] = range_idx

        if range_idx == Range.TOTAL:
            self.widget.rangeExtraFrame.hide()
            self.widget.startDayLabel.hide()
            self.widget.startDayDropdown.hide()
        elif range_idx == Range.CUSTOM:
            self.widget.rangeExtraFrame.show()
            self.widget.startDayLabel.hide()
            self.widget.startDayDropdown.hide()
            self.widget.customRangeSpinbox.show()
            self.widget.calendarCheckbox.hide()
        elif range_idx in (Range.WEEK, Range.TWO_WEEKS):
            self.widget.rangeExtraFrame.show()
            self.widget.customRangeSpinbox.hide()
            self.widget.calendarCheckbox.show()
            self.on_use_calendar_update()
            self.widget.calendarCheckbox.setText(f'{String.USE_CALENDAR} {Range.LABEL[Range.WEEK]}')
        elif range_idx in (Range.MONTH, Range.YEAR):
            self.widget.rangeExtraFrame.show()
            self.widget.startDayLabel.hide()
            self.widget.startDayDropdown.hide()
            self.widget.customRangeSpinbox.hide()
            self.widget.calendarCheckbox.show()
            self.widget.calendarCheckbox.setText(f'{String.USE_CALENDAR} {Range.LABEL[range_idx]}')

        # HACK: idk, adjusts size correctly unlike all other attempts
        self.toggle_code_editor()
        self.toggle_code_editor()
        self._redraw()

    def set_button_color(self, button: QToolButton, color: str):
        button.setStyleSheet(f"border-radius: 10px;\n	background-color: {color}; width: 20px; height: 20px;")
        self.button_colors[str(button)] = color

    def open_delete_confirm_button(self, list_widget: QListWidget):
        confirm_button = QToolButton(self)
        confirm_button.setText(String.DELETE_CELL)

        # noinspection PyUnresolvedReferences
        confirm_button.clicked.connect(lambda _: _remove_cell_from_list(list_widget, self))

        confirm_button.leaveEvent = lambda _: confirm_button.deleteLater()
        remove_button_local_pos = self.widget.expandFrame.pos() + self.widget.removeButton.pos()
        padding = self.widget.expandFrame.layout().spacing()

        confirm_button.move(
            QPoint(
                (remove_button_local_pos.x() - confirm_button.width()) + self.widget.removeButton.width() + padding,
                remove_button_local_pos.y()
            )
        )

        confirm_button.show()

    def open_macro_dialog(self, line_edit: aqt.qt.QLineEdit):
        macro_dialog = MacroDialog(line_edit=line_edit, parent=self)
        macro_dialog.show()


class MacroDialog(QDialog):
    class FilterModel(QSortFilterProxyModel):
        def __init__(self, parent=None):
            super().__init__(parent)
            self._filter = ""

        def filterAcceptsRow(self, source_idx, source_parent):
            index = self.sourceModel().index(source_idx, 0, source_parent)
            data = index.data()

            if isinstance(data, str):
                data = data.lower()

            if not self.filter:
                return True

            return self.filter in data

        @property
        def filter(self):
            return self._filter

        @filter.setter
        def filter(self, text: str):
            self._filter = text
            self.invalidateFilter()

    def __init__(self, line_edit: aqt.qt.QLineEdit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowModality(WindowModal)

        self.ui = Ui_MacroDialog()
        self.ui.setupUi(MacroDialog=self)

        self.line_edit = line_edit

        # Initialize configs and the linked cell item
        self.addon_config = None
        self.cell_config = None

        cell_item = self.parent()

        if isinstance(cell_item, CellItem):
            self.cell_item = cell_item
            self.cell_config = self.cell_item.get_data()

            options_dialog = self.cell_item.parent().window()

            if isinstance(options_dialog, TimeStatsOptionsDialog):
                self.addon_config = options_dialog.config

        self.ui.buttonBox.button(aqt.qt.QDialogButtonBox.Ok).setText(String.INSERT)

        class MacroItem:
            def __init__(self, name: str, cmd: str, definition: str):
                """
                Template class used for easy storage/listing.
                """
                self.name = name
                self.cmd = cmd
                self.definition = definition

        self.model = QStandardItemModel()
        self.macros: list[MacroItem] = []

        # Loop through the attribute names of all "CMD"-string attributes in the Macro class
        for attr_name in dir(Macro):
            attr = getattr(Macro, attr_name)

            if isinstance(attr, str) and attr_name.startswith('CMD'):
                # Set definition to string in the definitions dictionary
                macro_def = Macro.DEFINITIONS.get(attr, None)

                if macro_def is not None:
                    # Remove the CMD_ prefix, replace underscores with spaces, and title case the string
                    formatted_name = attr_name.replace('CMD_', '').replace('_', ' ').title()
                    formatted_cmd = attr + ('}' if attr.find('{') >= 0 else '')

                    item_text = f'{formatted_name} - ({formatted_cmd}) {macro_def}'

                    item = QStandardItem(item_text)
                    item.setToolTip(item_text)
                    item.setData(attr, UserRole)

                    # Add row to item list model
                    self.model.appendRow(item)

                    # Append macro to stored list
                    self.macros.append(MacroItem(formatted_name, attr, Macro.DEFINITIONS[attr]))

        # Initialize proxy filter
        self.proxy_model = MacroDialog.FilterModel()
        self.proxy_model.setSourceModel(self.model)

        # Set to the newly created model
        self.ui.listView.setModel(self.proxy_model)

        # Build filter list text-change updates
        def text_changed(text: str):
            self.proxy_model.filter = text.lower()

        self.ui.filterLineEdit.textChanged.connect(text_changed)

        # Run updates to the preview label on item selected
        self.ui.listView.selectionModel().currentChanged.connect(self.update_preview)

        # Use selected macro on double-clicked item
        self.ui.listView.doubleClicked.connect(self.accept)

        # Update list view's item selection
        self.ui.listView.selectionModel().select(
            self.ui.listView.currentIndex(),
            aqt.qt.QItemSelectionModel.SelectCurrent,
        )

    def update_preview(self, index, *__args):
        """
        Update the preview label with the parsed command string, if a matching macro is found.
        If no matching macro is found, display the original command string.

        :param index: The index of the selected item in the model.
        :param __args: Any additional arguments.
        """
        # macro_cmd: str = self.model.data(index, UserRole)
        macro_cmd: str = self.proxy_model.data(index, UserRole)
        macro_cmd += '}' if macro_cmd.find('{') >= 0 else ''

        parsed_cmd = None
        for macro in self.macros:
            if macro.cmd == macro_cmd:
                # Prepend a random character to match an arbitrary context for the
                modified_cmd = f'_{macro_cmd}'

                # Grab the parsed string, minus the prepended context character
                parsed_cmd = parsed_string(modified_cmd, self.addon_config, self.cell_config)[1:]

                self.ui.previewLabel.setText(parsed_cmd)
                break

        if not parsed_cmd:
            self.ui.previewLabel.setText(macro_cmd)

    def accept(self) -> None:
        # Get selected item in QListView
        selected_index = self.ui.listView.currentIndex()

        # Get macro data from selected item
        macro_cmd: str = self.ui.listView.model().data(selected_index, UserRole)

        # Get current cursor position
        cursor_pos = self.line_edit.cursorPosition()

        # Insert text at current cursor position
        self.line_edit.insert(macro_cmd)

        # Set cursor position to end of inserted text
        self.line_edit.setCursorPosition(cursor_pos + len(macro_cmd))

        # Close macro dialog
        self.close()
