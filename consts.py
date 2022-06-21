class Text:
    TOTAL = 'Total'
    PAST_WEEK = 'Past Week'
    HRS = 'hrs'
    MIN = 'min'
    OPTIONS_ACTION = 'Study Time Stats Options...'


class Range:
    WEEK = 'Week'
    TWO_WEEKS = '2 Weeks'
    MONTH = 'Month'
    YEAR = 'Year'
    CUSTOM = 'Custom'
    DAYS = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365, CUSTOM: 0}


class Days:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6


class Config:
    WEEK_START = 'week_start'
    DEFAULTS = {WEEK_START: Days.SUNDAY}
