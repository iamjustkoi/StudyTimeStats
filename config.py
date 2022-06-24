from aqt import AnkiQt

from .consts import Config


class TimeStatsConfigManager:
    """
    Generic config manager for accessing and storing add-on's properties.
    """

    def __init__(self, mw: AnkiQt):
        super().__init__()
        self._mw = mw
        self._addon = self._mw.addonManager.addonFromModule(__name__)
        self._meta = self._mw.addonManager.addonMeta(self._addon)

        self.config = self._meta.get('config', Config.DEFAULT_CONFIG)

        for field in Config.DEFAULT_CONFIG:
            if field not in self.config:
                # load temp defaults
                self.config[field] = Config.DEFAULT_CONFIG[field]

        self._meta['config'] = self.config

    def write_config(self):
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)
