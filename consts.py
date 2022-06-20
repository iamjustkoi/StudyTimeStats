class Text:
    TOTAL = 'Total'
    PAST_WEEK = 'Past Week'
    HRS = 'hrs'
    MIN = 'min'
    OPTIONS_ACTION = 'Overview Time Stats Options...'


class Days:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6


CONFIG_WEEK_START = 'weekStart'
CONFIG_DEFAULTS = {CONFIG_WEEK_START: Days.SUNDAY}
