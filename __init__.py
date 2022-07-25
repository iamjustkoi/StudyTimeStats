"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in the "LICENSE" file, packaged with the add-on.

Shows total study time and a ranged amount of study time in Anki's main window.
"""
import re
from datetime import timedelta, datetime, date

from aqt import mw, gui_hooks, webview
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from aqt.qt import QAction

from src.config import TimeStatsConfigManager, ANKI_VERSION
from src.consts import *
from src.options import TimeStatsOptionsDialog

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
                width: 30vw;
                max-width: 200px;
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
            <div id="{table_id}">
                <div class="{col_id}" style="{total_style}">
                    <div class="{label_id}">{total_label}</div>
                    <div class="{data_id}">{total_hrs}</div>
                </div>
                <div class="{col_id}" style="{range_style}">
                    <div class="{label_id}">{range_label}</div>
                    <div class="{data_id}">{range_hrs}</div>
                </div>
            </div>
        </center>
'''


def initialize():
    """
Initializer for the add-on. Called at the start for finer execution order and a bit of readability.
    """
    build_hooks()
    build_actions()


def build_hooks():
    """
Append addon hooks to Anki.
    """
    gui_hooks.webview_will_set_content.append(append_to_webview)
    if ANKI_VERSION > ANKI_LEGACY_VER:
        gui_hooks.webview_did_inject_style_into_page.append(append_to_congrats)
        gui_hooks.operation_did_execute.append(refresh_tools_menu_action)
    else:
        gui_hooks.state_did_reset.append(refresh_tools_menu_action)


def build_actions():
    """
Add and connect addon actions. Currently, adds an options menu action and sets the addon configuration action,
found in Anki's addon window, to also open the options menu.
    """
    refresh_tools_menu_action()
    mw.addonManager.setConfigAction(__name__, on_options_called)


def refresh_tools_menu_action(changes=None, obj=None):
    """
Updates the toolbar actions menu with the options shortcut. Expects an Operation Change hook call,
but can also be used as a general update push, too.
    :param changes: unused OpChanges object
    :param obj: unused options object
    """
    if get_config_manager().config[Config.TOOLBAR_ENABLED]:
        options_action = QAction(String.OPTIONS_ACTION, mw)
        options_action.triggered.connect(on_options_called)
        # Handles edge cases where toolbar action already exists in the tools menu
        if options_action.text() not in [action.text() for action in mw.form.menuTools.actions()]:
            mw.form.menuTools.addAction(options_action)
    else:
        for action in mw.form.menuTools.actions():
            if action.text() == String.OPTIONS_ACTION:
                mw.form.menuTools.removeAction(action)


def on_options_called():
    """
Initializes and opens the options dialog.
    """
    dialog = TimeStatsOptionsDialog(get_config_manager())
    dialog.exec()


def get_config_manager() -> TimeStatsConfigManager:
    """
Retrieves the addon's config manager.
    :return: a deep-copy of the TimeStatsConfigManager Class
    """
    # this is neat, but also maybe a date option for the custom filter might be nice...
    return TimeStatsConfigManager(mw, (date.today() - date.fromisoformat(UNIQUE_DATE)).days)


def append_to_webview(content: webview.WebContent, context: object or None):
    """
If the current deck screen isn't excluded, formats the Anki webview to include html with study time data,
else does nothing.
    :param content: WebContent to be formatted
    :param context: object used to check if the current view can/should be formatted
    """
    if mw.col is None:
        # print(f'--Anki Window was NoneType')
        return

    addon_config = get_config_manager().config

    show_on_deck_browser = isinstance(context, DeckBrowser) and addon_config[Config.BROWSER_ENABLED]
    #  handles legacy congrats
    on_congrats = False if ANKI_VERSION > ANKI_LEGACY_VER else content.body.find("Congratulations!") >= 0
    show_on_congrats = on_congrats and addon_config[Config.CONGRATS_ENABLED]

    show_on_overview = isinstance(context, Overview) and addon_config[Config.OVERVIEW_ENABLED] and not on_congrats

    if show_on_deck_browser or ((show_on_overview or show_on_congrats) and is_enabled_for_current_deck()):
        content.body += get_stats_html()


def append_to_congrats(web: webview.AnkiWebView):
    """
