# from PyQt5.QtWidgets import QAction
from aqt.qt import QDialog, QColorDialog, QColor, QLabel
from .config import TimeStatsConfigManager
from .consts import Config, Range
from .options_dialog import Ui_OptionsDialog
from aqt.studydeck import StudyDeck


def set_background_color(label: QLabel, hex_arg: str):
    label.setStyleSheet(f'QWidget {{background-color: {hex_arg}}}')


def get_background_color(label: QLabel):
    stylesheet = label.styleSheet()
    return stylesheet.replace('QWidget {background-color: ', '').replace('}', '')


class TimeStatsOptionsDialog(QDialog):
    form = None

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
        self.manager = conf_manager
        self.config = conf_manager.config

        self._load()

    def accept(self) -> None:
        self._save()
        self.close()

    def on_range_type_change(self, idx: int):
        if idx == Range.CUSTOM:
            self.ui.custom_range_spinbox.show()
        else:
            self.ui.custom_range_spinbox.hide()

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

    def on_deck_excluded(self, study_deck: StudyDeck):
        excluded_deck_name = study_deck.name
        self.excluded_deck_names += [excluded_deck_name]
        self.config[Config.EXCLUDED_DIDS] += [self.manager.decks.id(name=excluded_deck_name, create=False)]
        self.ui.excluded_decks_list.addItem(excluded_deck_name)

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
            # if button.objectName() == self.ui.primary_color_button.objectName():
            # elif button.objectName() == self.ui.seconday_color_button.objectName():
            #     set_background_color(self.ui.secondary_color_preview, color.name(QColor.HexArgb))

    def _load(self):
        config = self.config
        ui = self.ui
        ui.week_start_dropdown.setCurrentIndex(config[Config.WEEK_START])

        ui.range_select_dropdown.activated[int].connect(self.on_range_type_change)
        ui.range_select_dropdown.setCurrentIndex(config[Config.RANGE_TYPE])
        self.on_range_type_change(self.ui.range_select_dropdown.currentIndex())

        ui.use_start_checkbox.setChecked(config[Config.USE_WEEK_START])
        ui.custom_range_spinbox.setValue(config[Config.CUSTOM_RANGE])
        ui.total_line.setText(config[Config.CUSTOM_TOTAL_TEXT])
        ui.ranged_line.setText(config[Config.CUSTOM_RANGE_TEXT])

        # Color Pickers
        set_background_color(ui.primary_color_preview, config[Config.PRIMARY_COLOR])
        ui.primary_color_button.clicked.connect(lambda: self.on_color_dialog(ui.primary_color_preview))
        set_background_color(ui.secondary_color_preview, config[Config.SECONDARY_COLOR])
        ui.seconday_color_button.clicked.connect(lambda: self.on_color_dialog(ui.secondary_color_preview))

        ui.browser_checkbox.setChecked(config[Config.BROWSER_ENABLED])
        ui.overview_checkbox.setChecked(config[Config.OVERVIEW_ENABLED])
        ui.congrats_checkbox.setChecked(config[Config.CONGRATS_ENABLED])

        # Excluded Decks
        self.excluded_deck_names = [self.manager.decks.name(i) for i in self.config.get(Config.EXCLUDED_DIDS)]
        ui.excluded_decks_list.addItems(self.excluded_deck_names)

        # Button Actions
        ui.add_button.clicked.connect(self.on_add_clicked)
        ui.remove_button.clicked.connect(self.on_remove_clicked)

        ui.tabs_widget.setCurrentIndex(0)

    def _save(self):
        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config[Config.RANGE_TYPE] = self.ui.range_select_dropdown.currentIndex()
        self.config[Config.USE_WEEK_START] = self.ui.use_start_checkbox.isChecked()
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
