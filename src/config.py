# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

import re

from anki import buildinfo
from aqt import AnkiQt

from .consts import Config, Macro

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
                config[field] = data.replace('%from_custom_date:', Macro.CMD_FROM_DATE_HOURS)
        elif isinstance(data, dict):
            _reformat_conf(data)
    return config


class TimeStatsConfigManager:

    def __init__(self, mw: AnkiQt):
        """
        Generic config manager for accessing and writing addon config values.

        :param mw: Anki window to retrieve addon and other data from
        """
        super().__init__()
        self.mw = mw
        self._addon = self.mw.addonManager.addonFromModule(__name__)
        self._meta = self.mw.addonManager.addonMeta(self._addon)

        self.config = self._init_config()

        # self.config = self._meta.get('config', Config.DEFAULT_CONFIG)
        # self.config = _reformat_conf(self.config)
        # for field in Config.DEFAULT_CONFIG:
        #     if field not in self.config:
        #         # load temp defaults
        #         self.config[field] = Config.DEFAULT_CONFIG[field]

        self.decks = self.mw.col.decks if self.mw.col is not None else None

        # Add a constant key to meta
        self._meta['config'] = self.config

    def _init_config(self, deep=True):
        meta = self._meta if deep else self.mw.addonManager.addonMeta(self._addon)
        config = meta.get('config', Config.DEFAULT_CONFIG.copy())
        config = _reformat_conf(config) if deep else config
        for field in Config.DEFAULT_CONFIG:
            if field not in config:
                # load temp defaults
                config[field] = Config.DEFAULT_CONFIG[field]

        return config

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)

    def write_config_val(self, key: str, val):
        config = self._init_config(deep=False)
        config[key] = val
        meta = self.mw.addonManager.addonMeta(self._addon)
        meta['config'] = config
        self.mw.addonManager.writeAddonMeta(self._addon, meta)
