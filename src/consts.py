"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in the "LICENSE" file, packaged with the add-on.
"""

CURRENT_VERSION = '1.3.7'

ANKI_LEGACY_VER = 35
ANKI_DEFAULT_ROLLOVER = 4
UNIQUE_DATE = '2006-10-05'
CMD_RANGE = '%range'
CMD_DATE = '%from_date'
CMD_YEAR = '%from_year'
CMD_FULL_DAY = '%from_full_day'
CMD_DAY = '%from_day'
CMD_DAYS = '%days'

CMD_MONTH = '%from_month'
CMD_FULL_MONTH = '%from_full_month'

CMD_TOTAL_HRS = '%total_hrs'

CMD_RANGE_HRS = '%range_hrs'
CMD_DAY_HRS = '%day_hrs'
CMD_WEEK_HRS = '%week_hrs'
CMD_TWO_WEEKS_HRS = '%two_week_hrs'
CMD_MONTH_HRS = '%month_hrs'
CMD_YEAR_HRS = '%year_hrs'

CMD_PREV_RANGE_HRS = '%prev_range_hrs'
CMD_PREV_DAY_HRS = '%prev_day_hrs'
CMD_PREV_WEEK_HRS = '%prev_week_hrs'
CMD_PREV_TWO_WEEKS_HRS = '%prev_two_week_hrs'
CMD_PREV_MONTH_HRS = '%prev_month_hrs'
CMD_PREV_YEAR_HRS = '%prev_year_hrs'

CMD_FROM_DATE_HRS = '%from_custom_hrs:'

ICON_PATH = '../res/img/stats_icon.svg'
KOFI_ICON_PATH = '../res/img/kofilogo_blue.PNG'
PATREON_ICON_PATH = '../res/img/patreon.png'
ANKI_LIKE_ICON_PATH = '../res/img/anki_like.png'

PATREON_URL = 'https://www.patreon.com/iamjustkoi'
KOFI_URL = 'https://ko-fi.com/iamjustkoi'
ANKI_URL = 'https://ankiweb.net/shared/info/1247171202'

TABLE_ID, COL_ID, LABEL_ID, DATA_ID = 'sts-table', 'sts-col', 'sts-label', 'sts-data'
HTML_SHELL = f'''
        <style>
            #{TABLE_ID} {{{{
                display: table;
                margin-top: .5em;
                max-width: fit-content;
                font-weight: normal;
            }}}}
            .{COL_ID} {{{{
                display: table-cell;
                word-break: break-all;
                width: 30vw;
                max-width: 200px;
            }}}}
            .{COL_ID} > * {{{{
                display: table-row;
            }}}}
            .{LABEL_ID} {{{{
                color: {{primary_color}};
            }}}}
            .{DATA_ID} {{{{
                color: {{secondary_color}};
                font-weight: bold;
            }}}}
        </style>
        <center>
            <div id="{TABLE_ID}">
                <div class="{COL_ID}" style="{{total_style}}">
                    <div class="{LABEL_ID}">{{total_label}}</div>
                    <div class="{DATA_ID}">{{total_hrs}}</div>
                </div>
                <div class="{COL_ID}" style="{{range_style}}">
                    <div class="{LABEL_ID}">{{range_label}}</div>
                    <div class="{DATA_ID}">{{range_hrs}}</div>
                </div>
            </div>
        </center>
'''


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
    WEEK, TWO_WEEKS, MONTH, YEAR, CUSTOM = 0, 1, 2, 3, 4
    DAYS_IN = {WEEK: 7, TWO_WEEKS: 14, MONTH: 30, YEAR: 365, CUSTOM: 1}
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
    CUSTOM_TOTAL_HRS = 'Custom_Total_Hrs'
    CUSTOM_RANGE_HRS = 'Custom_Range_Hrs'
    CUSTOM_HRS_TEXT = 'Custom_Hrs_Text'
    CUSTOM_MIN_TEXT = 'Custom_Min_Text'
    SHOW_TOTAL = 'Hide_Total_Stat'
    SHOW_RANGED = 'Hide_Ranged_Stat'
    PRIMARY_COLOR = 'Primary_Color'
    SECONDARY_COLOR = 'Secondary_Color'
    BROWSER_ENABLED = 'Browser_Enabled'
    OVERVIEW_ENABLED = 'Overview_Enabled'
    CONGRATS_ENABLED = 'Congrats_Enabled'
    INCLUDE_DELETED = 'Include_Deleted_Reviews'
    USE_ROLLOVER = 'Use_Rollover_Hour'
    EXCLUDED_DIDS = "Excluded_Deck_IDs"
    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        WEEK_START: Weekday.SUNDAY,
        USE_CALENDAR_RANGE: True,
        RANGE_TYPE: Range.WEEK,
        CUSTOM_DAYS: 7,
        CUSTOM_TOTAL_TEXT: String.TOTAL,
        CUSTOM_RANGE_TEXT: String.PAST_RANGE,
        CUSTOM_TOTAL_HRS: String.TOTAL_HRS,
        CUSTOM_RANGE_HRS: String.PAST_HRS,
        CUSTOM_HRS_TEXT: String.HRS,
        CUSTOM_MIN_TEXT: String.MIN,
        SHOW_TOTAL: True,
        SHOW_RANGED: True,
        PRIMARY_COLOR: 'white',
        SECONDARY_COLOR: '#76bfb4',
        BROWSER_ENABLED: True,
        OVERVIEW_ENABLED: True,
        CONGRATS_ENABLED: True,
        INCLUDE_DELETED: True,
        USE_ROLLOVER: False,
        EXCLUDED_DIDS: [1]
    }