Extra handler used for the congrats page since it can't be as easily retrieved with the existing hooks.
    :param web: AnkiWebView to check against and format.
    """
    if mw.col is None:
        # print(f'--Anki Window was NoneType')
        return

    addon_config = get_config_manager().config

    if web.page().url().path().find('congrats.html') != -1 and addon_config[Config.CONGRATS_ENABLED]:
        if is_enabled_for_current_deck():
            web.eval(
                f'if (document.getElementById("{table_id}") == null) document.body.innerHTML += `{get_stats_html()}`'
            )


def is_enabled_for_current_deck() -> bool:
    """
Determines whether the current screen's selection should display get_time_stats based on user's excluded deck ID's.
    :return: true if current selection isn't excluded, otherwise false.
    """
    return mw.col.decks.current().get('id') not in get_config_manager().config[Config.EXCLUDED_DIDS]


def get_unit_type(hours: float):
    """
Returns the given unit type for the given amount of time.
    :param hours: referenced time
    :return: the hours unit if given a value larger than 1, otherwise the minutes unit
    """
    return Config.CUSTOM_HRS_TEXT if hours > 1 else Config.CUSTOM_MIN_TEXT


def get_formatted_hrs_or_min(hours: float, precision=2):
    """
Returns a locale-formatted length of time.
    :param hours: referenced time
    :param precision: total digits to show after a decimal
    :return: hours if given a value larger than 1, otherwise minutes
    """
    val = round(hours, precision) if hours > 1 else round(hours * 60, precision)
    return f'{val:n}'


def get_stats_html():
    """
Uses the addon config and current get_time_stats to retrieve the html to display on Anki's main window.
    :return: html string containing review configured review information
    """
    addon_config = get_config_manager().config

    html_string = html_shell.format(
        total_label=addon_config[Config.CUSTOM_TOTAL_TEXT],
        range_label=addon_config[Config.CUSTOM_RANGE_TEXT],
        total_hrs=addon_config[Config.CUSTOM_TOTAL_HRS],
        range_hrs=addon_config[Config.CUSTOM_RANGE_HRS],
        primary_color=addon_config[Config.PRIMARY_COLOR],
        secondary_color=addon_config[Config.SECONDARY_COLOR],
        total_style='' if addon_config[Config.SHOW_TOTAL] else 'display: none;',
        range_style='' if addon_config[Config.SHOW_RANGED] else 'display: none;',
        table_id=table_id,
        col_id=col_id,
        label_id=label_id,
        data_id=data_id
    )

    return get_formatted_html_macros(html_string)


def get_formatted_html_macros(html_string: str):
    """
