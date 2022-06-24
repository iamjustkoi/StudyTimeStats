from aqt.qt import QDialog
from .config import TimeStatsConfigManager
from .consts import Config
from .options_dialog import Ui_OptionsDialog


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
        self.manager = conf_manager
        self.config = conf_manager.config
        self._load()

    def _load(self):
        self.ui.week_start_dropdown.setCurrentIndex(self.config[Config.WEEK_START])

    def _save(self):
        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        self.close()



