# from PyQt5.QtWidgets import QAction
from aqt.qt import QDialog, QColorDialog, QColor, QLabel, QDialogButtonBox, QRect
from .config import TimeStatsConfigManager
from .consts import Config, RangeType, Text
from .options_dialog import Ui_OptionsDialog
from aqt.studydeck import StudyDeck


def set_label_background(label: QLabel, hex_arg: str):
    label.setStyleSheet(f'QWidget {{background-color: {hex_arg}}}')


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()
        self.manager = conf_manager
        self.config = conf_manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self._primary_color = self.config[Config.PRIMARY_COLOR]
        self._secondary_color = self.config[Config.SECONDARY_COLOR]

        # Exclude Tab Button Actions
        self.ui.add_button.clicked.connect(self.on_add_clicked)
        self.ui.remove_button.clicked.connect(self.on_remove_clicked)

        # Restore Defaults Button
        self.ui.confirm_button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.on_restore_defaults)

        # Color Select Button
        self.ui.primary_color_button.clicked.connect(lambda: self.open_color_dialog(self.ui.primary_color_preview))
        self.ui.seconday_color_button.clicked.connect(lambda: self.open_color_dialog(self.ui.secondary_color_preview))

        # Range Button
        self.ui.range_select_dropdown.activated[int].connect(self.on_range_type_change)
        self.ui.use_calendar_checkbox.clicked.connect(self.update_calendar_range_extras)

        # Update the position of the custom spinbox to the same position as the calendar checkbox
        self.ui.appearance_grid_layout.replaceWidget(self.ui.use_calendar_checkbox, self.ui.custom_range_spinbox)

        # Update custom range's max value
        self.ui.custom_range_spinbox.setMaximum(self.manager.max_range)

        self._load()

    def open_color_dialog(self, preview: QLabel):
        is_primary = preview.objectName() == self.ui.primary_color_preview.objectName()
        selected_color = self._primary_color if is_primary else self._secondary_color

        color = QColorDialog.getColor(initial=QColor(selected_color), options=QColorDialog.ShowAlphaChannel)

        if color.isValid():
            color_name = color.name(QColor.HexRgb)
            set_label_background(preview, color_name)
            if is_primary:
                self._primary_color = color_name
            else:
                self._secondary_color = color_name

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
        deck_dialog.form.buttonBox.removeButton(deck_dialog.form.buttonBox.button(QDialogButtonBox.Help))
        deck_dialog.origNames = list(filter(lambda name: name not in self.excluded_deck_names, deck_dialog.names))
        deck_dialog.redraw('')

    def on_remove_clicked(self):
        for item in self.ui.excluded_decks_list.selectedItems():
            self.excluded_deck_names.remove(item.text())
            list(self.config[Config.EXCLUDED_DIDS]).remove(self.manager.decks.id(name=item.text(), create=False))

        self.ui.excluded_decks_list.clear()
        self.ui.excluded_decks_list.addItems(self.excluded_deck_names)

    def on_deck_excluded(self, study_deck: StudyDeck):
        excluded_deck_name = study_deck.name
        self.excluded_deck_names += [excluded_deck_name]
        self.config[Config.EXCLUDED_DIDS] += [self.manager.decks.id(name=excluded_deck_name, create=False)]
        self.ui.excluded_decks_list.addItem(excluded_deck_name)

    def on_restore_defaults(self):
        print(f'restore defaults')
        for field in Config.DEFAULT_CONFIG:
            # load temp defaults
            self.config[field] = Config.DEFAULT_CONFIG[field]
        self._load()

    def accept(self) -> None:
        self._save()
        self.close()

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

    def _redraw_cal_checkbox(self):
        width = self.ui.use_calendar_checkbox.width()
        height = self.ui.use_calendar_checkbox.height()
        x = self.ui.use_calendar_checkbox.pos().x()
        y = self.ui.use_calendar_checkbox.pos().y()

        self.ui.use_calendar_checkbox.setGeometry(QRect(x, y, width, height))

    def _get_excluded_dids(self):
        names = [self.ui.excluded_decks_list.item(i).text() for i in range(self.ui.excluded_decks_list.count())]
        return [self.manager.decks.id(item, create=False) for item in names]

    def _load(self):
        self.ui.week_start_dropdown.setCurrentIndex(self.config[Config.WEEK_START])

        self.ui.range_select_dropdown.setCurrentIndex(self.config[Config.RANGE_TYPE])
        self.on_range_type_change(self.ui.range_select_dropdown.currentIndex())

        self.ui.use_calendar_checkbox.setChecked(self.config[Config.USE_CALENDAR_RANGE])
        self.update_calendar_range_extras()

        self.ui.custom_range_spinbox.setValue(self.config[Config.CUSTOM_RANGE])
        self.ui.total_line.setText(self.config[Config.CUSTOM_TOTAL_TEXT])
        self.ui.ranged_line.setText(self.config[Config.CUSTOM_RANGE_TEXT])

        # Color Pickers
        set_label_background(self.ui.primary_color_preview, self.config[Config.PRIMARY_COLOR])
        set_label_background(self.ui.secondary_color_preview, self.config[Config.SECONDARY_COLOR])

        self.ui.browser_checkbox.setChecked(self.config[Config.BROWSER_ENABLED])
        self.ui.overview_checkbox.setChecked(self.config[Config.OVERVIEW_ENABLED])
        self.ui.congrats_checkbox.setChecked(self.config[Config.CONGRATS_ENABLED])

        # Excluded Decks
        self.excluded_deck_names = [self.manager.decks.name(i) for i in self.config.get(Config.EXCLUDED_DIDS)]
        self.ui.excluded_decks_list.clear()
        self.ui.excluded_decks_list.addItems(self.excluded_deck_names)

    def _save(self):
        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config[Config.RANGE_TYPE] = self.ui.range_select_dropdown.currentIndex()
        self.config[Config.USE_CALENDAR_RANGE] = self.ui.use_calendar_checkbox.isChecked()
        self.config[Config.CUSTOM_RANGE] = self.ui.custom_range_spinbox.value()
        self.config[Config.CUSTOM_TOTAL_TEXT] = self.ui.total_line.text()
        self.config[Config.CUSTOM_RANGE_TEXT] = self.ui.ranged_line.text()

        # Primary Color css stylesheet
        self.config[Config.PRIMARY_COLOR] = self._primary_color
        self.config[Config.SECONDARY_COLOR] = self._secondary_color

        self.config[Config.BROWSER_ENABLED] = self.ui.browser_checkbox.isChecked()
        self.config[Config.OVERVIEW_ENABLED] = self.ui.overview_checkbox.isChecked()
        self.config[Config.CONGRATS_ENABLED] = self.ui.congrats_checkbox.isChecked()

        self.config[Config.EXCLUDED_DIDS] = self._get_excluded_dids()

        self.manager.write_config()
        self.manager.reload()
