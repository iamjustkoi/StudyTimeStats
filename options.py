from aqt.qt import QDialog
from .config import StudyTimeStatsConfig
from .consts import Config
from .options_dialog import Ui_OptionsDialog


class OptionsDialog(QDialog):

    def __init__(self, config: StudyTimeStatsConfig):
        super().__init__()

        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        # TODO: get config value and apply to dropdown
        # self.ui.week_start_dropdown.setCurrentIndex(config.get_config().get(Config.WEEK_START))

