import anki.config
from aqt import AnkiQt
from .consts import Config


class TimeStatsConfigManager(dict):
    """
    Generic config manager for accessing and storing the add-on's properties.
    """

    fields = {Config.WEEK_START}

    def __init__(self, mw: AnkiQt):
        super().__init__()
        self._mw = mw
        self.config = self._mw.col.get_config(__name__, default=Config.DEFAULT_CONFIG)
        self._mw.col.set_config(__name__, self.config)

        # self.config = self._mw.addonManager.getConfig(__name__)

        # self._mw.addonManager.addonConfigDefaults(__name__)

        # self._mw.addonManager.getConfig(__name__)
        #
        # print(f'Config: {__name__}')

    def get_config(self):
        # config = self._mw.addonManager.getConfig(__name__)
        config = self.config
        for field in self.fields:
            if field not in self.config:
                config[field] = Config.DEFAULT_CONFIG[field]
        return config

    def set_config(self, new_conf):
        self._mw.col.set_config(__name__, new_conf)
