# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.
import re
import traceback
from datetime import datetime, timedelta
from datetime import date as datetimedate
from typing import Match, Sequence

from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.overview import Overview, OverviewContent
from aqt.webview import AnkiWebView

from .config import ANKI_VERSION, TimeStatsConfigManager
from .consts import *


def _is_enabled_for_deck(conf_manager: TimeStatsConfigManager):
    return mw.col.decks.current().get('id') not in conf_manager.config[Config.EXCLUDED_DIDS]


def _args_from_ids(ids: list):
    """
    Does the same thing as Anki's implementation (ids2str) with less concern over versioning, but also less
    reliability.

    :param ids: ids to output
    :return: a string element converted from a square brackets to a parenthesis format
    """
    return '(' + (str(ids).replace('[', '').replace(']', '')) + ')'


def _unit_key_for_time(hours: float):
    """
    Returns the given unit key for the given amount of time.

    :param hours: referenced time
    :return: the hours unit if given a value larger than 1, otherwise the minutes unit
    """
    return Config.CUSTOM_HRS_TEXT if hours > 1 else Config.CUSTOM_MIN_TEXT


def _formatted_time(hours: float, precision=2):
    """
    Returns a locale-formatted length of time.

    :param hours: referenced time
    :param precision: total digits to show after a decimal
    :return: hours if given a value larger than 1, otherwise minutes
    """
    val = round(hours, precision) if hours > 1 else round(hours * 60, precision)
    return f'{val:n}'


def _offset_hour():
    offset_hour = 0

    if TimeStatsConfigManager(mw).config[Config.USE_ROLLOVER]:
        if ANKI_VERSION > ANKI_LEGACY_VER:
            offset_hour = mw.col.get_preferences().scheduling.rollover
        else:
            offset_hour = mw.col.conf.get('rollover', ANKI_DEFAULT_ROLLOVER)

    return offset_hour


def _total_hrs_in_revlog(revlog: [[int, int]]):
    """
    Returns the total review time within a sequence of reviews.

    :param revlog: referenced log sequence
    :return: total hours in the sequence
    """
    return sum([log[1] for log in revlog[0:]]) / 1000 / 60 / 60


def build_hooks():
    gui_hooks.deck_browser_will_render_content.append(append_to_browser)
    gui_hooks.overview_will_render_content.append(append_to_overview)
    if ANKI_VERSION > ANKI_LEGACY_VER:
        gui_hooks.webview_did_inject_style_into_page.append(append_to_congrats)


def append_to_browser(__browser: DeckBrowser, content: DeckBrowserContent):
    """
    Appends stats to the deck browser.
    :param __browser: unused browser object
    :param content: browser content to append stats to
    """
    if TimeStatsConfigManager(mw).config[Config.BROWSER_ENABLED]:
        content.stats += stats_html()


def append_to_overview(__overview: Overview, content: OverviewContent):
    """
    Appends stats to the overview.
    :param __overview: unused overview object
    :param content: overview content to append stats to
    """
    conf_manager = TimeStatsConfigManager(mw)

    if conf_manager.config[Config.OVERVIEW_ENABLED] and _is_enabled_for_deck(conf_manager):
        content.table += stats_html()


def append_to_congrats(web: AnkiWebView):
    """
    Extra handler used for the congrats page since it can't be as easily retrieved with the existing hooks.

    :param web: AnkiWebView to check against and format.
    """
    if mw.col:
        conf_manager = TimeStatsConfigManager(mw)

        if web.page().url().path().find('congrats.html') != -1:
            if conf_manager.config[Config.CONGRATS_ENABLED] and _is_enabled_for_deck(conf_manager):
                js = f'if (document.getElementById("{TABLE_ID}") == null) document.body.innerHTML += `{stats_html()}`'
                web.eval(js)


