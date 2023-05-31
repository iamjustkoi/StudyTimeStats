# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

from aqt.qt import QT_VERSION_STR
from aqt.theme import theme_manager

CURRENT_VERSION = '2.0.4'

ANKI_LEGACY_VER = 35
ANKI_DEFAULT_ROLLOVER = 4
ANKI_QT_VER = int(QT_VERSION_STR.split('.')[0])

UNIQUE_DATE = '2006-10-05'

ADDON_ICON_PATH = '../res/img/stats_icon.svg'
HEART_ICON_PATH = '../res/img/heart_icon.svg'
KOFI_ICON_PATH = '../res/img/kofilogo_blue.PNG'
PATREON_ICON_PATH = '../res/img/patreon.png'
ANKI_LIKE_ICON_PATH = '../res/img/anki_like.png'

REMOVE_ICON_PATH = '../res/img/remove_icon.svg'
ADD_ICON_PATH = '../res/img/add_icon.svg'
CODE_ICON_PATH = '../res/img/code_icon.svg'
CHEVRON_ICON_PATH = '../res/img/chevron_down.svg'
VERT_LINES_PATH = '../res/img/vert_lines.svg'
HORIZ_LINES_PATH = '../res/img/horiz_lines.svg'
HANDLES_PATH = '../res/img/vert_grip.svg'

PATREON_URL = 'https://www.patreon.com/iamjustkoi'
KOFI_URL = 'https://ko-fi.com/iamjustkoi'
ANKI_URL = 'https://ankiweb.net/shared/info/1247171202'

TABLE_ID = 'sts-table'
COL_CLASS = 'sts-col'
HORIZ_CELL_CLASS = 'flow-horizontal'
VERT_CELL_CLASS = 'flow-vertical'
HTML_SHELL = '''
         <style>
             #''' + TABLE_ID + ''' {
                 display: table;
                 margin-top: .5em;
                 max-width: fit-content;
                 font-weight: normal;
             }
             .''' + COL_CLASS + ''' {
                 display: table-cell;
                 width: 30vw;
                 max-width: 200px;
             }
             .''' + HORIZ_CELL_CLASS + ''' {
                 display: flex !important; 
                 max-width: fit-content;
                 justify-content: space-evenly;
                 word-break: break-word;
             }
             .''' + HORIZ_CELL_CLASS + ''' > * {
                 padding: 0 2px 0 2px;
                 width: fit-content;
             }
             .''' + VERT_CELL_CLASS + ''' > * {
                 width: max-content;
                 max-width: fit-content;
                 word-break: break-word;
             }
         </style>
         <center>
             <div id="''' + TABLE_ID + '''">
                {cell_data}
             </div>
         </center>
'''

CELL_HTML_SHELL = '''<div class="{{CellClass}}">
    <div style="color: {{TitleColor}};">{{Title}}</div>
    <div style="color: {{OutputColor}}; font-weight: bold;">{{Output}}</div>
</div>
'''

SUSPENDED = 'suspended'
LEARN = 'learn'
RELEARN = 'relearn'
REVIEW = 'review'
NEW = 'new'
SIB_BURIED = 'sib_buried'
MAN_BURIED = 'man_buried'
BURIED = 'buried'


