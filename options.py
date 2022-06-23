from aqt.qt import QDialog
from .config import TimeStatsConfigManager
from .consts import Config, Days
from .options_dialog import Ui_OptionsDialog


class TimeStatsOptionsDialog(QDialog):

    def __init__(self, conf_manager: TimeStatsConfigManager):
        super().__init__()

        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
        self.config_manager = conf_manager
        self.config = self.config_manager.get_config()

        print(f'loaded idx: {self.config[Config.WEEK_START]}')
        self.ui.week_start_dropdown.setCurrentIndex(self.config[Config.WEEK_START])

    def accept(self) -> None:
        # super(self.ui).accepted()
        print(f'saved idx: {self.ui.week_start_dropdown.currentIndex()}')

        self.config[Config.WEEK_START] = self.ui.week_start_dropdown.currentIndex()
        self.config_manager.set_config(self.config)

        self.close()