# use the same, gotten from append functions -> stats_html(), addon config in arg?
def cell_data_html():
    """
    :return: an html representation of a statistics-cell block
    """
    addon_config: dict = TimeStatsConfigManager(mw).config
    # revlog = full_revlog(addon_config)

    cells_html = ''
    for cell_data in addon_config[Config.CELLS_DATA]:
        cell_html: str = cell_data[Config.HTML].replace('{{', '{').replace('}}', '}')
        cell_html = f'<div class="{COL_CLASS}">\n{cell_html}\n</div>'

        cell_html = cell_html.format(
            CellClass=f'{HORIZ_CLASS}' if cell_data[Config.DIRECTION] == Direction.HORIZONTAL else '',
            TitleColor=cell_data[Config.TITLE_COLOR],
            Title=cell_data[Config.TITLE],
            OutputColor=cell_data[Config.OUTPUT_COLOR],
            Output=cell_data[Config.OUTPUT],
        )

        cells_html += filtered_html(cell_html, addon_config, cell_data)

    return cells_html


def stats_html():
    return HTML_SHELL.replace("{cell_data}", cell_data_html())


# def legacy_filtered_html(html: str, revlog: list, range_type, use_cal=False, week_start=0, custom_days=7):
#
#     pattern = r'(?<!%){}'
#
#     # print(f'pattern.format={pattern.format(CMD_RANGE_HRS)}')
#
#     # if re.search(fr'(?<!%){CMD_TOTAL_HRS}', html):
#     #     total_hrs = _total_hrs_in_revlog(revlog)
#     #     total_val = _formatted_time(total_hrs)
#     #     total_unit = addon_config[get_unit_type(total_hrs)]
#     #     html = re.sub(pattern.format(CMD_TOTAL_HRS), f'{total_val} {total_unit}', html)
#
#     if re.search(pattern.format(CMD_RANGE_HRS), html):
#         html = re.sub(pattern.format(CMD_RANGE_HRS), val_unit_range(revlog, days_ago), html)
#
#     if re.search(pattern.format(CMD_DAY_HRS), html):
#         html = re.sub(pattern.format(CMD_DAY_HRS), val_unit_range(revlog, days=0), html)
#
#     # html = re.sub(pattern.format(___), ___, html)
#
#     if re.search(pattern.format(CMD_WEEK_HRS), html):
#         html = re.sub(
#             pattern.format(CMD_WEEK_HRS), val_unit_range(revlog, get_days_ago(Range.WEEK)), html
#         )
#
#     if re.search(pattern.format(CMD_TWO_WEEKS_HRS), html):
#         html = re.sub(
#             pattern.format(CMD_TWO_WEEKS_HRS),
#             val_unit_range(revlog, get_days_ago(Range.TWO_WEEKS)),
#             html
#         )
#
#     if re.search(pattern.format(CMD_MONTH_HRS), html):
#         html = re.sub(
#             pattern.format(CMD_MONTH_HRS), val_unit_range(revlog, get_days_ago(Range.MONTH)), html
#         )
#
#     if re.search(pattern.format(CMD_YEAR_HRS), html):
#         html = re.sub(
#             pattern.format(CMD_YEAR_HRS), val_unit_range(revlog, get_days_ago(Range.YEAR)), html
#         )
#
#     if re.search(pattern.format(CMD_PREV_RANGE_HRS), html):
#         range_hrs = val_unit_range(revlog, range_type=range_type, start_at=1)
#         html = re.sub(pattern.format(CMD_PREV_RANGE_HRS), range_hrs, html)
#
#     if re.search(pattern.format(CMD_PREV_WEEK_HRS), html):
#         range_hrs = val_unit_range(revlog, range_type=Range.WEEK, start_at=1)
#         html = re.sub(pattern.format(CMD_PREV_WEEK_HRS), range_hrs, html)
#
#     if re.search(pattern.format(CMD_PREV_TWO_WEEKS_HRS), html):
#         range_hrs = val_unit_range(revlog, range_type=Range.TWO_WEEKS, start_at=1)
#         html = re.sub(pattern.format(CMD_PREV_TWO_WEEKS_HRS), range_hrs, html)
#
#     if re.search(pattern.format(CMD_PREV_MONTH_HRS), html):
#         range_hrs = val_unit_range(revlog, range_type=Range.MONTH, start_at=1)
#         html = re.sub(pattern.format(CMD_PREV_MONTH_HRS), range_hrs, html)
#
#     if re.search(pattern.format(CMD_PREV_YEAR_HRS), html):
#         range_hrs = val_unit_range(revlog, range_type=Range.YEAR, start_at=1)
#         html = re.sub(pattern.format(CMD_PREV_YEAR_HRS), range_hrs, html)
#
#     # Use for not returning duplicates in double-passed variables:
#     if re.search(pattern.format(CMD_PREV_DAY_HRS), html):
#         ref_date = (datetime.today() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
#         ranged_hrs = _total_hrs_in_revlog(get_logs_in_range(revlog, 0, ref_date))
#         range_val = _formatted_time(ranged_hrs)
#         range_unit = addon_config[get_unit_type(ranged_hrs)]
#         html = re.sub(pattern.format(CMD_PREV_DAY_HRS), f'{range_val} {range_unit}', html)
#
#     if re.search(pattern.format(CMD_RANGE), html):
#         if range_type != Range.CUSTOM:
#             range_text = Range.LABEL[range_type]
#         else:
#             range_text = f'{addon_config[Config.CUSTOM_DAYS]} {String.DAYS}'
#         html = re.sub(pattern.format(CMD_RANGE), range_text, html)
#
#     if re.search(pattern.format(CMD_DATE), html):
#         html = re.sub(
#             pattern.format(CMD_DATE), (datetimedate.today() - timedelta(days=days_ago)).strftime('%x'), html
#         )
#
#     if re.search(pattern.format(CMD_YEAR), html):
#         html = re.sub(
#             pattern.format(CMD_YEAR), (datetimedate.today() - timedelta(days=days_ago)).strftime('%Y'), html
#         )
#
#     if re.search(pattern.format(CMD_FULL_DAY), html):
#         html = re.sub(
#             pattern.format(CMD_FULL_DAY), (datetimedate.today() - timedelta(days=days_ago)).strftime('%A'), html
#         )
#
#     if re.search(pattern.format(CMD_DAY), html):
#         html = re.sub(
#             pattern.format(CMD_DAY), (datetimedate.today() - timedelta(days=days_ago)).strftime('%a'), html
#         )
#
#     if re.search(pattern.format(CMD_MONTH), html):
#         html = re.sub(
#             pattern.format(CMD_MONTH), (datetimedate.today() - timedelta(days=days_ago)).strftime('%b'), html
#         )
#
#     if re.search(pattern.format(CMD_FULL_MONTH), html):
#         html = re.sub(
#             pattern.format(CMD_FULL_MONTH), (datetimedate.today() - timedelta(days=days_ago)).strftime('%B'), html
#         )
#
#     if re.search(pattern.format(CMD_DAYS), html):
#         html = re.sub(pattern.format(CMD_DAYS), f'{days_ago}', html)
#         # if re.search(r'(?<!%)%date\(.*,+.*\)', html):  # future filter?
#
#     # Removed assignment expression (:=) for Python 3.7 builds
#     matches = re.search(pattern.format(fr'{CMD_FROM_DATE_HRS}\d\d\d\d-\d\d-\d\d'), html)
#     if matches:
#         try:
#             day_range = (datetime.today() - datetime.fromisoformat(matches.group(2))).days
#             ranged_hrs = _total_hrs_in_revlog(get_logs_in_range(revlog, day_range))
#             range_val = _formatted_time(ranged_hrs)
#             range_unit = addon_config[get_unit_type(ranged_hrs)]
#             html = re.sub(pattern.format("".join(matches.groups())), f'{range_val} {range_unit}', html)
#         except ValueError:
#             aqt.utils.showWarning(f'{traceback.format_exc()}')
#
#     if re.search(r'%%', html):
#         html = html.replace('%%', '%')
#
#     return html


