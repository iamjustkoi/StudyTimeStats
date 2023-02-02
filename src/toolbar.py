# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

from datetime import date

from aqt import mw
from aqt.qt import QAction

from .config import TimeStatsConfigManager
from .options import TimeStatsOptionsDialog
from .consts import (
    Config,
    String,
    UNIQUE_DATE,
)


def build_toolbar_actions():
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
