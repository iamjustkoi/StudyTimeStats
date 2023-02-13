# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.
import re
import traceback
from datetime import datetime, timedelta
import calendar
from time import time
from typing import Sequence

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
    return Config.HRS_UNIT if hours > 1 else Config.MIN_UNIT


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


def filtered_html(html: str, addon_config: dict, cell_data: dict):
    updated_html = html
    initial_time = time()

    def sub_html(macro: str, revlog: list):
        nonlocal updated_html
        total_hrs = _total_hrs_in_revlog(revlog)
        unit_key = _unit_key_for_time(total_hrs)
        print(f'{cell_data[Config.TITLE]=}')
        print(f'{macro=}')
        print(f'{cell_data[Config.RANGE]=}')
        print(f'{total_hrs=}')
        updated_html = re.sub(
            fr'(?<!%){macro}',
            f'{_formatted_time(total_hrs)} {cell_data[unit_key]}',
            updated_html,
        )

    # Time

    cmd = CMD_TOTAL_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS]))

    cmd = CMD_RANGE_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(cell_data)))

    cmd = CMD_DAY_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.CUSTOM,
            Config.DAYS: 1,
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)))

    cmd = CMD_WEEK_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.WEEK,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)))

    cmd = CMD_TWO_WEEKS_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.TWO_WEEKS,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)))

    cmd = CMD_MONTH_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.MONTH,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)))

    cmd = CMD_YEAR_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.YEAR,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)))

    cmd = CMD_PREV_RANGE_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: cell_data[Config.RANGE],
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
            Config.DAYS: cell_data[Config.DAYS],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)))

    cmd = CMD_PREV_DAY_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.CUSTOM,
            Config.DAYS: 1,
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)))

    cmd = CMD_PREV_WEEK_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.WEEK,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)))

    cmd = CMD_PREV_TWO_WEEKS_HRS
    if re.search(fr'(?<!%){cmd}', updated_html):
        placeholder_data = {
            Config.RANGE: Range.TWO_WEEKS,
            Config.USE_CALENDAR: True,
            Config.WEEK_START: cell_data[Config.WEEK_START],
        }
        sub_html(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)))

    # cmd = CMD_PREV_MONTH_HRS
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass
    #
    # cmd = CMD_PREV_YEAR_HRS
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass
    #

    cmd = fr'{CMD_FROM_DATE_HRS}(\d\d\d\d-\d\d-\d\d)'
    max_warn_count = 3
    for match in re.findall(fr'(?<!%){cmd}', updated_html):
        try:
            # minus a day for inclusive checking
            from_date = date_with_rollover(datetime.fromisoformat(match)) - timedelta(days=1)
            from_time_ms = int(from_date.timestamp() * 1000)
            to_time_ms = int(date_with_rollover(datetime.today()).timestamp() * 1000)

            sub_html(
                fr'{CMD_FROM_DATE_HRS}{match}',
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], (from_time_ms, to_time_ms)),
            )
        except ValueError:
            if max_warn_count > 0:
                aqt.utils.showWarning(f'{traceback.format_exc()}')
                max_warn_count -= 1
            sub_html(cmd, [])

    # Text

    # cmd = CMD_RANGE
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_DATE
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_YEAR
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_FULL_DAY
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_DAY
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_DAYS
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_MONTH
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    # cmd = CMD_FULL_MONTH
    # if re.search(fr'(?<!%){cmd}', updated_html):
    #     pass

    print(f'Commands completed. Elapsed time: {((time() - initial_time) * 1000):2f}ms')
    print()

    return updated_html


