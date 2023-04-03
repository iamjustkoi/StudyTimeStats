# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.
import calendar
import re
from datetime import datetime, timedelta
from time import time
from typing import Sequence

from anki.consts import REVLOG_RESCHED
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

        cells_html += parsed_string(cell_html, addon_config, cell_data)

    return cells_html


def stats_html():
    return HTML_SHELL.replace("{cell_data}", cell_data_html())


def parsed_string(string: str, addon_config: dict, cell_data: dict):
    updated_string = string
    _cached_range_time_ms: tuple[int, int] = 0, 0

    initial_time = time()

    def time_macros():
        # Time
        cmd = Macro.CMD_TOTAL_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_time(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS]))

        cmd = Macro.CMD_RANGE_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_time(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], _range_time_ms()))

        cmd = Macro.CMD_DAY_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_WEEK_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_TWO_WEEKS_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_MONTH_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_YEAR_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_PREV_RANGE_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: cell_data[Config.RANGE],
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
                Config.DAYS: cell_data[Config.DAYS],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_DAY_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_WEEK_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_TWO_WEEKS_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_MONTH_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_YEAR_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
            }
            _update_string_time(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_ETA_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            logs = filtered_revlog(addon_config[Config.EXCLUDED_DIDS])
            avg_hrs_per_card = _total_hrs_in_revlog(logs) / len(logs)

            total_count = 0
            due_tree = mw.col.sched.deck_due_tree()
            for child in due_tree.children:
                if child.deck_id not in addon_config[Config.EXCLUDED_DIDS]:
                    deck_conf = _conf_for_did(child.deck_id)

                    # Check for filtered/dynamic deck
                    if deck_conf and deck_conf.get('new', None):
                        delays = len(deck_conf['new'].get('delays', [0]))
                        total_count += (delays * child.new_count) + child.learn_count + child.review_count

            eta_hrs = avg_hrs_per_card * total_count

            unit_key = _unit_key_for_time(eta_hrs)
            _update_string_text(cmd, f'{_formatted_time(eta_hrs)} {cell_data[unit_key]}')

        cmd = fr'{Macro.CMD_FROM_DATE_HRS}:(\d\d\d\d-\d\d-\d\d)(?!:)'
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: str
            _process_range(match, replace_cb=_update_string_time, cmd=Macro.CMD_FROM_DATE_HRS)

        cmd = fr'{Macro.CMD_FROM_DATE_HRS}:(\d\d\d\d-\d\d-\d\d):(\d\d\d\d-\d\d-\d\d)'
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: tuple[str]
            _process_range(match[0], match[1], replace_cb=_update_string_time, cmd=Macro.CMD_FROM_DATE_HRS)

        # Avg
        cmd = Macro.CMD_DAY_AVG_HRS
        if re.findall(fr'(?<!%){cmd}', updated_string):
            logs = filtered_revlog(addon_config[Config.EXCLUDED_DIDS], _range_time_ms())
            from_date = datetime.fromtimestamp(_range_time_ms()[0] / 1000)
            to_date = datetime.fromtimestamp(_range_time_ms()[1] / 1000)
            days_in_logs = (to_date - from_date).days
            avg_hrs = _total_hrs_in_revlog(logs) / (days_in_logs if days_in_logs > 0 else 1)
            unit_key = _unit_key_for_time(avg_hrs)
            _update_string_text(cmd, f'{_formatted_time(avg_hrs)} {cell_data[unit_key]}')

        cmd = Macro.CMD_CARD_AVG_HRS
        if re.findall(fr'(?<!%){cmd}', updated_string):
            logs = filtered_revlog(addon_config[Config.EXCLUDED_DIDS], _range_time_ms())
            avg_hrs = _total_hrs_in_revlog(logs) / len(logs)
            unit_key = _unit_key_for_time(avg_hrs)
            _update_string_text(cmd, f'{_formatted_time(avg_hrs)} {cell_data[unit_key]}')

        cmd = Macro.CMD_HIGHEST_DAY_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier()
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _update_string_text(cmd, f'{_formatted_time(hours)} {cell_data[unit_key]}')

        cmd = Macro.CMD_HIGHEST_WEEK_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            # Set weekday to -1 of itself
            #  Note: SQLite's STRFTIME has Sunday at 0, while datetime (Python) has Monday at 0
            weekday_for_modifier = cell_data[Config.WEEK_START] - 1
            weekday_for_modifier += 7 if weekday_for_modifier < 0 else 0
            max_log = _max_log_from_modifier([f'weekday {weekday_for_modifier}'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _update_string_text(cmd, f'{_formatted_time(hours)} {cell_data[unit_key]}')

        cmd = Macro.CMD_HIGHEST_MONTH_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier(['start of month'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _update_string_text(cmd, f'{_formatted_time(hours)} {cell_data[unit_key]}')

        cmd = Macro.CMD_HIGHEST_YEAR_HRS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier(['start of year'])
            hours = max_log[1] / 60 / 60 / 1000
            unit_key = _unit_key_for_time(hours)
            _update_string_text(cmd, f'{_formatted_time(hours)} {cell_data[unit_key]}')

    def review_macros():
        # Reviews
        cmd = Macro.CMD_TOTAL_REVIEWS
        if re.findall(fr'(?<!%){cmd}', updated_string):
            _update_string_reviews(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS]))

        cmd = Macro.CMD_RANGE_REVIEWS
        if re.findall(fr'(?<!%){cmd}', updated_string):
            _update_string_reviews(cmd, filtered_revlog(addon_config[Config.EXCLUDED_DIDS], _range_time_ms()))

        cmd = Macro.CMD_DAY_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_WEEK_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_TWO_WEEKS_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_MONTH_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_YEAR_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data))
            )

        cmd = Macro.CMD_PREV_RANGE_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: cell_data[Config.RANGE],
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
                Config.DAYS: cell_data[Config.DAYS],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_DAY_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.CUSTOM,
                Config.DAYS: 1,
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_WEEK_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.WEEK,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_TWO_WEEKS_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.TWO_WEEKS,
                Config.USE_CALENDAR: True,
                Config.WEEK_START: cell_data[Config.WEEK_START],
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_MONTH_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.MONTH,
                Config.USE_CALENDAR: True,
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = Macro.CMD_PREV_YEAR_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            placeholder_data = {
                Config.RANGE: Range.YEAR,
                Config.USE_CALENDAR: True,
            }
            _update_string_reviews(
                cmd,
                filtered_revlog(addon_config[Config.EXCLUDED_DIDS], range_from_data(placeholder_data, 2))
            )

        cmd = fr'{Macro.CMD_FROM_DATE_REVIEWS}:(\d\d\d\d-\d\d-\d\d)(?!:)'
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: str
            _process_range(match, replace_cb=_update_string_reviews, cmd=Macro.CMD_FROM_DATE_REVIEWS)

        cmd = fr'{Macro.CMD_FROM_DATE_REVIEWS}:(\d\d\d\d-\d\d-\d\d):(\d\d\d\d-\d\d-\d\d)'
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: tuple[str]
            _process_range(match[0], match[1], replace_cb=_update_string_reviews, cmd=Macro.CMD_FROM_DATE_REVIEWS)

        cmd = Macro.CMD_HIGHEST_DAY_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier(order_by='count')
            reviews = max_log[2]
            _update_string_text(cmd, str(reviews))

        cmd = Macro.CMD_HIGHEST_WEEK_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            # Set weekday to -1 of itself
            #  Note: SQLite's STRFTIME has Sunday at 0, while datetime (Python) has Monday at 0
            weekday_for_modifier = cell_data[Config.WEEK_START] - 1
            weekday_for_modifier += 7 if weekday_for_modifier < 0 else 0
            max_log = _max_log_from_modifier([f'weekday {weekday_for_modifier}'], order_by='count')
            reviews = max_log[2]
            _update_string_text(cmd, str(reviews))

        cmd = Macro.CMD_HIGHEST_MONTH_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier(['start of month'], order_by='count')
            reviews = max_log[2]
            _update_string_text(cmd, str(reviews))

        cmd = Macro.CMD_HIGHEST_YEAR_REVIEWS
        if re.search(fr'(?<!%){cmd}', updated_string):
            max_log = _max_log_from_modifier(['start of year'], order_by='count')
            reviews = max_log[2]
            _update_string_text(cmd, str(reviews))

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

            _update_string_text(cmd, repl)

        cmd = Macro.CMD_DATE + '(?!:)'
        if re.findall(fr'(?<!%){cmd}', updated_string):
            _update_string_text(fr'(?<!%){cmd}', datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime("%x"))

        cmd = Macro.CMD_DATE_STRF
        for match in re.findall(fr'(?<!%){cmd}', updated_string):
            match: str
            date_format = match[match.find("\"") + 1:match.rfind("\"")]
            _update_string_text(match, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime(date_format))

        cmd = Macro.CMD_YEAR
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%Y'))

        cmd = Macro.CMD_FULL_DAY
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%A'))

        cmd = Macro.CMD_DAY
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%a'))

        cmd = Macro.CMD_MONTH
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%b'))

        cmd = Macro.CMD_FULL_MONTH
        if re.search(fr'(?<!%){cmd}', updated_string):
            _update_string_text(cmd, datetime.fromtimestamp(_range_time_ms()[0] / 1000).strftime('%B'))

        cmd = Macro.CMD_DAYS
        if re.search(fr'(?<!%){cmd}', updated_string):
            from_date = datetime.fromtimestamp(_range_time_ms()[0] / 1000)
            to_date = date_with_rollover(datetime.today())
            delta_days = (to_date - from_date).days
            _update_string_text(cmd, str(delta_days))

    def eval_macros(precision=2):
        """
        Evaluates and formats calc expressions in the cell's html.

        :param precision: The precision of the resulting value.
        """
        for match in (matches := re.findall(fr'(?<!%){Macro.CMD_EVAL}([^}}]*)}}', updated_string)):
            expression = match
            raw_match = match.replace('+', r'\+').replace('*', r'\*').replace('-', r'\-')
            is_using_hours = False
            result = 0

            expression = expression.lstrip('0')

            if f' {cell_data[Config.MIN_UNIT]}' in expression:
                is_using_hours = True
                expression = re.sub(
                    fr'(\d+)\s+{cell_data[Config.MIN_UNIT]}',
                    lambda m: str(int(m.group(1)) * 60),
                    expression,
                )

            if f' {cell_data[Config.HRS_UNIT]}' in expression:
                is_using_hours = True
                expression = re.sub(fr'\s+{cell_data[Config.HRS_UNIT]}', '', expression)

            # ! INSECURE !
            #  Leaving open-ended, for now, may want to do some more checks depending on use-cases
            try:
                result = eval(expression)
            except ValueError:
                result = "ERR"
                is_using_hours = False

            if is_using_hours:
                unit_key = _unit_key_for_time(result)
                _update_string_text(
                    fr'{Macro.CMD_EVAL}{raw_match}\}}',
                    f'{_formatted_time(result)} {cell_data[unit_key]}',
                )
            else:
                _update_string_text(
                    fr'{Macro.CMD_EVAL}{raw_match}\}}',
                    f'{round(result, precision):n}',
                )

    def _update_string_time(macro: str, revlog: list = None):
        nonlocal updated_string

        if revlog is None:
            updated_string = re.sub(fr'(?<!%){macro}', f'ERR', updated_string)
            return

        total_hrs = _total_hrs_in_revlog(revlog)
        unit_key = _unit_key_for_time(total_hrs)
        updated_string = re.sub(
            fr'(?<!%){macro}',
            f'{_formatted_time(total_hrs)} {cell_data[unit_key]}',
            updated_string,
        )

    def _update_string_reviews(macro: str, revlog: list = None):
        nonlocal updated_string

        if revlog is None:
            updated_string = re.sub(fr'(?<!%){macro}', f'ERR', updated_string)
            return

        total_reviews = len(revlog)
        updated_string = re.sub(fr'(?<!%){macro}', str(total_reviews), updated_string)

    def _update_string_text(macro: str, text: str):
        nonlocal updated_string
        updated_string = re.sub(fr'(?<!%){macro}', text, updated_string)

    def _process_range(from_date_str: str, to_date_str: str = None, replace_cb=None, cmd=Macro.CMD_FROM_DATE_HRS):
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
                    replace_cb(
                        fr'{cmd}:{from_date_str}:{to_date_str}',
                        filtered_revlog(addon_config[Config.EXCLUDED_DIDS], (from_ms, to_ms)),
                    )

            else:
                to_date_raw = datetime.today()
                to_ms = int(date_with_rollover(to_date_raw).timestamp() * 1000)
                if replace_cb:
                    replace_cb(
                        fr'{cmd}:{from_date_str}(?!:)',
                        filtered_revlog(addon_config[Config.EXCLUDED_DIDS], (from_ms, to_ms)),
                    )

        except ValueError:
            if replace_cb:
                replace_cb(fr'{cmd}:{from_date_str}(:{to_date_str})?', None)

    def _range_time_ms() -> tuple[int, int]:
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

    def _max_log_from_modifier(
        modifiers: [str] = None,
        timerange: tuple[int, int] = _range_time_ms(),
        order_by='time'
    ) -> Sequence:
        """
        Grabs a log with the highest total time and total reviews found in the selected range,
        suggested by the given modifier. Uses 'start of day' modifier for all queries.
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
            INNER JOIN cards
            ON revlog.cid = cards.id
            -- Select reviews only, excluding preset decks, between "range_limit" range
            WHERE revlog.type < {REVLOG_RESCHED}
            {_excluded_did_limit(addon_config[Config.EXCLUDED_DIDS])}
            {range_limit}
            -- Get highest value via group, sort, and the first (highest) row
            GROUP BY startOfRange
            ORDER BY {order_by} DESC LIMIT 1;
        '''

        print(f'sql_cmd={sql_query}')

        max_log = mw.col.db.first(sql_query)
        if not max_log:
            print(f'max_log returned an emtpy array for selected modifier(s): {modifiers}')
            max_log = [0, 0]

        return max_log

    time_macros()
    review_macros()
    text_macros()
    eval_macros()

    print(f'Commands completed. Elapsed time: {((time() - initial_time) * 1000):2f}ms')
    print()

    return updated_string


def range_from_data(cell_data: dict, iterations=1) -> tuple[int, int]:
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


def _excluded_did_limit(excluded_dids: list = None):
    include_deleted = TimeStatsConfigManager(mw).config.get(Config.INCLUDE_DELETED, False)

    if include_deleted and mw.state != 'overview':
        # If not currently viewing a deck, including deleted decks, grab all non-excluded deck ids
        filtered_did_cmd = f'AND cards.did NOT IN {_args_from_ids(excluded_dids) if excluded_dids else ""}'

    else:
        # Grab the current parent/children deck ids (inclusive) if viewing a deck, else grab all deck ids (inclusive)
        if mw.state == 'overview':
            included_dids = [
                i for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))
                if i not in excluded_dids
            ]
        else:
            included_dids = [
                name_id.id for name_id in mw.col.decks.all_names_and_ids()
                if name_id.id not in excluded_dids
            ]

        filtered_did_cmd = f'AND cards.did IN {_args_from_ids(included_dids)}'

    return filtered_did_cmd


def filtered_revlog(excluded_dids: list = None, time_range_ms: tuple[int, int] = None) \
        -> list[Sequence]:
    """
    Grabs a list of review data logs which each have the format: [timestamp, timerange].
    :param excluded_dids:
    :param time_range_ms:
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
        SELECT revlog.id, revlog.time
        FROM revlog
        INNER JOIN cards
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

    :param date: date to adjust
    :return: an adjusted datetime object
    """
    return date.replace(hour=23, minute=59, second=59) + timedelta(hours=_offset_hour())
