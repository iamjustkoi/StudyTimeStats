from aqt import AnkiQt

from .consts import Config


class TimeStatsConfigManager:
    """
    Generic config manager for accessing and storing add-on's properties.
    """

    def __init__(self, mw: AnkiQt, max_filter_range: int):
        super().__init__()
        self.mw = mw
        self._addon = self.mw.addonManager.addonFromModule(__name__)
        self._meta = self.mw.addonManager.addonMeta(self._addon)

        self.config = self._meta.get('config', Config.DEFAULT_CONFIG)
        self.decks = self.mw.col.decks
        self.max_range = max_filter_range

        for field in Config.DEFAULT_CONFIG:
            if field not in self.config:
                # load temp defaults
                self.config[field] = Config.DEFAULT_CONFIG[field]

        self._meta['config'] = self.config

    def write_config(self):
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)
