from .config import TimeStatsConfigManager
from aqt.qt import QDialog


class OptionsDialog(QDialog):
    def __init__(self, config: TimeStatsConfigManager):
        super(OptionsDialog, self).__init__()
        self.config = config
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Overview Time Stats Options")
        self.setMaximumHeight(350)
        self.setMaximumWidth(332)
