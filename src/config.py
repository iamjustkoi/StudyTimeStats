# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

import re

from anki import buildinfo
from aqt import AnkiQt

from .consts import CELL_HTML_SHELL, CURRENT_VERSION, Config, Direction, Macro, Range, String

ANKI_VERSION = int(buildinfo.version.replace('2.1.', ''))


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

        self.decks = self.mw.col.decks if self.mw.col is not None else None

        # Add a constant key to meta
        self._meta['config'] = self.config

    def write_config(self):
        """
        Writes the config manager's current values to the addon meta file.
        """
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)

    def write_config_val(self, key: str, val):
        """
        Creates a shallow copy of the current config and writes a single value to the addon meta file
        using the shallow copy as a template.
        """
        config = self._init_config(deep=False)
        config[key] = val
        meta = self.mw.addonManager.addonMeta(self._addon)
        meta['config'] = config
        self.mw.addonManager.writeAddonMeta(self._addon, meta)

    def _init_config(self, deep=True):
        meta = self._meta if deep else self.mw.addonManager.addonMeta(self._addon)
        config = meta.get('config', Config.DEFAULT_CONFIG.copy())
        config = _reformat_conf(config) if deep else config
        for field in Config.DEFAULT_CONFIG:
            if field not in config:
                # load temp defaults
                config[field] = Config.DEFAULT_CONFIG[field]

        return config


def _reformat_conf(config: dict):
    """
    Handles the addon's config updates/patching pipeline.

    :param config: The current config for the addon.
    :return: An updated addon config with updated formatting/patched changes.
    """
    addon_ver = config.get(Config.VERSION, '0.0.0')
    formatted_addon_ver = re.sub('-.*', '', addon_ver)
    ver_numbers: list[int] = [int(n) for n in formatted_addon_ver.split('.')]

    # v1.3.5
    # Replaces "%from_custom_date" with the updated, custom-date-range hours macro.
    if ver_numbers[0] <= 1 and ver_numbers[1] <= 3 and ver_numbers[2] <= 5:
        def replace_macro(outer_conf: dict):
            for field in outer_conf:
                data = outer_conf[field]
                if isinstance(data, str) and re.match(fr'.*(?<!%)%from_custom_date:.*', data):
                    outer_conf[field] = data.replace('%from_custom_date:', Macro.CMD_FROM_DATE_HOURS)
                elif isinstance(data, dict):
                    replace_macro(data)

        replace_macro(config)

    # v2.0.0
    # Initializes cells to the legacy types (total/range), given they're currently unhidden.
    if ver_numbers[0] < 2 and not config.get(Config.CELLS_DATA, None):
        cells = []
        default_data = Config.DEFAULT_CELL_DATA.copy()

        if not config.get('Hide_Total_Stat', False):
            cells.append(
                {
                    Config.TITLE: config.get('Custom_Total_Text', String.TOTAL),
                    Config.OUTPUT: config.get('Custom_Total_Hrs', Macro.CMD_RANGE_HOURS),
                    Config.TITLE_COLOR: config.get('Primary_Color', default_data[Config.TITLE_COLOR]),
                    Config.OUTPUT_COLOR: config.get('Secondary_Color', default_data[Config.OUTPUT_COLOR]),
                    Config.DIRECTION: Direction.VERTICAL,
                    Config.RANGE: Range.TOTAL,
                    Config.USE_CALENDAR: default_data[Config.USE_CALENDAR],
                    Config.WEEK_START: default_data[Config.WEEK_START],
                    Config.DAYS: default_data[Config.DAYS],
                    Config.HRS_UNIT: config.get('Custom_Hrs_Text', default_data[Config.HRS_UNIT]),
                    Config.MIN_UNIT: config.get('Custom_Min_Text', default_data[Config.MIN_UNIT]),
                    Config.HTML: CELL_HTML_SHELL,
                }
            )

        if not config.get('Hide_Ranged_Stat', False):
            cells.append(
                {
                    Config.TITLE: config.get('Custom_Range_Text', String.PAST_RANGE),
                    Config.OUTPUT: config.get('Custom_Range_Hrs', Macro.CMD_RANGE_HOURS),
                    Config.TITLE_COLOR: config.get('Primary_Color', default_data[Config.TITLE_COLOR]),
                    Config.OUTPUT_COLOR: config.get('Secondary_Color', default_data[Config.OUTPUT_COLOR]),
                    Config.DIRECTION: Direction.VERTICAL,
                    Config.RANGE: config.get('Range_Type', default_data[Config.RANGE]),
                    Config.USE_CALENDAR: config.get('Use_Calendar_Range', default_data[Config.USE_CALENDAR]),
                    Config.WEEK_START: config.get('Week_Start', default_data[Config.WEEK_START]),
                    Config.DAYS: config.get('Custom_Days', default_data[Config.DAYS]),
                    Config.HRS_UNIT: config.get('Custom_Hrs_Text', default_data[Config.HRS_UNIT]),
                    Config.MIN_UNIT: config.get('Custom_Min_Text', default_data[Config.MIN_UNIT]),
                    Config.HTML: CELL_HTML_SHELL,
                }
            )

        config[Config.CELLS_DATA] = cells

    config[Config.VERSION] = CURRENT_VERSION

    return config
