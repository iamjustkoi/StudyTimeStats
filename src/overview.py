# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.
from datetime import datetime, timedelta

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


def _unit_type(hours: float):
    """
    Returns the given unit type for the given amount of time.

    :param hours: referenced time
    :return: the hours unit if given a value larger than 1, otherwise the minutes unit
    """
    return Config.CUSTOM_HRS_TEXT if hours > 1 else Config.CUSTOM_MIN_TEXT


def _reformatted_time(hours: float, precision=2):
    """
    Returns a locale-formatted length of time.

    :param hours: referenced time
    :param precision: total digits to show after a decimal
    :return: hours if given a value larger than 1, otherwise minutes
    """
    val = round(hours, precision) if hours > 1 else round(hours * 60, precision)
    return f'{val:n}'


def filtered_html(html: str, revlog: list):
    return html


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
            dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
        else:
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


# use the same, gotten from append functions -> stats_html(), addon config in arg?
def cell_data_html():
    """
    :return: an html representation of a statistics-cell block
    """
    addon_config: dict = TimeStatsConfigManager(mw).config
    revlog = full_revlog(addon_config)

    cells_html = ''
    for cell_data in addon_config[Config.CELLS_DATA]:
        cell_html: str = cell_data[Config.HTML].replace('{{', '{').replace('}}', '}')
        cell_html = f'<div class="{COL_CLASS}">\n{cell_html}\n</div>'
        cell_html = filtered_html(cell_html, revlog)
        cells_html += cell_html.format(
            CellClass=f'{HORIZ_CLASS}' if cell_data[Config.DIRECTION] == Direction.HORIZONTAL else '',
            TitleColor=cell_data[Config.TITLE_COLOR],
            Title=cell_data[Config.TITLE],
            OutputColor=cell_data[Config.OUTPUT_COLOR],
            Output=cell_data[Config.OUTPUT],
        )
    return cells_html


def stats_html():
    return HTML_SHELL.replace("{cell_data}", cell_data_html())


def total_hrs_in_revlog(revlog: [[int, int]]):
    """
    Returns the total review time within a sequence of reviews.

    :param revlog: referenced log sequence
    :return: total hours in the sequence
    """
    return sum([log[1] for log in revlog[0:]]) / 1000 / 60 / 60


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


def _offset_hour():
    offset_hour = 0

    if TimeStatsConfigManager(mw).config[Config.USE_ROLLOVER]:
        if ANKI_VERSION > ANKI_LEGACY_VER:
            offset_hour = mw.col.get_preferences().scheduling.rollover
        else:
            offset_hour = mw.col.conf.get('rollover', ANKI_DEFAULT_ROLLOVER)

    return offset_hour


def date_with_rollover(date: datetime = datetime.today()):
    """
    Retrieves a date-time adjusted to its day-end hour and Anki/add-on preferences for end of day.

    :param date: date to adjust
    :return: an adjusted datetime object
    """

    return date.replace(hour=23, minute=59, second=59) - timedelta(hours=_offset_hour())


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
