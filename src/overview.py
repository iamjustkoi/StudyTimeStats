# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.
import calendar
import re
from datetime import datetime, timedelta
from time import time
from typing import List, Sequence, Tuple

from anki.decks import DeckTreeNode
from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.overview import Overview, OverviewContent
from aqt.webview import AnkiWebView

from .config import ANKI_VERSION, TimeStatsConfigManager
from .consts import *

if ANKI_VERSION > ANKI_LEGACY_VER + 1:
    # noinspection PyUnresolvedReferences
    from anki.consts import (
        REVLOG_RESCHED,
        QUEUE_TYPE_SUSPENDED,
        QUEUE_TYPE_LRN,
        QUEUE_TYPE_NEW,
        QUEUE_TYPE_REV,
        QUEUE_TYPE_DAY_LEARN_RELEARN,
        QUEUE_TYPE_MANUALLY_BURIED,
        QUEUE_TYPE_SIBLING_BURIED,
    )
else:
    QUEUE_TYPE_MANUALLY_BURIED = -3
    QUEUE_TYPE_SIBLING_BURIED = -2
    QUEUE_TYPE_SUSPENDED = -1
    QUEUE_TYPE_NEW = 0
    QUEUE_TYPE_LRN = 1
    QUEUE_TYPE_REV = 2
    QUEUE_TYPE_DAY_LEARN_RELEARN = 3
    REVLOG_RESCHED = 4

CARD_STATE = {
    SUSPENDED: QUEUE_TYPE_SUSPENDED,
    MAN_BURIED: QUEUE_TYPE_MANUALLY_BURIED,
    SIB_BURIED: QUEUE_TYPE_SIBLING_BURIED,
    NEW: QUEUE_TYPE_NEW,
    LEARN: QUEUE_TYPE_LRN,
    REVIEW: QUEUE_TYPE_REV,
    RELEARN: QUEUE_TYPE_DAY_LEARN_RELEARN,
}

cached_logs: dict = {}


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

        # Swap duplicate spaces characters with non-breaking space characters
        updated_title = cell_data[Config.TITLE].replace('  ', '&nbsp;&nbsp;')
        updated_output = cell_data[Config.OUTPUT].replace('  ', '&nbsp;&nbsp;')

        cell_html = cell_html.format(
            CellClass=HORIZ_CELL_CLASS if cell_data[Config.DIRECTION] == Direction.HORIZONTAL else VERT_CELL_CLASS,
            TitleColor=cell_data[Config.TITLE_COLOR],
            Title=updated_title,
            OutputColor=cell_data[Config.OUTPUT_COLOR],
            Output=updated_output,
        )

        cells_html += parsed_string(cell_html, addon_config, cell_data)

    return cells_html


def clear_cached_logs():
    global cached_logs
    cached_logs = {}


def stats_html():
    clear_cached_logs()
    return HTML_SHELL.replace("{cell_data}", cell_data_html())


