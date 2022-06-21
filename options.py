from aqt.qt import QDialog
from .config import StudyTimeStatsConfig
from .options_dialog import Ui_OptionsDialog


class OptionsDialog(QDialog):
    def __init__(self, config: StudyTimeStatsConfig):
        super().__init__()

        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)



