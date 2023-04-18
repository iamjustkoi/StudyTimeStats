# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

from aqt import mw
from aqt.qt import QAction

from .config import TimeStatsConfigManager
from .consts import (
    Config,
    String,
)
from .options import TimeStatsOptionsDialog


def build_toolbar_actions():
    refresh_tools_menu_action()
    mw.addonManager.setConfigAction(__name__, on_options_called)


def refresh_tools_menu_action(__changes=None, __obj=None):
    """
    Updates the toolbar actions menu with the options shortcut. Expects an Operation Change hook call,
    but can also be used as a general update push, too.

    :param __changes: unused OpChanges object
    :param __obj: unused options object
    """
    if TimeStatsConfigManager(mw).config[Config.TOOLBAR_ENABLED]:
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
    dialog = TimeStatsOptionsDialog(TimeStatsConfigManager(mw))
    dialog.exec()