class Macro:
    # Text
    CMD_RANGE = '%range'
    CMD_DATE = '%from_date'
    CMD_YEAR = '%from_year'
    CMD_FULL_DAY = '%from_full_day'
    CMD_DAY = '%from_day'
    CMD_DAYS = '%days'
    CMD_DATE_FORMATTED = r'%from_date:strf\{".*\"}'

    CMD_MONTH = '%from_month'
    CMD_FULL_MONTH = '%from_full_month'

    # Time
    CMD_TOTAL_HOURS = '%total_hrs'

    CMD_RANGE_HOURS = '%range_hrs'
    CMD_DAY_HOURS = '%day_hrs'
    CMD_WEEK_HOURS = '%week_hrs'
    CMD_TWO_WEEKS_HOURS = '%two_week_hrs'
    CMD_MONTH_HOURS = '%month_hrs'
    CMD_YEAR_HOURS = '%year_hrs'

    CMD_ETA_HOURS = '%eta_hrs'

    CMD_HIGHEST_DAY_HOURS = '%highest_day_hrs'
    CMD_HIGHEST_WEEK_HOURS = '%highest_week_hrs'
    CMD_HIGHEST_MONTH_HOURS = '%highest_month_hrs'
    CMD_HIGHEST_YEAR_HOURS = '%highest_year_hrs'

    # Avg
    CMD_CARD_AVERAGE_HOURS = '%card_avg_hrs'
    CMD_DAY_AVERAGE_HOURS = '%day_avg_hrs'

    # Previous Time
    CMD_PREVIOUS_RANGE_HOURS = '%prev_range_hrs'
    CMD_PREVIOUS_DAY_HOURS = '%prev_day_hrs'
    CMD_PREVIOUS_WEEK_HOURS = '%prev_week_hrs'
    CMD_PREVIOUS_TWO_WEEKS_HOURS = '%prev_two_week_hrs'
    CMD_PREVIOUS_MONTH_HOURS = '%prev_month_hrs'
    CMD_PREVIOUS_YEAR_HOURS = '%prev_year_hrs'
    CMD_FROM_DATE_HOURS = '%from_custom_hrs'

    # Reviews
    CMD_TOTAL_REVIEWS = '%total_rev'
    CMD_RANGE_REVIEWS = '%range_rev'
    CMD_DAY_REVIEWS = '%day_rev'
    CMD_WEEK_REVIEWS = '%week_rev'
    CMD_TWO_WEEKS_REVIEWS = '%two_week_rev'
    CMD_MONTH_REVIEWS = '%month_rev'
    CMD_YEAR_REVIEWS = '%year_rev'

    CMD_PREVIOUS_RANGE_REVIEWS = '%prev_range_rev'
    CMD_PREVIOUS_DAY_REVIEWS = '%prev_day_rev'
    CMD_PREVIOUS_WEEK_REVIEWS = '%prev_week_rev'
    CMD_PREVIOUS_TWO_WEEKS_REVIEWS = '%prev_two_week_rev'
    CMD_PREVIOUS_MONTH_REVIEWS = '%prev_month_rev'
    CMD_PREVIOUS_YEAR_REVIEWS = '%prev_year_rev'
    CMD_FROM_DATE_REVIEWS = '%from_custom_rev'

    CMD_HIGHEST_DAY_REVIEWS = '%highest_day_rev'
    CMD_HIGHEST_WEEK_REVIEWS = '%highest_week_rev'
    CMD_HIGHEST_MONTH_REVIEWS = '%highest_month_rev'
    CMD_HIGHEST_YEAR_REVIEWS = '%highest_year_rev'

    # Misc
    CMD_EVAL = '%eval{'

    CMD_PRECISION = r':p'
    PRECISION_EXTRA = r'\d*'

    CMD_STATE = r':state'
    STATE_EXTRA = r'[\w,]*'

    # Definitions for all macros
    DEFINITIONS = {
        # Text
        CMD_RANGE:
            '''label for the currently selected range''',
        CMD_DATE:
            '''current range's start date using the system's locale''',
        CMD_YEAR:
            '''current range's year''',
        CMD_FULL_DAY:
            '''range filter's full start day''',
        CMD_DAY:
            '''range filter's starting day using a compact format''',
        CMD_DAYS:
            '''total days the range filter checks against''',
        CMD_DATE_FORMATTED:
            '''formatted date string using the current range's from-date (e.g. %from_date:strf{"%x"} -> 2022-01-01)''',
        CMD_MONTH:
            '''range filter's month name using a compact format''',
        CMD_FULL_MONTH:
            '''range filter's full month name''',

        # Time
        CMD_TOTAL_HOURS:
            '''total study time''',
        CMD_RANGE_HOURS:
            '''total study time for the current range''',

        CMD_DAY_HOURS:
            '''total study time for the past day''',
        CMD_WEEK_HOURS:
            '''total study time for the past week''',
        CMD_TWO_WEEKS_HOURS:
            '''total study time for the past two weeks''',
        CMD_MONTH_HOURS:
            '''total study time for the past month''',
        CMD_YEAR_HOURS:
            '''total study time for the past year''',

        CMD_ETA_HOURS:
            '''estimated study time for the current card queue''',

        CMD_HIGHEST_DAY_HOURS:
            '''highest total study time for all days in the current range''',
        CMD_HIGHEST_WEEK_HOURS:
            '''highest total study time for all weeks in the current range''',
        CMD_HIGHEST_MONTH_HOURS:
            '''highest total study time for all months in the current range''',
        CMD_HIGHEST_YEAR_HOURS:
            '''highest total study time for all years in the current range''',

        # Avg
        CMD_CARD_AVERAGE_HOURS:
            '''average study time per card for the current range''',
        CMD_DAY_AVERAGE_HOURS:
            '''average study time per day for the current range''',

        # Previous Time
        CMD_PREVIOUS_RANGE_HOURS:
            '''total study time for the previous range''',
        CMD_PREVIOUS_DAY_HOURS:
            '''total study time for the previous day''',
        CMD_PREVIOUS_WEEK_HOURS:
            '''total study time for the previous week''',
        CMD_PREVIOUS_TWO_WEEKS_HOURS:
            '''total study time for the previous two weeks''',
        CMD_PREVIOUS_MONTH_HOURS:
            '''total study time for the previous month''',
        CMD_PREVIOUS_YEAR_HOURS:
            '''total study time for the previous year''',

        CMD_FROM_DATE_HOURS:
            '''total study time for a custom date range (%from_custom_hrs:<from>:<to> (YYYY-MM-DD))''',

        # Reviews
        CMD_TOTAL_REVIEWS:
            '''total reviews''',
        CMD_RANGE_REVIEWS:
            '''total reviews for the current range''',

        CMD_DAY_REVIEWS:
            '''total reviews for the past day''',
        CMD_WEEK_REVIEWS:
            '''total reviews for the past week''',
        CMD_TWO_WEEKS_REVIEWS:
            '''total reviews for the past two weeks''',
        CMD_MONTH_REVIEWS:
            '''total reviews for the past month''',
        CMD_YEAR_REVIEWS:
            '''total reviews for the past year''',

        CMD_PREVIOUS_RANGE_REVIEWS:
            '''total reviews for the previous range''',
        CMD_PREVIOUS_DAY_REVIEWS:
            '''total reviews for the previous day''',
        CMD_PREVIOUS_WEEK_REVIEWS:
            '''total reviews for the previous week''',
        CMD_PREVIOUS_TWO_WEEKS_REVIEWS:
            '''total reviews for the previous two weeks''',
        CMD_PREVIOUS_MONTH_REVIEWS:
            '''total reviews for the previous month''',
        CMD_PREVIOUS_YEAR_REVIEWS:
            '''total reviews for the previous year''',

        CMD_FROM_DATE_REVIEWS:
            '''total reviews for a custom date range (%from_custom_hrs:<from>:<to> (YYYY-MM-DD))''',

        CMD_HIGHEST_DAY_REVIEWS:
            '''highest total reviews for all days in the current range''',
        CMD_HIGHEST_WEEK_REVIEWS:
            '''highest total reviews for all weeks in the current range''',
        CMD_HIGHEST_MONTH_REVIEWS:
            '''highest total reviews for all months in the current range''',
        CMD_HIGHEST_YEAR_REVIEWS:
            '''highest total reviews for all years in the current range''',

        # Misc
        CMD_EVAL:
            '''customized output that accepts any macros, math, or python as input (warning: unsafe implementation)''',

        CMD_PRECISION:
            '''filters an output's precision for time-based, decimal macros (%range_hrs:p{<0-4>})''',

        CMD_STATE:
            '''filters an output to the current state of a card, separated by commas'''
            f''' (%range_hrs:state{{<{NEW}/{LEARN}/{REVIEW}/{SUSPENDED}/{BURIED}>}},'''
            f''' e.g. %range_hrs:state{{{LEARN},{REVIEW}}})''',
    }


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
    ENABLE_ACTION = '&Enable'
    DISABLE_ACTION = '&Disable'
    INSERT = 'Insert'
    ERR = 'ERR'
    DELETE_CELL = 'Delete view?'


