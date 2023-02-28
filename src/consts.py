# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

import aqt
from aqt.theme import theme_manager

CURRENT_VERSION = '2.0.0-b2'

ANKI_LEGACY_VER = 35
ANKI_DEFAULT_ROLLOVER = 4
UNIQUE_DATE = '2006-10-05'

ADDON_ICON_PATH = '../res/img/stats_icon.svg'
KOFI_ICON_PATH = '../res/img/kofilogo_blue.PNG'
PATREON_ICON_PATH = '../res/img/patreon.png'
ANKI_LIKE_ICON_PATH = '../res/img/anki_like.png'

REMOVE_ICON_PATH = '../res/img/remove_icon.svg'
ADD_ICON_PATH = '../res/img/add_icon.svg'
CODE_ICON_PATH = '../res/img/code_icon.svg'
VERT_LINES_PATH = '../res/img/vert_lines.svg'
HORIZ_LINES_PATH = '../res/img/horiz_lines.svg'
VERT_HANDLES_PATH = '../res/img/vert_grip.svg'

PATREON_URL = 'https://www.patreon.com/iamjustkoi'
KOFI_URL = 'https://ko-fi.com/iamjustkoi'
ANKI_URL = 'https://ankiweb.net/shared/info/1247171202'

TABLE_ID = 'sts-table'
COL_CLASS = 'sts-col'
HORIZ_CLASS = 'flow-horizontal'
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
             .''' + COL_CLASS + ''' > * {
                 display: table-row;
             }
             .''' + HORIZ_CLASS + ''' {
                 display: flex !important; 
                 width: max-content;
                 justify-content: space-evenly;
             }
             .''' + HORIZ_CLASS + ''' > * {
                 padding: 0 2px 0 2px;
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


class Macro:
    # Text
    CMD_RANGE = '%range'
    CMD_DATE = '%from_date'
    CMD_YEAR = '%from_year'
    CMD_FULL_DAY = '%from_full_day'
    CMD_DAY = '%from_day'
    CMD_DAYS = '%days'
    CMD_DATE_STRF = r'%from_date:strf\{".*\"}'

    CMD_MONTH = '%from_month'
    CMD_FULL_MONTH = '%from_full_month'

    # Time
    CMD_TOTAL_HRS = '%total_hrs'

    CMD_RANGE_HRS = '%range_hrs'
    CMD_DAY_HRS = '%day_hrs'
    CMD_WEEK_HRS = '%week_hrs'
    CMD_TWO_WEEKS_HRS = '%two_week_hrs'
    CMD_MONTH_HRS = '%month_hrs'
    CMD_YEAR_HRS = '%year_hrs'

    CMD_ETA_HRS = '%eta_hrs'

    CMD_HIGHEST_DAY_HRS = '%highest_day_hrs'

    # Avg
    CMD_CARD_AVG_HRS = '%card_avg_hrs'
    CMD_DAY_AVG_HRS = '%day_avg_hrs'

    CMD_PREV_RANGE_HRS = '%prev_range_hrs'
    CMD_PREV_DAY_HRS = '%prev_day_hrs'
    CMD_PREV_WEEK_HRS = '%prev_week_hrs'
    CMD_PREV_TWO_WEEKS_HRS = '%prev_two_week_hrs'
    CMD_PREV_MONTH_HRS = '%prev_month_hrs'
    CMD_PREV_YEAR_HRS = '%prev_year_hrs'
    CMD_FROM_DATE_HRS = '%from_custom_hrs'

    # Reviews
    CMD_TOTAL_REVIEWS = '%total_rev'
    CMD_RANGE_REVIEWS = '%range_rev'
    CMD_DAY_REVIEWS = '%day_rev'
    CMD_WEEK_REVIEWS = '%week_rev'
    CMD_TWO_WEEKS_REVIEWS = '%two_week_rev'
    CMD_MONTH_REVIEWS = '%month_rev'
    CMD_YEAR_REVIEWS = '%year_rev'

    CMD_PREV_RANGE_REVIEWS = '%prev_range_rev'
    CMD_PREV_DAY_REVIEWS = '%prev_day_rev'
    CMD_PREV_WEEK_REVIEWS = '%prev_week_rev'
    CMD_PREV_TWO_WEEKS_REVIEWS = '%prev_two_week_rev'
    CMD_PREV_MONTH_REVIEWS = '%prev_month_rev'
    CMD_PREV_YEAR_REVIEWS = '%prev_year_rev'
    CMD_FROM_DATE_REVIEWS = '%from_custom_rev'

    # Misc
    CMD_EVAL = '%eval{'


class String:
    TOTAL = 'Total'
    PAST_RANGE = 'Past %range'
    TOTAL_HRS = '%total_hrs'
    PAST_HRS = '%range_hrs'
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


class Range:
    TOTAL, WEEK, TWO_WEEKS, MONTH, YEAR, CUSTOM = -1, 0, 1, 2, 3, 4
    DAYS_IN = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365, CUSTOM: 1}
    LABEL = {WEEK: String.WEEK, TWO_WEEKS: String.TWO_WEEKS, MONTH: String.MONTH, YEAR: String.YEAR}


class Weekday:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = 0, 1, 2, 3, 4, 5, 6


class Direction:
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'


class Color:
    # [Light, Dark]
    HOVER = ['#040404', '#b0b0b0']
    BUTTON_ICON = ['#808080', '#8a8a8a']
    TITLE_DEFAULT = ['#000000', '#FFFFFF']
    OUTPUT_DEFAULT = ['#76bfb4', '#76bfb4']
    # BUTTON_ACTIVE = ['rgba(0, 0, 0, 5%)', 'rgba(255, 255, 255, 10%)']
    BUTTON_ACTIVE = ['#cacaca', '#5b5b5b']


class Config:
    TOOLBAR_ENABLED = 'Use_Toolbar_Options'
    CUSTOM_DAYS = 'Custom_Days'
    CUSTOM_TOTAL_TEXT = 'Custom_Total_Text'
    CUSTOM_RANGE_TEXT = 'Custom_Range_Text'
    CUSTOM_TOTAL_HRS = 'Custom_Total_Hrs'
    CUSTOM_RANGE_HRS = 'Custom_Range_Hrs'
    CUSTOM_HRS_TEXT = 'Custom_Hrs_Text'
    CUSTOM_MIN_TEXT = 'Custom_Min_Text'
    BROWSER_ENABLED = 'Browser_Enabled'
    OVERVIEW_ENABLED = 'Overview_Enabled'
    CONGRATS_ENABLED = 'Congrats_Enabled'
    INCLUDE_DELETED = 'Include_Deleted_Reviews'
    USE_ROLLOVER = 'Use_Rollover_Hour'
    EXCLUDED_DIDS = "Excluded_Deck_IDs"
    CELLS_DATA = "cellsData"

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
        OUTPUT: String.PAST_HRS,
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
    }

    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        BROWSER_ENABLED: True,
        OVERVIEW_ENABLED: True,
        CONGRATS_ENABLED: True,
        INCLUDE_DELETED: True,
        USE_ROLLOVER: False,
        EXCLUDED_DIDS: [1],
        CELLS_DATA: []
    }