Replaces the input html string with formatted text based on input codes.
Currently, uses the string identifiers: %range, %from_date, %from_year, %from_full_weekday, %from_weekday, and %days.
    :param html_string: html string to be formatted
    :return: the formatted html string object
    """
    addon_config = get_config_manager().config
    range_type = addon_config[Config.RANGE_TYPE]

    revlog = get_revlog(addon_config)
    days_ago = get_days_ago(addon_config[Config.RANGE_TYPE], addon_config)

    if re.search(fr'(?<!%){CMD_TOTAL_HRS}', html_string):
        total_hrs = get_hrs_in_revlog(revlog)
        total_val = get_formatted_hrs_or_min(total_hrs)
        total_unit = addon_config[get_unit_type(total_hrs)]
        html_string = html_string.replace(CMD_TOTAL_HRS, f'{total_val} {total_unit}')

    if re.search(fr'(?<!%){CMD_RANGE_HRS}', html_string):
        ranged_hrs = get_hrs_in_revlog(get_logs_in_range(revlog, days_ago))
        range_val = get_formatted_hrs_or_min(ranged_hrs)
        range_unit = addon_config[get_unit_type(ranged_hrs)]
        html_string = html_string.replace(CMD_RANGE_HRS, f'{range_val} {range_unit}')

    if re.search(fr'(?<!%){CMD_LAST_CAL_HRS}', html_string):
        # extra day added to not include the received week-start day
        from_date = datetime.today() - timedelta(days=get_days_ago(range_type, addon_config) + 1)
        # = 1 accounts for extra day
        ranged_hrs = get_hrs_in_revlog(get_logs_in_range(revlog, Range.DAYS_IN[range_type] - 1, from_date=from_date))
        cal_val = get_formatted_hrs_or_min(ranged_hrs)
        cal_unit = addon_config[get_unit_type(ranged_hrs)]
        html_string = html_string.replace(CMD_LAST_CAL_HRS, f'{cal_val} {cal_unit}')

    # Use for not returning duplicates in double-passed variables:
    # match = re.search(fr'(?<!%){CMD_LAST_DAY}', html_string)
    # len(match.regs)r
    if re.search(fr'(?<!%){CMD_LAST_DAY_HRS}', html_string):
        ref_date = (datetime.today() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        # ranged_hrs = get_hrs_in_revlog(get_logs_in_range(revlog, days_ago=0, from_date=ref_date))
        ranged_hrs = get_hrs_in_revlog(get_logs_in_range(revlog, 0, ref_date))
        day_val = get_formatted_hrs_or_min(ranged_hrs)
        day_unit = addon_config[get_unit_type(ranged_hrs)]
        html_string = html_string.replace(CMD_LAST_DAY_HRS, f'{day_val} {day_unit}')

    if re.search(fr'(?<!%){CMD_RANGE}', html_string):
        if range_type != Range.CUSTOM:
            range_text = Range.LABEL[range_type]
        else:
            range_text = f'{addon_config[Config.CUSTOM_DAYS]} {String.DAYS}'
        html_string = html_string.replace(CMD_RANGE, range_text)

    if re.search(fr'(?<!%){CMD_DATE}', html_string):
        html_string = html_string.replace(
            CMD_DATE, (date.today() - timedelta(days=days_ago)).strftime('%x')
        )

    if re.search(fr'(?<!%){CMD_YEAR}', html_string):
        html_string = html_string.replace(
            CMD_YEAR, (date.today() - timedelta(days=days_ago)).strftime('%Y')
        )

    if re.search(fr'(?<!%){CMD_FULL_DAY}', html_string):
        html_string = html_string.replace(
            CMD_FULL_DAY, (date.today() - timedelta(days=days_ago)).strftime('%A')
        )

    if re.search(fr'(?<!%){CMD_DAY}', html_string):
        html_string = html_string.replace(
            CMD_DAY, (date.today() - timedelta(days=days_ago)).strftime('%a')
        )

    if re.search(fr'(?<!%){CMD_MONTH}', html_string):
        html_string = html_string.replace(
            CMD_MONTH, (date.today() - timedelta(days=days_ago)).strftime('%b')
        )

    if re.search(fr'(?<!%){CMD_FULL_MONTH}', html_string):
        html_string = html_string.replace(
            CMD_FULL_MONTH, (date.today() - timedelta(days=days_ago)).strftime('%B')
        )

    if re.search(fr'(?<!%){CMD_DAYS}', html_string):
        html_string = html_string.replace(
            CMD_DAYS, f'{days_ago}'
        )
        # if re.search(r'(?<!%)%date\(.*,+.*\)', html_string):  # future filter?

    if re.search(r'%%', html_string):
        html_string = html_string.replace('%%', '%')

    return html_string


def get_args_from_ids(cids: list):
    return '(' + (str(cids).replace('[', '').replace(']', '')) + ')'


def get_revlog(addon_config):
    """
