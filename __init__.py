"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file, located in the add-on's root directory.

Shows total study time and a ranged amount of study time in Anki's main window.
"""
import re
from datetime import timedelta, datetime, date

from aqt import mw, gui_hooks, webview
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from aqt.qt import QAction

from .config import TimeStatsConfigManager
from .consts import String, Range, UNIQUE_DATE, Config, CMD_RANGE, CMD_DATE, CMD_YEAR, CMD_FULL_DAY, CMD_DAY, CMD_DAYS
from .options import TimeStatsOptionsDialog

table_id, col_id, label_id, data_id = 'sts-table', 'sts-col', 'sts-label', 'sts-data'
html_shell = '''
        <style>
            #{table_id} {{
                display: table;
                margin-top: .5em;
                max-width: fit-content;
                font-weight: normal;
            }}
            .{col_id} {{
                display: table-cell;
                word-break: break-all;
                width: 30vh;
            }}
            .{col_id} > * {{
                display: table-row;
            }}
            .{label_id} {{
                color: {primary_color};
            }}
            .{data_id} {{
                color: {secondary_color};
                font-weight: bold;
            }}
        </style>
        <center>
            <div id=sts-table>
                <div class="sts-col">
                    <div class="sts-label">{total_label}</div>
                    <div class="sts-data">{total_value} {total_unit}</div>
                </div>
                <div class="sts-col">
                    <div class="sts-label">{range_label}</div>
                    <div class="sts-data">{range_value} {range_unit}</div>
                </div>
            </div>
        </center>
'''


def initialize():
    """
Initializer for add-on. Called at start for finer execution order and a bit of readability.
    """
    build_hooks()
    build_actions()


def build_hooks():
    """
Append addon hooks to Anki.
    """
    gui_hooks.webview_will_set_content.append(format_webview)
    gui_hooks.webview_did_inject_style_into_page.append(format_congrats)


def build_actions():
    """
Add and connect addon actions. Currently, adds an options menu action and sets the addon configuration action,
found in Anki's addon window, to also open the options menu.
    """
    options_action = QAction(String.OPTIONS_ACTION, mw)
    options_action.triggered.connect(on_options_called)
    # Handle edge case where toolbar action already exists
    if options_action in mw.form.menuTools.actions():
        mw.form.menuTools.removeAction(options_action)

    mw.form.menuTools.addAction(options_action)
    mw.addonManager.setConfigAction(__name__, on_options_called)


def get_config_manager() -> TimeStatsConfigManager:
    """
Retrieves the addon's config manager.
    :return: a deep-copy of the TimeStatsConfigManager Class
    """
    # this is neat, but also maybe a date option for the custom filter might be nice...
    return TimeStatsConfigManager(mw, (date.today() - date.fromisoformat(UNIQUE_DATE)).days)


def format_webview(content: webview.WebContent, context: object or None):
    """
If the current deck screen isn't excluded, formats the Anki webview to include html with study time data,
else does nothing.
    :param content: WebContent to be formatted
    :param context: object used to check if the current view can/should be formatted
    """
    if mw.col is None:
        # print(f'--Anki Window was NoneType')
        return

    config_manager = get_config_manager()

    if (isinstance(context, DeckBrowser) and config_manager.config[Config.BROWSER_ENABLED]) or \
            (isinstance(context, Overview) and config_manager.config[Config.OVERVIEW_ENABLED] and
             should_display_on_current_screen()):
        content.body += formatted_html()


def format_congrats(web: webview.AnkiWebView):
    """
Extra handler used for the congrats page since it can't be as easily retrieved with the existing hooks.
    :param web: AnkiWebView to check against and format.
    """
    if mw.col is None:
        # print(f'--Anki Window was NoneType')
        return

    config_manager = get_config_manager()

    if web.page().url().path().find('congrats.html') != -1 and config_manager.config[Config.CONGRATS_ENABLED]:
        if should_display_on_current_screen():
            web.eval(
                f'if (document.getElementById("{table_id}") == null) document.body.innerHTML += `{formatted_html()}`'
            )


def on_options_called():
    """
Initializes and opens the options dialog.
    """
    dialog = TimeStatsOptionsDialog(get_config_manager())
    dialog.show()


def should_display_on_current_screen():
    """
Determines whether the current screen's selection should display stats based on user's excluded deck ID's.
    :return: True if current selection isn't excluded, otherwise false.
    """
    return mw.col.decks.current().get('id') not in get_config_manager().config[Config.EXCLUDED_DIDS]


def get_review_stats() -> (float, float, int):
    """
Retrieves Anki review data needed for formatting using the currently visible decks and SQL commands filtering through
the Anki database files.
    :return: Tuple: (total review time, filtered review time, total days filtered)
    """
    addon_config = get_config_manager().config

    # print(f'mw state: {mw.state}')
    if mw.state == 'overview':
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
    else:
        dids = mw.col.decks.all_ids()

    for excluded_did in addon_config[Config.EXCLUDED_DIDS]:
        if str(excluded_did) in dids:
            dids.remove(str(excluded_did))

    # print(f'checking dids: {[mw.col.decks.name(i) for i in dids]}')

    dids_as_args = '(' + ', '.join(dids) + ')'
    cids_cmd = f'SELECT id FROM cards WHERE did in {dids_as_args}\n'
    cids = mw.col.db.all(cids_cmd)
    formatted_cids = '(' + (str(cids).replace('[', '').replace(']', '')) + ')'
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}'

    rev_log = mw.col.db.all(revlog_cmd)

    # Calendar Range Math!
    range_type = addon_config[Config.RANGE_TYPE]
    if range_type != Range.CUSTOM:
        days_ago = Range.DAYS_IN[range_type]
        if addon_config[Config.USE_CALENDAR_RANGE]:
            if range_type == Range.WEEK or range_type == Range.TWO_WEEKS:
                week_date = date.today() - timedelta(days=(Range.DAYS_IN[range_type] - 7))
                week_start_day = addon_config[Config.WEEK_START]
                if week_date.weekday() >= week_start_day:
                    days_ago = (week_date.weekday() - week_start_day) + (Range.DAYS_IN[range_type] - 7)
                else:
                    days_ago = (week_date.weekday() - week_start_day) + (Range.DAYS_IN[range_type])
            elif range_type == Range.MONTH:
                days_ago = (date.today() - date.today().replace(day=1)).days
            elif range_type == Range.YEAR:
                days_ago = (date.today() - date.today().replace(month=1, day=1)).days
    else:
        days_ago = addon_config[Config.CUSTOM_DAYS]
    filtered_revlog = filter_revlog(rev_log, days_ago=days_ago)

    all_rev_times_ms = [log[1] for log in rev_log[0:]]
    filtered_rev_times_ms = [log[1] for log in filtered_revlog[0:]]

    return sum(all_rev_times_ms) / 1000 / 60 / 60, sum(filtered_rev_times_ms) / 1000 / 60 / 60, int(days_ago)


def formatted_html():
    """
