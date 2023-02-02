# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.overview import Overview, OverviewContent

from .config import TimeStatsConfigManager
from .consts import *


def append_to_browser(deck_browser: DeckBrowser, content: DeckBrowserContent):
    if TimeStatsConfigManager(mw).config[Config.BROWSER_ENABLED]:
        content.stats += stats_html()


def append_to_overview(overview: Overview, content: OverviewContent):
    conf_manager = TimeStatsConfigManager(mw)

    def is_enabled_for_deck():
        return mw.col.decks.current().get('id') not in conf_manager.config[Config.EXCLUDED_DIDS]

    if conf_manager.config[Config.OVERVIEW_ENABLED] and is_enabled_for_deck():
        content.table += stats_html()


def cell_data_html():
    addon_config: dict = TimeStatsConfigManager(mw).config

    for cell_data in addon_config[Config.CELL_DATA]:
        cell_html: str = cell_data[Config.HTML].replace('{{', '{').replace('}}', '}')
        cell_html.format(
            CellClass=HORIZ_CLASS if cell_data[Config.DIRECTION] == Direction.HORIZONTAL else '',
            TitleColor=cell_data[Config.TITLE_COLOR],
        )

    return ''


def stats_html():
    """
    Uses the addon config and current get_time_stats to retrieve the html to display on Anki's main window.
    :return: html string containing review configured review information
    """
    # addon_config = TimeStatsConfigManager(mw).config

    return HTML_SHELL.format(cell_data=cell_data_html())


def build_hooks():
    gui_hooks.deck_browser_will_render_content.append(append_to_browser)
    gui_hooks.overview_will_render_content.append(append_to_overview)
