class Text:
    TOTAL = 'Total'
    PAST_WEEK = 'Past Week'
    HRS = 'hrs'
    MIN = 'min'
    OPTIONS_ACTION = 'Study Time Stats Options...'
    USE_CALENDAR = 'Use Calendar'
    DAYS = 'Days'
    WEEK = 'Week'
    TWO_WEEKS = '2 Weeks'
    MONTH = 'Month'
    YEAR = 'Year'


class RangeType:
    WEEK, TWO_WEEKS, MONTH, YEAR, CUSTOM = 0, 1, 2, 3, 4
    DAYS = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365, CUSTOM: 0}
    TEXT = {
        WEEK: Text.WEEK,
        TWO_WEEKS: Text.TWO_WEEKS,
        MONTH: Text.MONTH,
        YEAR: Text.YEAR
    }


class Weekday:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6


class Config:
    WEEK_START = 'Week_Start'
    USE_CALENDAR_RANGE = 'Use_Calendar_Range'
    RANGE_TYPE = 'Range_Type'
    CUSTOM_RANGE = 'Custom_Range'
    CUSTOM_TOTAL_TEXT = 'Custom_Total_Text'
    CUSTOM_RANGE_TEXT = 'Custom_Range_Text'
    PRIMARY_COLOR = 'Primary_Color'
    SECONDARY_COLOR = 'Secondary_Color'
    BROWSER_ENABLED = 'Browser_Enabled'
    OVERVIEW_ENABLED = 'Overview_Enabled'
    CONGRATS_ENABLED = 'Congrats_Enabled'
    EXCLUDED_DIDS = "Excluded_Deck_IDs"
    DEFAULT_CONFIG = {
        WEEK_START: Weekday.SUNDAY,
        USE_CALENDAR_RANGE: True,
        RANGE_TYPE: RangeType.WEEK,
        CUSTOM_RANGE: 7,
        CUSTOM_TOTAL_TEXT: 'Total',
        CUSTOM_RANGE_TEXT: 'Past %range',
        PRIMARY_COLOR: 'white',
        SECONDARY_COLOR: '#80e179',
        BROWSER_ENABLED: True,
        OVERVIEW_ENABLED: True,
        CONGRATS_ENABLED: True,
        EXCLUDED_DIDS: [1]
    }


SPECIAL_DATE = '2006-10-05'