class Range:
    TOTAL, WEEK, TWO_WEEKS, MONTH, YEAR, CUSTOM = -1, 0, 1, 2, 3, 4
    DAYS_IN = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365, CUSTOM: 1}
    LABEL = {WEEK: String.WEEK, TWO_WEEKS: String.TWO_WEEKS, MONTH: String.MONTH, YEAR: String.YEAR}


class Weekday:
    SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY = 0, 1, 2, 3, 4, 5, 6


class Direction:
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'


class Color:
    # [Light, Dark]
    HOVER = ['#040404', '#b0b0b0']
    BUTTON_ICON = ['#808080', '#8a8a8a']
    TITLE_DEFAULT = ['#000000', '#FFFFFF']
    OUTPUT_DEFAULT = ['#76bfb4', '#76bfb4']
    BUTTON_ACTIVE = ['#cacaca', '#5b5b5b']


class Config:
    TOOLBAR_ENABLED = 'Use_Toolbar_Options'
    CUSTOM_DAYS = 'Custom_Days'
    CUSTOM_TOTAL_TEXT = 'Custom_Total_Text'
    CUSTOM_RANGE_TEXT = 'Custom_Range_Text'
    CUSTOM_TOTAL_HOURS = 'Custom_Total_Hrs'
    CUSTOM_RANGE_HOURS = 'Custom_Range_Hrs'
    CUSTOM_HOURS_TEXT = 'Custom_Hrs_Text'
    CUSTOM_MIN_TEXT = 'Custom_Min_Text'
    BROWSER_ENABLED = 'Browser_Enabled'
    OVERVIEW_ENABLED = 'Overview_Enabled'
    CONGRATS_ENABLED = 'Congrats_Enabled'
    INCLUDE_DELETED = 'Include_Deleted_Reviews'
    USE_ROLLOVER = 'Use_Rollover_Hour'
    USE_DECIMAL = 'Use_Decimal_Format'
    EXCLUDED_DIDS = "Excluded_Deck_IDs"
    CELLS_DATA = "cellsData"
    WIN_SIZE = 'winSize'
    VERSION = 'version'

    TITLE = 'title'
    OUTPUT = 'output'
    TITLE_COLOR = 'titleColor'
    OUTPUT_COLOR = 'outputColor'
    DIRECTION = 'direction'
    RANGE = 'range'
    USE_CALENDAR = 'useCalendar'
    WEEK_START = 'weekStart'
    DAYS = 'days'
    HRS_UNIT = 'hrsUnit'
    MIN_UNIT = 'minUnit'
    HTML = 'html'
    DEFAULT_CELL_DATA = {
        TITLE: String.PAST_RANGE,
        OUTPUT: Macro.CMD_RANGE_HOURS,
        TITLE_COLOR: Color.TITLE_DEFAULT[theme_manager.get_night_mode()],
        OUTPUT_COLOR: Color.OUTPUT_DEFAULT[theme_manager.get_night_mode()],
        DIRECTION: Direction.VERTICAL,
        RANGE: Range.WEEK,
        USE_CALENDAR: True,
        WEEK_START: Weekday.SUNDAY,
        DAYS: 7,
        HRS_UNIT: String.HRS,
        MIN_UNIT: String.MIN,
        HTML: CELL_HTML_SHELL,
    }

    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        BROWSER_ENABLED: True,
        OVERVIEW_ENABLED: True,
        CONGRATS_ENABLED: True,
        INCLUDE_DELETED: True,
        USE_ROLLOVER: True,
        USE_DECIMAL: True,
        EXCLUDED_DIDS: [1],
        CELLS_DATA: [
            {
                TITLE: String.TOTAL,
                OUTPUT: Macro.CMD_RANGE_HOURS,
                TITLE_COLOR: Color.TITLE_DEFAULT[theme_manager.get_night_mode()],
                OUTPUT_COLOR: Color.OUTPUT_DEFAULT[theme_manager.get_night_mode()],
                DIRECTION: Direction.VERTICAL,
                RANGE: Range.TOTAL,
                USE_CALENDAR: True,
                WEEK_START: Weekday.SUNDAY,
                DAYS: 7,
                HRS_UNIT: String.HRS,
                MIN_UNIT: String.MIN,
                HTML: CELL_HTML_SHELL,
            },
            {
                TITLE: String.PAST_RANGE,
                OUTPUT: Macro.CMD_RANGE_HOURS,
                TITLE_COLOR: Color.TITLE_DEFAULT[theme_manager.get_night_mode()],
                OUTPUT_COLOR: Color.OUTPUT_DEFAULT[theme_manager.get_night_mode()],
                DIRECTION: Direction.VERTICAL,
                RANGE: Range.WEEK,
                USE_CALENDAR: True,
                WEEK_START: Weekday.SUNDAY,
                DAYS: 7,
                HRS_UNIT: String.HRS,
                MIN_UNIT: String.MIN,
                HTML: CELL_HTML_SHELL,
            }
        ]
    }
