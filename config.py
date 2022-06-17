from aqt import AnkiQt
from .consts import CONFIG_DEFAULTS, CONFIG_WEEK_START


class TimeStatsConfigManager:
    fields = {CONFIG_WEEK_START}
    _mw = None

    def __init__(self, mw: AnkiQt):
        self._mw = mw
        self.config = mw.col.get_config(__name__, default=CONFIG_DEFAULTS)
        print(f'Conf name: {__name__}')
        self._mw.col.set_config(__name__, self.config)
