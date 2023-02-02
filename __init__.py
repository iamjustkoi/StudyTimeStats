# MIT License: Copyright (c) 2022-2023 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
# Full license text available in the "LICENSE" file, packaged with the add-on.

"""
Shows total study time and a ranged amount of study time in Anki's main window.
"""
from .src import overview
from .src import toolbar


def initialize():
    """
Initializer for the add-on. Called at the start for finer execution order and a bit of readability.
    """
    overview.build_hooks()
    toolbar.build_toolbar_actions()


initialize()
