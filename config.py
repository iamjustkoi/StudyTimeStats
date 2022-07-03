"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file, located in the add-on's root directory.
"""
from aqt import AnkiQt

from .consts import Config


class TimeStatsConfigManager:

    def __init__(self, mw: AnkiQt, max_filter_range: int):
        """
Generic config manager for accessing and writing addon config values.

    :param mw: Anki window to retrieve addon and other data from
    :param max_filter_range: maximum days the addon can filter through
        """
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

    # TODO: Check if config is not default and write if config was changed to meta file
    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)