def range_from_data(cell_data: dict, iterations=1) -> tuple[int, int]:
    to_date = date_with_rollover(datetime.utcnow())

    if cell_data[Config.RANGE] == Range.TOTAL:
        return 0, int(to_date.timestamp() * 1000)

    elif cell_data[Config.RANGE] == Range.CUSTOM:
        from_days = cell_data[Config.DAYS] * iterations + cell_data[Config.DAYS] - 1
        from_ms = int((to_date - timedelta(days=from_days)).timestamp() * 1000)

        to_days = cell_data[Config.DAYS] * (iterations - 1)
        to_ms = int((to_date - timedelta(days=to_days)).timestamp() * 1000)

        print(
            f'range={datetime.fromtimestamp(from_ms / 1000).strftime("%x(%H:%M)")} <=> '
            f'{datetime.fromtimestamp(to_ms / 1000).strftime("%x(%H:%M)")}'
        )

        return from_ms, to_ms

    else:
        if cell_data[Config.USE_CALENDAR]:
            if cell_data[Config.RANGE] in (Range.WEEK, Range.TWO_WEEKS):
                total_weekdays = Range.DAYS_IN[cell_data[Config.RANGE]]

                days_since_start = to_date.weekday() - cell_data[Config.WEEK_START]
                # Plus an extra interval, if past the current week's start-day
                days_since_start += 7 * (days_since_start > 0) + (7 * (total_weekdays == 14))

                # Days since the first day of the week + (iterations * weekdays) + weekdays
                delta_days = days_since_start + ((iterations - 1) * total_weekdays) + total_weekdays
                from_ms = int((to_date - timedelta(days=delta_days)).timestamp() * 1000)

                # Go forward again by 1 week, if iterating, else just use the current day
                to_delta_days = delta_days - ((iterations - 1) * total_weekdays) if iterations > 1 else 0
                to_ms = int((to_date - timedelta(days=to_delta_days)).timestamp() * 1000)

                return from_ms, to_ms

            elif cell_data[Config.RANGE] == Range.MONTH:
                # Approximating using 30 days then grabbing the resulting month's range
                delta_days = (30 * (iterations - 1))

                # inclusive (goes back 1 more day)
                from_date = (to_date - timedelta(days=delta_days)).replace(day=1) + timedelta(days=-1)

                # If iterations are set, use the first day of the month for the end of the range, instead
                if iterations > 1:
                    month_range = calendar.monthrange(from_date.year, from_date.month)[1]
                    to_date = (from_date + timedelta(days=month_range))

                from_ms = int(from_date.timestamp() * 1000)
                to_ms = int(to_date.timestamp() * 1000)
                return from_ms, to_ms

            elif cell_data[Config.RANGE] == Range.YEAR:
                # inclusive (extra day added)
                delta_days = 1
                to_ms = int(to_date.timestamp() * 1000)

                if iterations > 1:
                    current_year = to_date.year
                    # update to_ms to be the previous year's time

                    for i in range(iterations - 1):
                        current_year -= 1
                        delta_days += calendar.isleap(current_year - 1) and 366 or 365
                        to_ms = int(to_date.replace(year=current_year, month=12, day=31).timestamp() * 1000)

                from_ms = int((to_date.replace(month=1, day=1) - timedelta(days=delta_days)).timestamp() * 1000)

                return from_ms, to_ms

        elif not cell_data[Config.USE_CALENDAR]:
            from_days = Range.DAYS_IN[cell_data[Config.RANGE]] * iterations + (
                    Range.DAYS_IN[cell_data[Config.RANGE]] > 1)
            from_ms = int((to_date - timedelta(days=from_days)).timestamp() * 1000)

            to_days = Range.DAYS_IN[cell_data[Config.RANGE]] * (iterations - 1)
            to_ms = int((to_date - timedelta(days=to_days)).timestamp() * 1000)

            return from_ms, to_ms


def filtered_revlog(excluded_dids: list = None, time_range_ms: tuple[int, int] = None, include_deleted=False) \
        -> list[Sequence]:
    if include_deleted and mw.state != 'overview':
        # If not currently viewing a deck, including deleted decks, grab all non-excluded deck ids
        filtered_did_cmd = f'WHERE cards.did NOT IN {_args_from_ids(excluded_dids) if excluded_dids else ""}'
    else:
        # Grab the current parent/children deck ids (inclusive) if viewing a deck, else grab all deck ids (inclusive)
        if mw.state == 'overview':
            included_dids = [
                i for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))
                if str(i) not in excluded_dids
            ]
        else:
            included_dids = [
                name_id.id for name_id in mw.col.decks.all_names_and_ids()
                if str(name_id) not in excluded_dids
            ]
        filtered_did_cmd = f'WHERE cards.did IN {_args_from_ids(included_dids)}'

    # SQL
    # Select id (unix time), time (elapsed review time) from review logs
    # Join revlog cid with cards id, and use when comparing the cid vs the did of the review
    #   (revlog doesn't contain a deck id column)
    # Select id (unix time) between the (optional) unix time range, else end query (;)
    revlog_cmd = f'''
        SELECT revlog.id, revlog.time
        FROM revlog
        INNER JOIN cards
        ON revlog.cid = cards.id
        {filtered_did_cmd}       
    ''' + (f' AND revlog.id BETWEEN {time_range_ms[0]} AND {time_range_ms[1]};' if time_range_ms else ';')

    return mw.col.db.all(revlog_cmd)


def days_since_week_start(
    week_start_day: int,
    current_day: int
):
    """
    Gets days since the last week-start date based on a set number of weeks.

    :param week_start_day: start of the week to count total days from
    :param current_day: an integer representation of the current week-day
    :return: days since week start
    """

    # Adds an extra week if the current day is already past the week start
    return current_day - week_start_day - (7 * (current_day >= week_start_day))


def date_with_rollover(date: datetime = datetime.today()):
    """
    Retrieves a date-time adjusted to its day-end hour and Anki/add-on preferences for end of day.

    :param date: date to adjust
    :return: an adjusted datetime object
    """
    return date.replace(hour=23, minute=59, second=59) + timedelta(hours=_offset_hour())
