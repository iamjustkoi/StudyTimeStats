"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file, located in the add-on's root directory.
"""

CURRENT_VERSION = '1.2.2a'

ANKI_LEGACY_VER = 35
ANKI_DEFAULT_ROLLOVER = 4
UNIQUE_DATE = '2006-10-05'
CMD_RANGE = '%range'
CMD_DATE = '%from_date'
CMD_YEAR = '%from_year'
CMD_FULL_DAY = '%from_full_day'
CMD_DAY = '%from_day'
CMD_DAYS = '%days'
ICON_PATH = 'raw\\icon.svg'
KOFI_FILEPATH = 'raw\\kofilogo_blue.PNG'
PATREON_FILEPATH = 'raw\\patreon.png'
PATREON_URL = 'https://www.patreon.com/iamjustkoi'
KOFI_URL = 'https://ko-fi.com/iamjustkoi'


class String:
    TOTAL = 'Total'
    PAST_RANGE = 'Past %range'
    HRS = 'hrs'
    MIN = 'min'
    OPTIONS_ACTION = 'Study &Time Stats Options...'
    USE_CALENDAR = 'Use Calendar'
    DAYS = 'Days'
    WEEK = 'Week'
    TWO_WEEKS = '2 Weeks'
    MONTH = 'Month'
    YEAR = 'Year'
    COPY_LINK_ACTION = 'Copy &Link Location'


class Range:
    WEEK, TWO_WEEKS, MONTH, YEAR, CUSTOM = 0, 1, 2, 3, 4
    DAYS_IN = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365}
    LABEL = {WEEK: String.WEEK, TWO_WEEKS: String.TWO_WEEKS, MONTH: String.MONTH, YEAR: String.YEAR}


class Weekday:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6


class Config:
    TOOLBAR_ENABLED = 'Use_Toolbar_Options'
    WEEK_START = 'Week_Start'
    USE_CALENDAR_RANGE = 'Use_Calendar_Range'
    RANGE_TYPE = 'Range_Type'
    CUSTOM_DAYS = 'Custom_Days'
    CUSTOM_TOTAL_TEXT = 'Custom_Total_Text'
    CUSTOM_RANGE_TEXT = 'Custom_Range_Text'
    CUSTOM_HRS_TEXT = 'Custom_Hrs_Text'
    CUSTOM_MIN_TEXT = 'Custom_Min_Text'
    SHOW_TOTAL = 'Hide_Total_Stat'
    SHOW_RANGED = 'Hide_Ranged_Stat'
    PRIMARY_COLOR = 'Primary_Color'
    SECONDARY_COLOR = 'Secondary_Color'
    BROWSER_ENABLED = 'Browser_Enabled'
    OVERVIEW_ENABLED = 'Overview_Enabled'
    CONGRATS_ENABLED = 'Congrats_Enabled'
    EXCLUDED_DIDS = "Excluded_Deck_IDs"
    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        WEEK_START: Weekday.SUNDAY,
        USE_CALENDAR_RANGE: True,
        RANGE_TYPE: Range.WEEK,
        CUSTOM_DAYS: 7,
        CUSTOM_TOTAL_TEXT: String.TOTAL,
        CUSTOM_RANGE_TEXT: String.PAST_RANGE,
        CUSTOM_HRS_TEXT: String.HRS,
        CUSTOM_MIN_TEXT: String.MIN,
        SHOW_TOTAL: True,
        SHOW_RANGED: True,
        PRIMARY_COLOR: 'white',
        SECONDARY_COLOR: '#76bfb4',
        BROWSER_ENABLED: True,
        OVERVIEW_ENABLED: True,
        CONGRATS_ENABLED: True,
        EXCLUDED_DIDS: [1]
    }