def filtered_html(html: str, addon_config: dict, cell_data: dict):
    cids = filtered_cids(addon_config[Config.EXCLUDED_DIDS], addon_config[Config.INCLUDE_DELETED])
    # pattern = r'(?<!%){}'

    print(f'filtered_html() < {html}')

    def sub_html(macro: str, revlog: list):
        nonlocal html
        print(f'sub_html()')
        total_hrs = _total_hrs_in_revlog(revlog)
        unit_key = _unit_key_for_time(total_hrs)
        html = re.sub(
            fr'(?<!%){macro}',
            f'{_formatted_time(total_hrs)} {addon_config[unit_key]}',
            html,
        )

    if re.search(fr'(?<!%){CMD_TOTAL_HRS}', html):
        # revlog = filtered_revlog(cids)
        # total_hrs = _total_hrs_in_revlog(revlog)
        # unit_key = _unit_key_for_time(total_hrs)
        # sub_html(filtered_revlog(cids), CMD_TOTAL_HRS, f'{_formatted_time(total_hrs)} {addon_config[unit_key]}')
        print(f're.search(CMD_TOTAL_HRS)')
        sub_html(CMD_TOTAL_HRS, filtered_revlog(cids))

    # if re.search(fr'(?<!%){CMD_RANGE_HRS}', html):
    #     cell_data[Config]
    #     sub_html(CMD_TOTAL_HRS, filtered_revlog(cids))

    # for repl in replacements:
    #     repl: [str, str]
    #     html = re.sub(r'(?<!%){}'.format(repl[0]), repl[1], html)

    # Get command type -> get logs -> replace

    return html


