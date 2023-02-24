# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

import re

from anki import buildinfo
from aqt import AnkiQt

from .consts import Macro, Config

ANKI_VERSION = int(buildinfo.version.replace('2.1.', ''))


def _reformat_conf(config: dict):
    """
    Handles addon config update pipelines.
    :param config: The current config for the addon.
    :return: An updated addon config with some redone formatting.
    """
    for field in config:
        data = config[field]
        if isinstance(data, str):
            if re.match(fr'.*(?<!%)%from_custom_date:.*', data):
                config[field] = data.replace('%from_custom_date:', Macro.CMD_FROM_DATE_HRS)
        elif isinstance(data, dict):
            _reformat_conf(data)
    return config


class TimeStatsConfigManager:

    def __init__(self, mw: AnkiQt):
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
        self.config = _reformat_conf(self.config)
        self.decks = self.mw.col.decks if self.mw.col is not None else None
        # self.max_range = max_filter_range

        for field in Config.DEFAULT_CONFIG:
            if field not in self.config:
                # load temp defaults
                self.config[field] = Config.DEFAULT_CONFIG[field]

        self._meta['config'] = self.config

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)
