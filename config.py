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
        self._addon = self._mw.addonManager.addonFromModule(__name__)
        self._meta = self._mw.addonManager.addonMeta(self._addon)
        self._config = self._meta.get("config", Config.DEFAULT_CONFIG)

    def get_config(self):
        for field in self.fields:
            if field not in self._config:
                # load temp defaults
                self._config[field] = Config.DEFAULT_CONFIG[field]
        return self._config

    def write_config(self):
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)

    # def set_config(self, new_conf):
    #     self.addon = self._mw.addonManager.addonFromModule(__name__)
    #     # self._mw.addonManager.addonMeta(self.addon)['config'] = new_conf
    #     meta = self._mw.addonManager.addon_meta(self.addon)
    #     self._mw.addonManager.write_addon_meta(meta)