# May want to convert this to a class, instead (caching, function access, multiple queries, etc.)
def parsed_string(string: str, addon_config: dict, cell_data: dict):
    updated_string = string
    _cached_range_time_ms: Tuple[int, int] = 0, 0

    initial_time = time()

    def _precision(text):
        """
        Searches for the precision modifier in the given text and outputs a precision value, if one is found.
        :param text: Command text to search through.
        :return: An integer representing the processed decimal precision.
        """
        precision_match = re.search(fr'{Macro.CMD_PRECISION}{{({Macro.PRECISION_EXTRA})}}', text)
        return int(precision_match.group(1)) if precision_match else None

    def _states(pattern):
        """
        Searches for the state modifier in the given text and outputs a list of card states, if found.
        :param pattern: Command text to search through.
        :return: A list of integers representing the processed card state(s).
        """
        matches = re.search(fr'{Macro.CMD_STATE}{{({Macro.STATE_EXTRA})}}', pattern)
        states = []
        if matches:
            match = matches.group(1)
            # Quick way to merge learn and relearn states
            match = re.sub(rf'\b{LEARN}\b', f'{LEARN},{RELEARN}', match)
            match = re.sub(rf'\b{BURIED}\b', f'{SIB_BURIED},{MAN_BURIED}', match)

            state_strings = match.split(',')
            states = [CARD_STATE[state] for state in state_strings if state in CARD_STATE.keys()]

        return states

    def _time_pattern(pattern: str):
        # Prepended "any" character ('.') so only macros with the character's context are matched
        return '.' \
            + f'(?<!%){pattern}' \
            + fr'(?:{Macro.CMD_PRECISION}{{{Macro.PRECISION_EXTRA}}}|{Macro.CMD_STATE}{{{Macro.STATE_EXTRA}}})*'

    def _review_pattern(pattern: str):
        # Prepended "any" character ('.') so only macros with the character's context are matched
        return '.' \
            + f'(?<!%){pattern}' \
            + fr'(?:{Macro.CMD_STATE}{{{Macro.STATE_EXTRA}}})?'

    def _cached_log(cmd, excluded_dids: list = None, time_range_ms: Tuple[int, int] = None):
        global cached_logs
        cached_log = cached_logs.get(cmd, None)

        if cached_log:
            return cached_log

        filtered_log = filtered_revlog(excluded_dids, time_range_ms)
        cached_logs[cmd] = filtered_log

        return filtered_log

    def _cache_key(cmd: str, extra):
        # Basic, repeatable joiner method
        return cmd + '<' + str(extra) + '>'

    def time_macros():
        # Time
        cmd = Macro.CMD_TOTAL_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            _update_string_time(match, _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS]))

        cmd = Macro.CMD_RANGE_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            _update_string_time(
                match,
                _cached_log(
                    _cache_key(cmd, cell_data[Config.RANGE]),
                    addon_config[Config.EXCLUDED_DIDS],
                    _range_time_ms(),
                ),
            )

        cmd = Macro.CMD_DAY_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)),
            )

        cmd = Macro.CMD_WEEK_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)),
            )

        cmd = Macro.CMD_TWO_WEEKS_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)),
            )

        cmd = Macro.CMD_MONTH_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)),
            )

        cmd = Macro.CMD_YEAR_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data)),
            )

        cmd = Macro.CMD_PREVIOUS_RANGE_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: cell_data[Config.RANGE],
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
                Config.DAYS: cell_data[Config.DAYS],
            }
            _update_string_time(
                match,
                _cached_log(
                    _cache_key(cmd, cell_data[Config.RANGE]),
                    addon_config[Config.EXCLUDED_DIDS],
                    range_from_data(placeholder_data, 2),
                ),
            )

        cmd = Macro.CMD_PREVIOUS_DAY_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)),
            )

        cmd = Macro.CMD_PREVIOUS_WEEK_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)),
            )

        cmd = Macro.CMD_PREVIOUS_TWO_WEEKS_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)),
            )

        cmd = Macro.CMD_PREVIOUS_MONTH_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)),
            )

        cmd = Macro.CMD_PREVIOUS_YEAR_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
            }
            _update_string_time(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2)),
            )

        def _avg_hrs_per_card(in_logs):
            return (_total_hrs_in_revlog(in_logs) / len(in_logs)) if len(in_logs) > 0 else 0

        cmd = Macro.CMD_ETA_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            logs = _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS])

            # Grab total cards due
            current_did = mw.col.decks.current().get('id') if mw.state == 'overview' else None
            due_tree = mw.col.sched.deck_due_tree(current_did)

            def _total_due_in_tree(tree: DeckTreeNode):
                """
                Recursively grabs the total cards due for a given deck node.

                :param tree: The DeckNodeTree to use when grabbing delays/card totals.
                :return: The total number of cards due for the given node.
                """
                out_total = 0

                # If children found in tree, recursively combine their due cards
                if tree.children and len(tree.children) > 0:
                    for child in tree.children:
                        out_total += _total_due_in_tree(child)

                # Else, output the current due-card total using the deck config group's new-card steps (delays)
                else:
                    deck_conf = _conf_for_did(tree.deck_id)

                    # Check for filtered/dynamic deck
                    if deck_conf and deck_conf.get('new', None):
                        delays = len(deck_conf['new'].get('delays', [0]))

                        out_total = (delays * tree.new_count) + tree.learn_count + tree.review_count

                return out_total

            # Build output
            eta_hrs = _avg_hrs_per_card(logs) * _total_due_in_tree(due_tree)
            unit_key = _unit_key_for_time(eta_hrs)

            _sub_text(
                match,
                f'{_formatted_time(eta_hrs, _precision(match), addon_config[Config.USE_DECIMAL])} '
                f'{cell_data[unit_key]}',
            )

        cmd = fr'{Macro.CMD_FROM_DATE_HOURS}:(\d\d\d\d-\d\d-\d\d)'
        pattern = _time_pattern(cmd)
        for match in re.findall(fr'(?<!%){pattern}(?!:\d)', updated_string):
            match: str
            _process_range(match, replace_cb=_update_string_time, cmd=Macro.CMD_FROM_DATE_HOURS)

        cmd = fr'{Macro.CMD_FROM_DATE_HOURS}:(\d\d\d\d-\d\d-\d\d):(\d\d\d\d-\d\d-\d\d)'
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            match: Tuple[str]
            _process_range(match[0], match[1], replace_cb=_update_string_time, cmd=Macro.CMD_FROM_DATE_HOURS)

        # Avg
        cmd = Macro.CMD_DAY_AVERAGE_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            logs = _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], _range_time_ms())
            from_date = datetime.fromtimestamp(_range_time_ms()[0] / 1000)
            to_date = datetime.fromtimestamp(_range_time_ms()[1] / 1000)
            days_in_logs = (to_date - from_date).days
            avg_hrs = _total_hrs_in_revlog(logs) / (days_in_logs if days_in_logs > 0 else 1)
            unit_key = _unit_key_for_time(avg_hrs)
            _sub_text(
                match,
                f'{_formatted_time(avg_hrs, _precision(match), addon_config[Config.USE_DECIMAL])} '
                f'{cell_data[unit_key]}',
            )

        cmd = Macro.CMD_CARD_AVERAGE_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            logs = _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], _range_time_ms())
            avg_hrs = _avg_hrs_per_card(logs)
            unit_key = _unit_key_for_time(avg_hrs)

            _sub_text(
                match,
                f'{_formatted_time(avg_hrs, _precision(match), addon_config[Config.USE_DECIMAL])} '
                f'{cell_data[unit_key]}',
            )

        cmd = Macro.CMD_HIGHEST_DAY_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log()
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _sub_text(
                match,
                f'{_formatted_time(hours, _precision(match), addon_config[Config.USE_DECIMAL])} {cell_data[unit_key]}',
            )

        cmd = Macro.CMD_HIGHEST_WEEK_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            # Set weekday to -1 of itself
            #  Note: SQLite's STRFTIME has Sunday at 0, while datetime (Python) has Monday at 0
            weekday_for_modifier = cell_data[Config.WEEK_START] - 1
            weekday_for_modifier += 7 if weekday_for_modifier < 0 else 0
            max_log = _highest_date_modified_log([f'weekday {weekday_for_modifier}'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _sub_text(
                match,
                f'{_formatted_time(hours, _precision(match), addon_config[Config.USE_DECIMAL])} {cell_data[unit_key]}',
            )

        cmd = Macro.CMD_HIGHEST_MONTH_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log(['start of month'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _sub_text(
                match,
                f'{_formatted_time(hours, _precision(match), addon_config[Config.USE_DECIMAL])} {cell_data[unit_key]}',
            )

        cmd = Macro.CMD_HIGHEST_YEAR_HOURS
        pattern = _time_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log(['start of year'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)

            _sub_text(
                match,
                f'{_formatted_time(hours, _precision(match), addon_config[Config.USE_DECIMAL])} {cell_data[unit_key]}',
            )

    def review_macros():
        # Reviews
        cmd = Macro.CMD_TOTAL_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            _update_string_reviews(match, _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS]))

        cmd = Macro.CMD_RANGE_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            _update_string_reviews(
                match,
                _cached_log(
                    _cache_key(cmd, cell_data[Config.RANGE]),
                    addon_config[Config.EXCLUDED_DIDS],
                    _range_time_ms()
                ),
            )

        cmd = Macro.CMD_DAY_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_WEEK_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_TWO_WEEKS_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_MONTH_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_YEAR_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_PREVIOUS_RANGE_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: cell_data[Config.RANGE],
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
                Config.DAYS: cell_data[Config.DAYS],
            }
            _update_string_reviews(
                match,
                _cached_log(
                    _cache_key(cmd, cell_data[Config.RANGE]),
                    addon_config[Config.EXCLUDED_DIDS],
                    range_from_data(placeholder_data, 2)
                ),
            )

        cmd = Macro.CMD_PREVIOUS_DAY_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREVIOUS_WEEK_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREVIOUS_TWO_WEEKS_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREVIOUS_MONTH_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREVIOUS_YEAR_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
            }
            _update_string_reviews(
                match,
                _cached_log(cmd, addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = fr'{Macro.CMD_FROM_DATE_REVIEWS}:(\d\d\d\d-\d\d-\d\d)(?!:)'
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            match: str
            _process_range(match, replace_cb=_update_string_reviews, cmd=Macro.CMD_FROM_DATE_REVIEWS)

        cmd = fr'{Macro.CMD_FROM_DATE_REVIEWS}:(\d\d\d\d-\d\d-\d\d):(\d\d\d\d-\d\d-\d\d)'
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            match: Tuple[str]
            _process_range(match[0], match[1], replace_cb=_update_string_reviews, cmd=Macro.CMD_FROM_DATE_REVIEWS)

        cmd = Macro.CMD_HIGHEST_DAY_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log(order_by='count')
            reviews = max_log[2]
            _sub_text(match, str(reviews))

        cmd = Macro.CMD_HIGHEST_WEEK_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            # Set weekday to -1 of itself
            #  Note: SQLite's STRFTIME has Sunday at 0, while datetime (Python) has Monday at 0
            weekday_for_modifier = cell_data[Config.WEEK_START] - 1
            weekday_for_modifier += 7 if weekday_for_modifier < 0 else 0
            max_log = _highest_date_modified_log([f'weekday {weekday_for_modifier}'], order_by='count')
            reviews = max_log[2]
            _sub_text(match, str(reviews))

        cmd = Macro.CMD_HIGHEST_MONTH_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log(['start of month'], order_by='count')
            reviews = max_log[2]
            _sub_text(match, str(reviews))

        cmd = Macro.CMD_HIGHEST_YEAR_REVIEWS
        pattern = _review_pattern(cmd)
        for match in re.findall(pattern, updated_string):
            max_log = _highest_date_modified_log(['start of year'], order_by='count')
            reviews = max_log[2]
            _sub_text(match, str(reviews))

    def text_macros():
        # Text
        cmd = Macro.CMD_RANGE
        if re.search(fr'(?<!%){cmd}', updated_string):
            if cell_data[Config.RANGE] == Range.CUSTOM:
                repl = f'{cell_data[Config.DAYS]} {String.DAYS}'
            elif cell_data[Config.RANGE] == Range.TOTAL:
                repl = String.TOTAL
            else:
                repl = Range.LABEL[cell_data[Config.RANGE]]

            _sub_text(cmd, repl, False)

        cmd = Macro.CMD_DATE
        if re.search(fr'(?<!%){cmd}(?!:)', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime("%x"), False)

        cmd = Macro.CMD_DATE_FORMATTED
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: str
            date_format = match[(match.find("\"") + 1):(match.rfind("\""))]
            _sub_text(match, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime(date_format), False)

        cmd = Macro.CMD_YEAR
        if re.search(fr'(?<!%){cmd}', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%Y'), False)

        cmd = Macro.CMD_FULL_DAY
        if re.search(fr'(?<!%){cmd}', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%A'), False)

        cmd = Macro.CMD_DAY
        if re.search(fr'(?<!%){cmd}', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%a'), False)

        cmd = Macro.CMD_MONTH
        if re.search(fr'(?<!%){cmd}', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%b'), False)

        cmd = Macro.CMD_FULL_MONTH
        if re.search(fr'(?<!%){cmd}', updated_string):
            _sub_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%B'), False)

        cmd = Macro.CMD_DAYS
        if re.search(fr'(?<!%){cmd}', updated_string):
            from_date = datetime.fromtimestamp(_range_time_ms()[0] / 1000)
            to_date = date_with_rollover(datetime.today())
            delta_days = (to_date - from_date).days
            _sub_text(cmd, str(delta_days), False)

    def eval_macros():
        """
        Evaluates and formats calc expressions in the cell's html.
        """
        matches = re.findall(fr'(?<!%){Macro.CMD_EVAL}([^}}]*)}}', updated_string)
        for match in matches:
            match: str
            is_using_hours = False
            expression = match
            escaped_match = match.replace('+', r'\+').replace('*', r'\*').replace('-', r'\-')  # .replace('.', r'\.')
            precision = _precision(fr'{Macro.CMD_EVAL}{escaped_match}\}}')
            repl = f'{Macro.CMD_EVAL}{match}}}'

            if f' {cell_data[Config.MIN_UNIT]}' in expression:
                is_using_hours = True
                # Remove units from the expression
                expression = re.sub(
                    fr'(\d+)\s{cell_data[Config.MIN_UNIT]}',
                    lambda m: str(int(m.group(1)) * 60),
                    expression,
                )

            if f' {cell_data[Config.HRS_UNIT]}' in expression:
                is_using_hours = True
                # Remove units from the expression
                expression = re.sub(fr'\s+{cell_data[Config.HRS_UNIT]}', '', expression)

            # ! INSECURE !
            #  Leaving open-ended, for now, may want to do some more checks depending on use-cases
            try:
                # print(f'{expression=}')
                result = eval(expression)
            except ValueError or SyntaxError:
                result = String.ERR
                is_using_hours = False

            if is_using_hours:
                unit_key = _unit_key_for_time(result)
                _sub_text(
                    repl,
                    f'{_formatted_time(result, precision, addon_config[Config.USE_DECIMAL])}'
                    f' {cell_data[unit_key]}',
                )

            else:
                _sub_text(
                    repl,
                    f'{round(result, precision):n}' if isinstance(result, float) else str(result),
                )

    def _logs_with_states(revlog: list, card_states: List[int]):
        filtered_logs = []
        # matches = re.search(fr'{repl}\S*{Macro.CMD_STATE}{Macro.STATE_EXTRA}', updated_string)
        # extra_strings.append(fr'{Macro.CMD_STATE}\{{{matches.group(1) if matches else ""}\}}')

        # print(f'{card_states=}')

        for log in revlog:
            # print(f'{int(log[2])=}')
            if int(log[2]) in card_states:
                filtered_logs.append(log)

        return filtered_logs

    def _update_string_time(repl: str, revlog: list = None):
        nonlocal updated_string

        if revlog is None:
            _sub_text(
                repl,
                'ERR'
            )
            return

        card_states = _states(repl)
        precision = _precision(repl)

        filtered_logs = _logs_with_states(revlog, card_states) if card_states else revlog

        total_hrs = _total_hrs_in_revlog(filtered_logs)
        unit_key = _unit_key_for_time(total_hrs)

        _sub_text(
            repl,
            f'{_formatted_time(total_hrs, precision, addon_config[Config.USE_DECIMAL])} {cell_data[unit_key]}'
        )

    def _update_string_reviews(repl: str, revlog: list = None):
        nonlocal updated_string

        if revlog is None:
            updated_string = re.sub(fr'(?<!%){repl}', f'ERR', updated_string)
            return

        card_states = _states(repl)
        filtered_logs = _logs_with_states(revlog, card_states) if card_states else revlog

        total_reviews = len(filtered_logs)

        _sub_text(repl, str(total_reviews))

    def _sub_text(repl: str, text: str, has_context_char=True):
        nonlocal updated_string
        if has_context_char and repl[0] != '%':
            text = repl[0] + text

        # print(f'repl="{repl}", text="{text}"')

        updated_string = updated_string.replace(repl, text)

    def _process_range(from_date_str: str, to_date_str: str = None, replace_cb=None, cmd=Macro.CMD_FROM_DATE_HOURS):
        """
        Processes a date range and calls the replace_cb callable using a filtered revlog based on the input date range.

        :param from_date_str: A string representing the starting date in ISO format.
        :param to_date_str: A string representing the ending date in ISO format. If None, today's date is used.
        :param replace_cb: A callback function to replace the matched pattern using the filtered revlog.
        :param cmd: A string representing the command to be used in the matched pattern (e.g. <pattern>:<from>:<to>).
        """
        try:
            # minus a day for inclusive checking
            from_date_raw = datetime.fromisoformat(from_date_str)
            from_date = date_with_rollover(from_date_raw) - timedelta(days=1)
            from_ms = int(from_date.timestamp() * 1000)

            if to_date_str:
                to_date_raw = datetime.fromisoformat(to_date_str)
                to_date = date_with_rollover(to_date_raw)
                to_ms = int(to_date.timestamp() * 1000)
                if replace_cb:
                    repl = fr'{cmd}:{from_date_str}:{to_date_str}'
                    replace_cb(
                        repl,
                        _cached_log(repl, addon_config[Config.EXCLUDED_DIDS], (from_ms, to_ms)),
                    )

            else:
                to_date_raw = datetime.today()
                to_ms = int(date_with_rollover(to_date_raw).timestamp() * 1000)
                if replace_cb:
                    repl = fr'{cmd}:{from_date_str}'
                    replace_cb(
                        repl,
                        _cached_log(repl, addon_config[Config.EXCLUDED_DIDS], (from_ms, to_ms)),

                    )

        except ValueError:
            if replace_cb:
                replace_cb(fr'{cmd}:{from_date_str}(:{to_date_str})?', None)

    def _range_time_ms() -> Tuple[int, int]:
        """
        Retrieves the current range from cell data and caches it for future range calls.
        :return:  Tuple of range times in unix milliseconds, with the format: [from, to]
        """
        nonlocal _cached_range_time_ms

        if _cached_range_time_ms == (0, 0):
            if cell_data[Config.RANGE] == Range.TOTAL:
                review_id = mw.col.db.first('''SELECT id FROM revlog ORDER BY id''')

                if not review_id:
                    review_id = [0]

                _cached_range_time_ms = int(review_id[0]), range_from_data(cell_data)[1]

            else:
                _cached_range_time_ms = range_from_data(cell_data)

        return _cached_range_time_ms

    def _highest_date_modified_log(
        modifiers: [str] = None,
        timerange: Tuple[int, int] = _range_time_ms(),
        order_by='time',
    ) -> Sequence:
        """
        Grabs a log with the highest total time and highest total reviews found in the selected range,
        suggested by the given date modifier. Always uses the 'start of day' modifier to group queries.

        :param modifiers: A list of string values used to format review log timestamps
         and group them using the selected modified outputs.

        (e.g. 'start of day', 'weekday', 'start of month', 'start of year', etc.)

        https://www.sqlite.org/lang_datefunc.html#modifiers

        :return: A single sequence with the timestamp and total time in a grouped range:
         [timestamp, total time, review count]
        """

        modifiers = ['start of day'] if not modifiers else modifiers + ['start of day']
        range_limit = f'AND revlog.id BETWEEN {timerange[0]} AND {timerange[1]}' if timerange else ''

        sql_query = f'''
            SELECT CAST(
                -- Formatted row ids as unix milliseconds, with offset hours
                STRFTIME(
                    '%s', (revlog.id / 1000),
                    'unixepoch',
                    'localtime',
                    '{-_offset_hour()} hours',
                    '{"','".join(modifiers)}'
                ) AS int
            ) AS startOfRange,
            -- Total time in filtered range groups          
            SUM(revlog.time) as time,
            count(*) as count
            -- Search in revlog table
            FROM revlog
            -- Map revlog cid to cards id for selecting deck-id's from the cards table
            LEFT JOIN cards
            ON revlog.cid = cards.id
            -- Select reviews only, excluding preset decks, between "range_limit" range
            WHERE revlog.type < {REVLOG_RESCHED}
            {_excluded_did_limit(addon_config[Config.EXCLUDED_DIDS])}
            {range_limit}
            -- Get highest value via group, sort, and the first (highest) row
            GROUP BY startOfRange
            ORDER BY {order_by} DESC LIMIT 1;
        '''

        # print(f'sql_cmd={sql_query}')

        max_log = mw.col.db.first(sql_query)
        if not max_log:
            print(f'max_log returned an emtpy array for selected modifier(s): {modifiers}')
            max_log = [0, 0, 0]

        return max_log

    time_macros()
    review_macros()
    text_macros()
    eval_macros()

    # Combine leftover symbols
    updated_string = updated_string.replace('%%', '%')

    print(f'Commands completed. Elapsed time: {((time() - initial_time) * 1000):2f}ms', end='\n\n')

    return updated_string


def range_from_data(cell_data: dict, iterations=1) -> Tuple[int, int]:
    """
    Retrieve a time range tuple. Adjusted for preferred rollover/offset hour.
    :param cell_data: Template data used to distinguish target return data.
    :param iterations: Number of range-type to go back by when selecting a specific range
    (e.g. 1 week iteration = this week, 2 week iterations = previous week).
    :return: Tuple with a time range via milliseconds since unix epoch: [from, to].
    """
    to_date = date_with_rollover(datetime.today())
    from_ms, to_ms = 0, 0

    if cell_data[Config.RANGE] == Range.TOTAL:
        return 0, int(to_date.timestamp() * 1000)

    elif cell_data[Config.RANGE] == Range.CUSTOM:
        from_days = cell_data[Config.DAYS] * iterations
        from_ms = int((to_date - timedelta(days=from_days)).timestamp() * 1000)

        to_days = cell_data[Config.DAYS] * (iterations - 1)
        to_ms = int((to_date - timedelta(days=to_days)).timestamp() * 1000)

    else:
        if cell_data[Config.USE_CALENDAR]:
            if cell_data[Config.RANGE] in (Range.WEEK, Range.TWO_WEEKS):
                total_weekdays = Range.DAYS_IN[cell_data[Config.RANGE]]

                days_since_start = (to_date.weekday() % 7) - cell_data[Config.WEEK_START]

                # Plus an extra interval, if past the current week's start-day
                days_since_start += 7 * (days_since_start < 0) + (7 * (total_weekdays == 14))

                # Days since the first day of the week + (iterations * weekdays) + weekdays
                delta_days = days_since_start + 1 + ((iterations - 1) * total_weekdays) + (7 * (total_weekdays == 14))

                from_ms = int((to_date - timedelta(days=delta_days)).timestamp() * 1000)

                # Go forward again by 1 week, if iterating, else just use the current day
                to_delta_days = delta_days - ((iterations - 1) * total_weekdays) if iterations > 1 else 0
                to_ms = int((to_date - timedelta(days=to_delta_days)).timestamp() * 1000)

            elif cell_data[Config.RANGE] == Range.MONTH:
                # Approximating using 30 days then grabbing the resulting month's range
                delta_days = (30 * (iterations - 1))

                # - inclusive (goes back 1 more day)
                # - get the date with a rollover, again, since the new time uses a replacement for the day
                #    (not just using a time delta, anymore)
                from_date = date_with_rollover(
                    (to_date - timedelta(days=delta_days)).replace(day=1)  # - timedelta(days=1)
                )

                # If iterations are set, use the first day of the month for the end of the range, instead
                if iterations > 1:
                    month_range = calendar.monthrange(from_date.year, from_date.month)[1]
                    to_date = (from_date + timedelta(days=month_range))

                from_ms = int(from_date.timestamp() * 1000)
                to_ms = int(to_date.timestamp() * 1000)

            elif cell_data[Config.RANGE] == Range.YEAR:
                # # inclusive (extra day added)
                # delta_days = 1
                delta_days = 0
                to_ms = int(to_date.timestamp() * 1000)

                if iterations > 1:
                    current_year = to_date.year

                    for i in range(iterations - 1):
                        current_year -= 1
                        delta_days += calendar.isleap(current_year - 1) and 366 or 365
                        to_ms = int(to_date.replace(year=current_year, month=12, day=31).timestamp() * 1000)

                from_ms = int((to_date.replace(month=1, day=1) - timedelta(days=delta_days)).timestamp() * 1000)

        elif not cell_data[Config.USE_CALENDAR]:
            from_days = Range.DAYS_IN[cell_data[Config.RANGE]] * iterations + \
                        (Range.DAYS_IN[cell_data[Config.RANGE]] > 1)
            from_ms = int((to_date - timedelta(days=from_days)).timestamp() * 1000)

            to_days = Range.DAYS_IN[cell_data[Config.RANGE]] * (iterations - 1)
            to_ms = int((to_date - timedelta(days=to_days)).timestamp() * 1000)

    # print(
    #     f'range={datetime.fromtimestamp(from_ms / 1000).strftime("%x(%H:%M)")} '
    #     f'-> {datetime.fromtimestamp(to_ms / 1000).strftime("%x(%H:%M)")}'
    # )

    return from_ms, to_ms


def filtered_revlog(excluded_dids: list = None, time_range_ms: Tuple[int, int] = None) \
        -> list[Sequence]:
    """
    Grabs a list of review data logs which each have the format: [timestamp, timerange, review-queue].
    :param excluded_dids: A list of excluded deck id's
    :param time_range_ms: A tuple with the accepted unix millisecond time range with the format: (from, to)
    :return:
    """

    # SQL
    # Select id (unix time), time (elapsed review time) from review logs
    # Join revlog cid with cards id, and use when comparing the cid vs the did of the review
    #   (revlog doesn't contain a deck id column)
    # Where review type isn't a reschedule (or potentially unlisted others above it)
    # (Optional: select cards in included decks)
    # Select id (unix time) between the (optional) unix time range, else end query (;)
    revlog_cmd = f'''
        SELECT revlog.id, revlog.time, cards.queue
        FROM revlog
        LEFT JOIN cards
        ON revlog.cid = cards.id
        WHERE revlog.type < {REVLOG_RESCHED}
        {_excluded_did_limit(excluded_dids)}
        {f'AND revlog.id BETWEEN {time_range_ms[0]} AND {time_range_ms[1]}' if time_range_ms else ''}        
        ORDER BY revlog.cid;
    '''

    return mw.col.db.all(revlog_cmd)


def date_with_rollover(date: datetime = datetime.today()):
    """
    Retrieves a date-time adjusted to its day-end hour and Anki/add-on preferences for end of day.

    :param date: Date to adjust
    :return: An adjusted datetime object
    """
    return date.replace(hour=23, minute=59, second=59) + timedelta(hours=_offset_hour())


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


def _cards_in_queue(card_states: List[int] = None):
    return f'AND cards.queue IN {_args_from_ids(card_states)}' if card_states and len(card_states) > 0 else ''


def _unit_key_for_time(hours: float):
    """
    Returns the given unit key for the given amount of time.

    :param hours: referenced time
    :return: the hours unit if given a value larger than 1, otherwise the minutes unit
    """
    return Config.HRS_UNIT if hours > 1 else Config.MIN_UNIT


def _formatted_time(hours: float, precision: int = None, use_decimal=True):
    """
    Returns a locale-formatted length of time.

    :param hours: referenced time
    :param precision: total digits to show after a decimal
    :param use_decimal: whether to use the hh:mm format instead of a decimal for the output value

    :return: hours if given a value larger than 1, otherwise minutes
    """

    if precision is None:
        precision = 2

    if use_decimal:
        val = round(hours, precision) if hours > 1 else round(hours * 60, precision)
        return f'{val:n}'
    else:
        # Contributed by x51mon
        hour_only = int(hours)
        min_and_sec = (hours - hour_only) * 60
        min_only = int(min_and_sec)
        sec_only = (min_and_sec - min_only) * 60

        return str(hour_only) + ':' + "{:02.0f}".format(min_only) if hours > 1 \
            else str(min_only) + ':' + "{:02.0f}".format(sec_only)


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


def _conf_for_did(did: int):
    """
    Returns the configuration for the requested deck id (did).
    If a configuration is already associated with the deck, it is returned as-is.
    Otherwise, the default configuration is returned.

    Custom method used instead of Anki's method to hopefully future-proof it a bit.

    :param did: Integer representation for a deck's id.
    :return: A json object with the config values for a given deck, or the default deck's config.
    """
    deck = mw.col.decks.get(did, default=False)
    assert deck
    if "conf" in deck:
        conf = mw.col.decks.get_config(int(deck["conf"]))
        if not conf:
            # fall back on default
            conf = mw.col.decks.get_config("0")
        conf["dyn"] = False
        return conf
    # dynamic decks have embedded conf
    return deck


def _excluded_did_limit(excluded_dids: list = None):
    """
    Retrieves an SQL limiter with a leading "AND" operator that checks if "cards.did" are
    in the set of excluded deck id's using all currently visible decks.
    :param excluded_dids: A list of deck id's to be excluded (expects integers, execution may vary)
    """
    if len(excluded_dids) > 0:
        include_deleted = TimeStatsConfigManager(mw).config.get(Config.INCLUDE_DELETED, False)

        if include_deleted and mw.state != 'overview':
            # If not currently viewing a deck, including deleted decks, grab all non-excluded deck ids
            filtered_did_cmd = f'AND cards.did NOT IN {_args_from_ids(excluded_dids) if excluded_dids else ""}'

        else:
            # If currently in a deck's overview: grab the current deck's parent/children deck ids (inclusive)
            if mw.state == 'overview':
                included_dids = [
                    i for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))
                    if i not in excluded_dids
                ]

            # Else, grab all deck ids (inclusive)
            else:
                included_dids = [
                    name_id.id for name_id in mw.col.decks.all_names_and_ids()
                    if name_id.id not in excluded_dids
                ]

            filtered_did_cmd = f'AND cards.did IN {_args_from_ids(included_dids)}'
    else:
        filtered_did_cmd = ''

    return filtered_did_cmd
