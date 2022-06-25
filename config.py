from aqt import AnkiQt

from .consts import Config


class DeckManager:
    def name(self, did: int or str):
        return None

    def id(self, name: str, create: bool = False):
        return None
    pass


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
        self.decks = self.mw.col.decks if self.mw.col is not None else None
        self.max_range = max_filter_range

        for field in Config.DEFAULT_CONFIG:
            if field not in self.config:
                # load temp defaults
                self.config[field] = Config.DEFAULT_CONFIG[field]

        self._meta['config'] = self.config

    def get_decks(self):
        decks_shell = DeckManager
        return self.mw.col.decks if self.mw.col is not None else decks_shell

    def write_config(self):
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)
