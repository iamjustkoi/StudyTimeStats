from PyQt5.QtWidgets import QAction
# from anki import cards
from aqt import mw


def buildHooks():
    pass


def getTimeStats():
    if mw.state == "deckBrowser":
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))]

    else:
        dids = mw.col.decks.allIds()

    dids_as_args = "(" + ", ".join(dids) + ")"

    cids = mw.col.db.all(f'''SELECT id FROM cards WHERE did in {dids_as_args}\n''')
    formatted_cids = "(" + (str(cids).replace("[", "").replace("]", "")) + ")"

    card_stats = mw.col.db.all(f'''SELECT cid, time FROM revlog WHERE cid in {formatted_cids}''')
    card_ids = [i[0] for i in card_stats[0:]]
    card_times_ms = [i[1] for i in card_stats[0:]]

    from aqt.utils import tooltip
    tooltip(f"total: {len(card_ids)} time (hr): {sum(card_times_ms)/1000/60}", period=6000, x_offset=50)


buildHooks()
action_stats = QAction("Get Time Stats", mw)
action_stats.triggered.connect(getTimeStats)
if mw.form.menuTools.actions().__contains__(action_stats):
    mw.form.menuTools.removeAction(action_stats)
mw.form.menuTools.addAction(action_stats)
