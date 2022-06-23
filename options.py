from aqt.qt import QDialog
from .config import TimeStatsConfigManager
from .consts import Config
from .options_dialog import Ui_OptionsDialog


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()

        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
        self.config_manager = conf_manager
        config = conf_manager.get_config()

        self._load(config)

    def _load(self, config):
        self.ui.week_start_dropdown.setCurrentIndex(config[Config.WEEK_START])

    def accept(self) -> None:
        self.config_manager.get_config()[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config_manager.write_config()
        self.close()