Uses the addon config and current stats to retrieve the html to display on Anki's main window.
    :return: html string containing review configured review information
    """
    addon_config = get_config_manager().config
    total_hrs, ranged_hrs, days_ago = get_review_stats()

    total_val = round(total_hrs, 2) if total_hrs > 1 else round(total_hrs * 60, 2)
    range_val = round(ranged_hrs, 2) if ranged_hrs > 1 else round(ranged_hrs * 60, 2)
    total_unit = addon_config[Config.CUSTOM_HRS_TEXT] if total_hrs > 1 else addon_config[Config.CUSTOM_MIN_TEXT]
    range_unit = addon_config[Config.CUSTOM_HRS_TEXT] if ranged_hrs > 1 else addon_config[Config.CUSTOM_MIN_TEXT]

    html_string = html_shell.format(total_label=addon_config[Config.CUSTOM_TOTAL_TEXT],
                                    range_label=addon_config[Config.CUSTOM_RANGE_TEXT],
                                    total_value=total_val, range_value=range_val,
                                    total_unit=total_unit, range_unit=range_unit,
                                    primary_color=addon_config[Config.PRIMARY_COLOR],
                                    secondary_color=addon_config[Config.SECONDARY_COLOR],
                                    table_id=table_id, col_id=col_id, label_id=label_id, data_id=data_id)

    return filter_html_ids(html_string, days_ago)


def filter_html_ids(html_string: str, days_ago: int):
    """
Replaces the input html string with some basic formatted text based on identifier codes.
Currently uses the string identifiers: %range, %from_date, %from_year, %from_full_weekday, %from_weekday, and %days.
    :param html_string: html string to be formatted
    :param days_ago: days to use when replacing date-type identifiers
    :return: the formatted html string object
    """
    addon_config = get_config_manager().config
    if re.search(fr'(?<!%){CMD_RANGE}', html_string):
        start = addon_config[Config.RANGE_TYPE]
        range_text = Range.LABEL[start] if start != Range.CUSTOM \
            else f'{addon_config[Config.CUSTOM_DAYS]} {String.DAYS}'
        html_string = html_string.replace(CMD_RANGE, range_text)

    if re.search(fr'(?<!%){CMD_DATE}', html_string):
        html_string = html_string.replace(CMD_DATE, (date.today() - timedelta(days=days_ago)).strftime('%x'))

    if re.search(fr'(?<!%){CMD_YEAR}', html_string):
        html_string = html_string.replace(CMD_YEAR, (date.today() - timedelta(days=days_ago)).strftime('%Y'))

    if re.search(fr'(?<!%){CMD_FULL_DAY}', html_string):
        html_string = html_string.replace(CMD_FULL_DAY, (date.today() - timedelta(days=days_ago)).strftime(
            '%A'))

    if re.search(fr'(?<!%){CMD_DAY}', html_string):
        html_string = html_string.replace(CMD_DAY, (date.today() - timedelta(days=days_ago)).strftime('%a'))

    if re.search(fr'(?<!%){CMD_DAYS}', html_string):
        html_string = html_string.replace(CMD_DAYS, f'{days_ago}')
        # if re.search(r'(?<!%)%date\(.*,+.*\)', html_string):  # future filter?

    if re.search(r'%%', html_string):
        html_string = html_string.replace('%%', '%')

    return html_string


# def offset_date(dt: datetime, hours: int = 0):
#     """
# Offsets a datetime object using a set amount of hours. Mainly for adjusting times based on the rollover/day-end hour
# in Anki.
#     :param dt: datetime object to offset
#     :param hours: number of hours to offset the date
#     :return: an offset datetime object
#     """
#     return dt + timedelta(hours=hours)


def filter_revlog(rev_logs: [[int, int]], days_ago: int = None) -> [[int, int]]:
    """
Retrieves a collection of review logs based on the input number of days to retrieve from today.
    :param rev_logs: list of review logs containing an array with [log time-identifier, log time spent]
    :param days_ago: number of days to filter through
    :return: a new list of review logs based on the input days to filter
    """
    offset_hour = mw.col.get_preferences().scheduling.rollover
    filtered_logs = []
    for log in rev_logs[0:]:
        log_epoch_seconds = log[0] / 1000
        log_date = datetime.fromtimestamp(log_epoch_seconds)

        # log_delta = offset_date(datetime.now(), offset_hour) - log_date
        log_delta = (datetime.now() + timedelta(hours=offset_hour)) - log_date
        if log_delta.days <= days_ago:
            filtered_logs.append(log)

    return filtered_logs


initialize()