def filtered_cids(excluded_dids: list = None, include_deleted: bool = False) -> list[Sequence]:
    excluded_dids = _args_from_ids(excluded_dids)

    if include_deleted and mw.state != 'overview':
        # Including deleted and viewing a specific deck: grab all dids that aren't excluded
        excluded_cids_cmd = f'SELECT id FROM cards WHERE did in {excluded_dids}'
        excluded_cids = mw.col.db.all(excluded_cids_cmd)
        filter_cmd = f'WHERE cid not in {_args_from_ids(excluded_cids)}'
    else:
        # Grab all parent and child dids for the current deck, or all dids if viewing all decks, currently
        dids = [
            str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))
            if str(i) not in excluded_dids
        ] if mw.state == 'overview' else [
            str(name_id.id) for name_id in mw.col.decks.all_names_and_ids()
            if str(name_id) not in excluded_dids
        ]
        filter_cmd = f'WHERE did in {_args_from_ids(dids)}'

    return mw.col.db.all(f'SELECT DISTINCT cid FROM revlog {filter_cmd}')


def filtered_revlog(cids: list, time_range_ms: tuple[int, int] = None) \
        -> list[Sequence]:
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {_args_from_ids(cids)}'
    revlog_cmd += f' AND id BETWEEN {time_range_ms[0]} AND {time_range_ms[1]}' if time_range_ms else ''
    return mw.col.db.all(revlog_cmd)


