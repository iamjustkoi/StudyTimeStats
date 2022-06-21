import anki.config
from aqt import AnkiQt
from .consts import Config


class StudyTimeStatsConfig:
    """
    Generic config manager for accessing and storing the add-on's properties.
    """

    fields = {Config.WEEK_START}

    def __init__(self, mw: AnkiQt):
        self._mw = mw
        self.config = mw.col.get_config(__name__, default=Config.DEFAULTS)
        self._mw.col.set_config(__name__, self.config)

        print(f'Config: {__name__}')

    def get_config(self):
        config = anki.config.ConfigManager(self._mw.col.conf.get_config(__name__, {}))
        for field in self.fields:
            if field not in config:
                config[field] = Config.DEFAULTS[field]
        return config

    def set_config(self, new_conf):
        conf_manager = self._mw.col.conf
        if __name__ not in conf_manager:
            conf_manager[__name__] = {}
        for field in self.fields:
            conf_manager[__name__][field] = new_conf[field]