Retrieves Anki review data using the currently displayed decks and excluded decks filters.
    :param addon_config: config to use as a reference for excluded deck ids
    :return: a sequence with the format: [[log_id, review_time], ...]
    """
    excluded_dids = get_args_from_ids(addon_config[Config.EXCLUDED_DIDS])

    # Get deleted cards on overview, otherwise use standard known-cards per-deck
    if addon_config[Config.INCLUDE_DELETED] and mw.state != 'overview':
        excluded_cids_cmd = f'SELECT id FROM cards WHERE did in {excluded_dids}'
        excluded_cids = mw.col.db.all(excluded_cids_cmd)
        cids_cmd = f'SELECT cid FROM revlog WHERE cid not in {get_args_from_ids(excluded_cids)}'
    else:
        if mw.state == 'overview':
            dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
        else:
            dids = [str(name_id.id) for name_id in mw.col.decks.all_names_and_ids()]

        for excluded_did in excluded_dids:
            if excluded_did in dids:
                dids.remove(excluded_did)
        cids_cmd = f'SELECT id FROM cards WHERE did in {get_args_from_ids(dids)}'

        # print(f'checking decks: {[mw.col.decks.name(i) for i in dids]}')

    all_cids = mw.col.db.all(cids_cmd)
    # Remove duplicates via set-builder syntax
    unique_cids = {cid[0] for cid in all_cids}

    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {get_args_from_ids(list(unique_cids))}'
    return mw.col.db.all(revlog_cmd)


def get_days_ago(range_type: int, addon_config, from_date=datetime.today()):
    """
Returns the total number of days since the start of a ranged time length.
    :param range_type: range to use as a reference
    :param addon_config: add-on config for retrieving user values
    :param from_date: input date to check distance of start from
    :return: total days away the range is from the referenced date-time
    """
    # Calendar Range Math!
    if range_type == Range.CUSTOM:
        return addon_config[Config.CUSTOM_DAYS]

    from_base_date = from_date.replace(hour=23, minute=59, second=59)

    days_ago = Range.DAYS_IN[range_type]
    if addon_config[Config.USE_CALENDAR_RANGE]:
        if range_type == Range.WEEK or range_type == Range.TWO_WEEKS:
            total_weeks = Range.DAYS_IN[range_type] / 7
            days_ago = get_days_since_week_start(total_weeks, addon_config[Config.WEEK_START], from_base_date)
        else:
            if range_type == Range.MONTH:
                days_ago = (from_base_date - from_base_date.replace(day=1)).days
            elif range_type == Range.YEAR:
                days_ago = (from_base_date - from_base_date.replace(month=1, day=1)).days
    return days_ago


def get_hrs_in_revlog(revlog: [[int, int]]):
    """
Returns the total review time within a sequence of reviews.
    :param revlog: referenced log sequence
    :return: total hours in the sequence
    """
    return sum([log[1] for log in revlog[0:]]) / 1000 / 60 / 60


def get_days_since_week_start(
        total_weeks: int,
        week_start_day: int,
        from_date: datetime
):
    """
Gets days since the last week-start date based on a set number of weeks.
    :param total_weeks: range of weeks to use as a reference point
    :param week_start_day: start of the week to count total days from
    :param from_date: changes the reference date to this datetime
    :return: days since week start
    """
    ref_day = from_date.weekday()
    # Adds an extra week if the current day is already past the week start
    return (total_weeks * 7) + ((ref_day - week_start_day) - (7 * (ref_day >= week_start_day)))


def get_logs_in_range(
        revlog: [[int, int]],
        days_ago: int = 0,
        from_date: datetime = datetime.today()
) -> [[int, int]]:
    """
Retrieves a collection of review logs based on the input number of days to retrieve from today.
    :param revlog: list of review logs containing an array with [log time-identifier, log time spent]
    :param days_ago: number of days to filter back through
    :param from_date: changes the reference date to this datetime
    :return: a new list of review logs based on the input days to filter
    """
    if ANKI_VERSION > ANKI_LEGACY_VER:
        offset_hour = mw.col.get_preferences().scheduling.rollover
    else:
        offset_hour = mw.col.conf.get('rollover', ANKI_DEFAULT_ROLLOVER)

    from_adjusted_date = from_date.replace(hour=23, minute=59, second=59) - timedelta(hours=offset_hour)

    filtered_logs = []
    for log in revlog[0:]:
        log_epoch_seconds = log[0] / 1000
        log_date = datetime.fromtimestamp(log_epoch_seconds)

        log_delta = from_adjusted_date - log_date
        if 0 <= log_delta.days <= days_ago:
            filtered_logs.append(log)
    return filtered_logs


initialize()
