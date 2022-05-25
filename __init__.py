from PyQt5.QtWidgets import QAction
# from anki import cards
from aqt import mw

window_state = "overview"


def buildHooks():
    from aqt.gui_hooks import (state_will_change)
    state_will_change.append(on_window_state_will_change)


def on_window_state_will_change(old: str, new: str):
    global window_state
    window_state = new


def getTimeStats():
    global window_state
    # count, rev_time = mw.col.db.first("""select count(), sum(time)/1000/60 from revlog""") or 0
    if window_state == "deckBrowser":
        dids = mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))
    else:
        dids = "(" + (", ".join(mw.col.decks.allIds())) + ")"

    # cids = mw.col.db.all(f"select id from cards where did in {dids}")

    print(f"dids: \n {dids}")

    # TODO: Get cards with id filter from current deck

    # rev_stats = mw.col.db.all(f"""SELECT (Sum(time)/1000/60), (cid) FROM revlog WHERE cid In {ids};""") or 0
    # rev_time = mw.col.db.first(f"""select sum(time)/1000/60 from revlog""") or 0

    # rev_stats = mw.col.db.all(f"""SELECT cid FROM revlog WHERE cid in {ids}""") or 0
    # if total_time:
    #     print(f"Time: {total_time} minutes, {total_time / 60} hours.")
    # else:
    #     print("Not number.")


buildHooks()
action_stats = QAction("Get Time Stats", mw)
action_stats.triggered.connect(getTimeStats)
if mw.form.menuTools.actions().__contains__(action_stats):
    mw.form.menuTools.removeAction(action_stats)
mw.form.menuTools.addAction(action_stats)
