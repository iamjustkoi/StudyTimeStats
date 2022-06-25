# from PyQt5.QtWidgets import QAction
from aqt.qt import QDialog, QColorDialog, QColor, QLabel, QDialogButtonBox, QRect
from .config import TimeStatsConfigManager
from .consts import Config, RangeType, Text
from .options_dialog import Ui_OptionsDialog
from aqt.studydeck import StudyDeck


def set_background_color(label: QLabel, hex_arg: str):
    label.setStyleSheet(f'QWidget {{background-color: {hex_arg}}}')


def get_background_color(label: QLabel):
    stylesheet = label.styleSheet()
    return stylesheet.replace('QWidget {background-color: ', '').replace('}', '')


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
        self.manager = conf_manager
        self.config = conf_manager.config

        self._load(True)

    def accept(self) -> None:
        self._save()
        self.close()

    def on_range_type_change(self, idx: int):
        if idx == RangeType.CUSTOM:
            self.ui.custom_range_spinbox.show()
            self.ui.use_calendar_checkbox.hide()
            self.ui.appearance_grid_layout.replaceWidget(self.ui.use_calendar_checkbox, self.ui.custom_range_spinbox)
        else:
            self.ui.custom_range_spinbox.hide()
            self.ui.use_calendar_checkbox.show()
            self.ui.appearance_grid_layout.replaceWidget(self.ui.custom_range_spinbox, self.ui.use_calendar_checkbox)

        self.update_calendar_range_extras()

    # def update_use_cal_checkbox_label(self):

    def _redraw_cal_checkbox(self):
        width = self.ui.use_calendar_checkbox.width()
        height = self.ui.use_calendar_checkbox.height()
        x = self.ui.use_calendar_checkbox.pos().x()
        y = self.ui.use_calendar_checkbox.pos().y()

        self.ui.use_calendar_checkbox.setGeometry(QRect(x, y, width, height))

    def update_calendar_range_extras(self):
        self._redraw_cal_checkbox()
        dropdown_index = self.ui.range_select_dropdown.currentIndex()
        if dropdown_index != RangeType.CUSTOM:
            text_range = {
                RangeType.WEEK: Text.WEEK,
                RangeType.TWO_WEEKS: Text.WEEK,
                RangeType.MONTH: Text.MONTH,
                RangeType.YEAR: Text.YEAR
            }
            self.ui.use_calendar_checkbox.setText(f'{Text.USE_CALENDAR} {text_range[dropdown_index]}')

        using_calendar_range = self.ui.use_calendar_checkbox.isChecked()
        if (dropdown_index == RangeType.WEEK or dropdown_index == RangeType.TWO_WEEKS) and using_calendar_range:
            self.ui.week_start_dropdown.show()
            self.ui.week_start_label.show()
        else:
            self.ui.week_start_dropdown.hide()
            self.ui.week_start_label.hide()

    def on_deck_excluded(self, study_deck: StudyDeck):
        excluded_deck_name = study_deck.name
        self.excluded_deck_names += [excluded_deck_name]
        self.config[Config.EXCLUDED_DIDS] += [self.manager.decks.id(name=excluded_deck_name, create=False)]
        self.ui.excluded_decks_list.addItem(excluded_deck_name)

    def on_add_clicked(self):
        from aqt.qt import QDialogButtonBox

        deck_dialog = StudyDeck(
            self.manager.mw,
            accept="Exclude",
            title='Select Excluded Deck',
            parent=self,
            geomKey='selectDeck',
            buttons=[],
            callback=self.on_deck_excluded
        )

        # Filter out currently excluded and redraw the study deck dialog
        deck_dialog.form.buttonBox.removeButton(deck_dialog.form.buttonBox.button(QDialogButtonBox.StandardButton.Help))
        deck_dialog.origNames = list(filter(lambda name: name not in self.excluded_deck_names, deck_dialog.names))
        deck_dialog.redraw('')

    def on_remove_clicked(self):
        for item in self.ui.excluded_decks_list.selectedItems():
            self.excluded_deck_names.remove(item.text())
            list(self.config[Config.EXCLUDED_DIDS]).remove(self.manager.decks.id(name=item.text(), create=False))

        self.ui.excluded_decks_list.clear()
        self.ui.excluded_decks_list.addItems(self.excluded_deck_names)

    def on_color_dialog(self, preview: QLabel):
        color = \
            QColorDialog.getColor(initial=QColor(get_background_color(preview)), options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            set_background_color(preview, color.name(QColor.HexArgb))

    def _load(self, init=False):
        ui = self.ui

        if init:
            # Exclude Tab Button Actions
            ui.add_button.clicked.connect(self.on_add_clicked)
            ui.remove_button.clicked.connect(self.on_remove_clicked)

            # Restore Defaults Button Action
            ui.confirm_button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.on_restore_defaults)

            # Color Select Button Actions
            ui.primary_color_button.clicked.connect(lambda: self.on_color_dialog(ui.primary_color_preview))
            ui.seconday_color_button.clicked.connect(lambda: self.on_color_dialog(ui.secondary_color_preview))

            # update the position of the custom spinbox to the same position as the calendar checkbox
            self.ui.appearance_grid_layout.replaceWidget(self.ui.use_calendar_checkbox, self.ui.custom_range_spinbox)

            ui.range_select_dropdown.activated[int].connect(self.on_range_type_change)
            # ui.use_calendar_checkbox.activated[bool].connect(self.update_calendar_range_extras)
            ui.use_calendar_checkbox.clicked.connect(self.update_calendar_range_extras)
            ui.custom_range_spinbox.setMaximum(self.manager.max_range)

        ui.week_start_dropdown.setCurrentIndex(self.config[Config.WEEK_START])

        ui.range_select_dropdown.setCurrentIndex(self.config[Config.RANGE_TYPE])
        self.on_range_type_change(self.ui.range_select_dropdown.currentIndex())

        ui.use_calendar_checkbox.setChecked(self.config[Config.USE_CALENDAR_RANGE])
        self.update_calendar_range_extras()

        ui.custom_range_spinbox.setValue(self.config[Config.CUSTOM_RANGE])
        ui.total_line.setText(self.config[Config.CUSTOM_TOTAL_TEXT])
        ui.ranged_line.setText(self.config[Config.CUSTOM_RANGE_TEXT])

        # Color Pickers
        set_background_color(ui.primary_color_preview, self.config[Config.PRIMARY_COLOR])
        set_background_color(ui.secondary_color_preview, self.config[Config.SECONDARY_COLOR])

        ui.browser_checkbox.setChecked(self.config[Config.BROWSER_ENABLED])
        ui.overview_checkbox.setChecked(self.config[Config.OVERVIEW_ENABLED])
        ui.congrats_checkbox.setChecked(self.config[Config.CONGRATS_ENABLED])

        # Excluded Decks
        self.excluded_deck_names = [self.manager.decks.name(i) for i in self.config.get(Config.EXCLUDED_DIDS)]
        ui.excluded_decks_list.clear()
        ui.excluded_decks_list.addItems(self.excluded_deck_names)

    def on_restore_defaults(self):
        print(f'restore defaults')
        for field in Config.DEFAULT_CONFIG:
            # load temp defaults
            self.config[field] = Config.DEFAULT_CONFIG[field]
        self._load()

    def _save(self):
        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config[Config.RANGE_TYPE] = self.ui.range_select_dropdown.currentIndex()
        self.config[Config.USE_CALENDAR_RANGE] = self.ui.use_calendar_checkbox.isChecked()
        self.config[Config.CUSTOM_RANGE] = self.ui.custom_range_spinbox.value()
        self.config[Config.CUSTOM_TOTAL_TEXT] = self.ui.total_line.text()
        self.config[Config.CUSTOM_RANGE_TEXT] = self.ui.ranged_line.text()

        # Primary Color css stylesheet
        self.config[Config.PRIMARY_COLOR] = get_background_color(self.ui.primary_color_preview)
        self.config[Config.SECONDARY_COLOR] = get_background_color(self.ui.secondary_color_preview)

        self.config[Config.BROWSER_ENABLED] = self.ui.browser_checkbox.isChecked()
        self.config[Config.OVERVIEW_ENABLED] = self.ui.overview_checkbox.isChecked()
        self.config[Config.CONGRATS_ENABLED] = self.ui.congrats_checkbox.isChecked()

        self.config[Config.EXCLUDED_DIDS] = self._get_excluded_dids()

        self.manager.write_config()
        print(f'Result Config: {self.config}')

    def _get_excluded_dids(self):
        names = [self.ui.excluded_decks_list.item(i).text() for i in range(self.ui.excluded_decks_list.count())]
        return [self.manager.decks.id(item, create=False) for item in names]