def full_revlog(addon_config) -> list:
    """
    Retrieves Anki review data using the currently displayed decks and excluded decks filters.

    :param addon_config: config to use as a reference for excluded deck ids
    :return: a sequence with the format: [[log_id, review_time], ...]
    """
    excluded_dids = _args_from_ids(addon_config[Config.EXCLUDED_DIDS])

    # Get deleted cards on overview, otherwise use standard known-cards per-deck
    if addon_config[Config.INCLUDE_DELETED] and mw.state != 'overview':
        excluded_cids_cmd = f'SELECT id FROM cards WHERE did in {excluded_dids}'
        excluded_cids = mw.col.db.all(excluded_cids_cmd)
        cids_cmd = f'SELECT cid FROM revlog WHERE cid not in {_args_from_ids(excluded_cids)}'
    else:
        if mw.state == 'overview':
            # grab all parent and child dids for the current deck
            dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
        else:
            # grab all dids
            dids = [str(name_id.id) for name_id in mw.col.decks.all_names_and_ids()]

        for excluded_did in excluded_dids:
            if excluded_did in dids:
                dids.remove(excluded_did)

        cids_cmd = f'SELECT id FROM cards WHERE did in {_args_from_ids(dids)}'

    all_cids = mw.col.db.all(cids_cmd)
    # Remove duplicates via set-builder syntax
    unique_cids = {cid[0] for cid in all_cids}

    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {_args_from_ids(list(unique_cids))}'

    return mw.col.db.all(revlog_cmd)


def logs_in_range(
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

    from_adjusted_date = date_with_rollover(from_date)

    filtered_logs = []
    for log in revlog[0:]:
        log_epoch_seconds = log[0] / 1000
        log_date = datetime.fromtimestamp(log_epoch_seconds)

        log_delta = from_adjusted_date - log_date
        if 0 <= log_delta.days <= days_ago:
            filtered_logs.append(log)
    return filtered_logs


def days_ago(range_type: int, use_cal=False, week_start=0, from_date=datetime.today()) -> int:
    # Calendar Range Math!
    total_days = Range.DAYS_IN[range_type]

    if use_cal:
        from_adjusted_date = date_with_rollover(from_date)

        if range_type == Range.WEEK or range_type == Range.TWO_WEEKS:
            total_weeks = Range.DAYS_IN[range_type] / 7
            total_days = days_since_week_start(total_weeks, week_start, from_adjusted_date)
        else:
            if range_type == Range.MONTH:
                total_days = (from_adjusted_date - from_adjusted_date.replace(day=1)).days
            elif range_type == Range.YEAR:
                total_days = (from_adjusted_date - from_adjusted_date.replace(month=1, day=1)).days

    return total_days


def days_since_week_start(
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
    from_adjusted_date = date_with_rollover(from_date)
    ref_day = from_adjusted_date.weekday()
    # Adds an extra week if the current day is already past the week start
    return (total_weeks * 7) + ((ref_day - week_start_day) - (7 * (ref_day >= week_start_day)))


def val_unit_range(revlog: [[int, int]], unit: str, days: int = 0, range_type: int = None, start_at=0):
    """
    Retrieves the given range's hours in reviews.

    :param revlog: referenced log sequence
    :param unit: unit to append to output text
    :param days: (optional) days to go back from, overridden by range_type inputs
    :param range_type: (optional) range_type to use for hour calculations
    :param start_at: iteration to start the range_type gathering from, goes back n previous iterations, else starts
    from current
    :return: a formatted string with the range in hours/minutes with its associated unit pair (e.g. '2 hrs'/'3.1 min')
    """
    from_date = datetime.today()

    if range_type is not None:
        days = days_ago(range_type)
        if start_at > 0:
            # extra day added to not include the current/later range for outputs
            from_date -= timedelta(days=(days_ago(range_type) * start_at) + 1)
            days -= 1

    ranged_hrs = _total_hrs_in_revlog(logs_in_range(revlog, days, from_date))
    range_val = _formatted_time(ranged_hrs)

    return f'{range_val} {unit}'


def date_with_rollover(date: datetime = datetime.today()):
    """
    Retrieves a date-time adjusted to its day-end hour and Anki/add-on preferences for end of day.

    :param date: date to adjust
    :return: an adjusted datetime object
    """

    return date.replace(hour=23, minute=59, second=59) - timedelta(hours=_offset_hour())
